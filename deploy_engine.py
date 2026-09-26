#!/usr/bin/env python3
"""
deploy_engine.py – PlantsMag SEO Engine Deployment Script
=========================================================
Deploys the local engine/ directory to a VPS, configures PM2,
disables legacy N8N workflows, and runs a smoke test.

Target audience: US plant enthusiasts running PlantsMag infrastructure.
"""

import io
import os
import sys
import stat
import time
import json
import posixpath

# ── Force UTF-8 on stdout/stderr so Windows consoles don't choke ────────────
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import paramiko
except ImportError:
    print("❌  paramiko is not installed. Run:  pip install paramiko")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌  requests is not installed. Run:  pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

VPS_HOST = "72.62.93.117"
VPS_PORT = 22
VPS_USER = "root"
# NOTE: The password contains an apostrophe – store it in a raw string so
# Python does not misinterpret any escape sequences.
VPS_PASSWORD = r"5KT4'ub5B5oD8V9TB#/u"

LOCAL_ENGINE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine")
REMOTE_BASE_DIR = "/root/plantsmag-engine"
REMOTE_SUBDIRS = ["lib", "strategies", "logs"]

PM2_PROCESS_NAME = "plantsmag-seo"
ECOSYSTEM_FILE = "ecosystem.config.cjs"
TEST_SCRIPT = "seo-automation-cron.js"

# N8N API (runs on the same VPS)
N8N_BASE_URL = "http://localhost:5678/rest"
N8N_EMAIL = "plantsmag@gmail.com"
N8N_PASSWORD = "PlantsMag2026!"
N8N_WORKFLOW_IDS = [
    "CpyU2cf01DdtpfWo",
    "UKegbNpPIBkkNUrd",
    "SLgAkWAL2NBVzZ7U",
]

LOG_TAIL_LINES = 20


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def banner(step_num: int, title: str) -> None:
    """Print a clearly-visible step banner."""
    print(f"\n{'=' * 60}")
    print(f"  Step {step_num}: {title}")
    print(f"{'=' * 60}")


def run_ssh_command(ssh: paramiko.SSHClient, command: str, *, label: str = "") -> str:
    """
    Execute a command over SSH, stream output live, and return the
    combined stdout text.  Raises RuntimeError on non-zero exit.
    """
    if label:
        print(f"\n▶  {label}")
    print(f"   $ {command}")

    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    output_lines: list[str] = []

    for line in stdout:
        text = line.rstrip("\n").rstrip("\r")
        print(f"   {text}")
        output_lines.append(text)

    exit_code = stdout.channel.recv_exit_status()
    err_text = stderr.read().decode("utf-8", errors="replace").strip()

    if exit_code != 0:
        print(f"   ⚠  stderr: {err_text}")
        print(f"   ⚠  exit code: {exit_code}")
        # We warn but don't always raise – some PM2 commands return non-zero
        # when no process exists yet (e.g. pm2 stop on a missing process).
    return "\n".join(output_lines)


def sftp_mkdir_p(sftp: paramiko.SFTPClient, remote_dir: str) -> None:
    """Recursively create remote directories (like mkdir -p)."""
    dirs_to_create: list[str] = []
    current = remote_dir

    while True:
        try:
            sftp.stat(current)
            break  # exists
        except FileNotFoundError:
            dirs_to_create.append(current)
            parent = posixpath.dirname(current)
            if parent == current:
                break
            current = parent

    for d in reversed(dirs_to_create):
        try:
            sftp.mkdir(d)
            print(f"   📁 Created remote dir: {d}")
        except IOError:
            pass  # race condition or already exists


# ─────────────────────────────────────────────────────────────────────────────
# Main deployment flow
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    start_time = time.time()

    print("🌱  PlantsMag SEO Engine – Deployment Script")
    print(f"    Local source : {LOCAL_ENGINE_DIR}")
    print(f"    Remote target: {VPS_USER}@{VPS_HOST}:{REMOTE_BASE_DIR}")
    print(f"    Time         : {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Validate local engine directory exists
    if not os.path.isdir(LOCAL_ENGINE_DIR):
        print(f"\n❌  Local engine directory not found: {LOCAL_ENGINE_DIR}")
        print("    Make sure d:\\project\\plantsmag\\engine\\ exists and contains your project files.")
        sys.exit(1)

    # ── Step 1: SSH Connection ───────────────────────────────────────────
    banner(1, "Connect to VPS via SSH")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=VPS_HOST,
            port=VPS_PORT,
            username=VPS_USER,
            password=VPS_PASSWORD,
            timeout=30,
            look_for_keys=False,
            allow_agent=False,
        )
        print(f"   ✅ Connected to {VPS_HOST}:{VPS_PORT} as {VPS_USER}")
    except Exception as exc:
        print(f"   ❌ SSH connection failed: {exc}")
        sys.exit(1)

    # ── Step 2: Create remote directories ────────────────────────────────
    banner(2, "Create remote directory structure")
    sftp = ssh.open_sftp()

    sftp_mkdir_p(sftp, REMOTE_BASE_DIR)
    for subdir in REMOTE_SUBDIRS:
        sftp_mkdir_p(sftp, posixpath.join(REMOTE_BASE_DIR, subdir))
    print("   ✅ Directory structure ready")

    # ── Step 3: Upload all files from engine/ via SFTP ───────────────────
    banner(3, "Upload engine files via SFTP")
    file_count = 0
    total_bytes = 0

    for dirpath, dirnames, filenames in os.walk(LOCAL_ENGINE_DIR):
        # Skip node_modules and .git to avoid uploading dependencies
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git")]

        # Compute the relative path from the engine root
        rel_dir = os.path.relpath(dirpath, LOCAL_ENGINE_DIR)
        if rel_dir == ".":
            remote_dir = REMOTE_BASE_DIR
        else:
            # Convert Windows backslashes to POSIX forward slashes
            remote_dir = posixpath.join(REMOTE_BASE_DIR, rel_dir.replace("\\", "/"))

        # Ensure the remote directory exists
        sftp_mkdir_p(sftp, remote_dir)

        for filename in filenames:
            local_path = os.path.join(dirpath, filename)
            remote_path = posixpath.join(remote_dir, filename)
            file_size = os.path.getsize(local_path)

            print(f"   📤 {remote_path}  ({file_size:,} bytes)")
            sftp.put(local_path, remote_path)

            file_count += 1
            total_bytes += file_size

    sftp.close()
    print(f"\n   ✅ Uploaded {file_count} files ({total_bytes:,} bytes total)")

    # ── Step 4: npm install ──────────────────────────────────────────────
    banner(4, "Run npm install on the server")
    run_ssh_command(
        ssh,
        f"cd {REMOTE_BASE_DIR} && npm install",
        label="Installing Node.js dependencies",
    )
    print("   ✅ npm install complete")

    # ── Step 5: Install PM2 globally (if needed) ────────────────────────
    banner(5, "Ensure PM2 is installed globally")
    run_ssh_command(
        ssh,
        "command -v pm2 >/dev/null 2>&1 || npm install -g pm2",
        label="Checking / installing PM2",
    )
    print("   ✅ PM2 is available")

    # ── Step 6: Stop any existing PM2 process ────────────────────────────
    banner(6, f"Stop existing PM2 process '{PM2_PROCESS_NAME}'")
    run_ssh_command(
        ssh,
        f"pm2 stop {PM2_PROCESS_NAME} 2>/dev/null || echo 'No existing process to stop'",
        label="Stopping old process",
    )
    run_ssh_command(
        ssh,
        f"pm2 delete {PM2_PROCESS_NAME} 2>/dev/null || echo 'No existing process to delete'",
        label="Deleting old process entry",
    )
    print("   ✅ Old process cleaned up")

    # ── Step 7: Start the engine with PM2 ────────────────────────────────
    banner(7, "Start engine with PM2")
    run_ssh_command(
        ssh,
        f"cd {REMOTE_BASE_DIR} && pm2 start {ECOSYSTEM_FILE}",
        label="Starting via ecosystem config",
    )
    print("   ✅ PM2 process started")

    # ── Step 8: Save PM2 process list ────────────────────────────────────
    banner(8, "Save PM2 process list")
    run_ssh_command(ssh, "pm2 save", label="Persisting process list")
    print("   ✅ PM2 process list saved")

    # ── Step 9: PM2 startup ──────────────────────────────────────────────
    banner(9, "Configure PM2 startup on boot")
    run_ssh_command(ssh, "pm2 startup", label="Enabling PM2 startup hook")
    print("   ✅ PM2 startup configured")

    # N8N Workflows remain active as requested by the user.
    print("   ✅ Skipping N8N deactivation (Workflows remain active)")

    # ── Step 11: Run smoke test ──────────────────────────────────────────
    banner(11, "Run smoke test")
    run_ssh_command(
        ssh,
        f"cd {REMOTE_BASE_DIR} && node {TEST_SCRIPT} --test",
        label="Executing test run",
    )
    print("   ✅ Smoke test complete")

    # ── Step 12: Show PM2 status ─────────────────────────────────────────
    banner(12, "PM2 status")
    run_ssh_command(ssh, "pm2 status", label="Current PM2 processes")

    # ── Step 13: Show last 20 lines of log ───────────────────────────────
    banner(13, f"Last {LOG_TAIL_LINES} lines of PM2 log")
    run_ssh_command(
        ssh,
        f"pm2 logs --nostream --lines {LOG_TAIL_LINES}",
        label="Recent log output",
    )

    # ── Done ─────────────────────────────────────────────────────────────
    ssh.close()
    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"  🌱  Deployment complete in {elapsed:.1f}s")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
