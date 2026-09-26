const { execSync } = require('child_process');

console.log("Starting SPRINT 2: Generating 15 Comparison Articles");

for (let i = 1; i <= 15; i++) {
    console.log(`\n[${i}/15] Triggering Node.js Engine for Comparison Article...`);
    try {
        const result = execSync("node seo-automation-cron.js --test comparison", {
            cwd: "d:/project/plantsmag/engine",
            stdio: 'pipe'
        });
        const output = result.toString();
        console.log(`Success for article ${i}.`);
        const lines = output.trim().split('\n');
        lines.slice(-5).forEach(line => console.log(`  ${line}`));
    } catch (error) {
        console.log(`Error generating article ${i}:`);
        console.log(error.stderr ? error.stderr.toString() : error.message);
    }
    
    if (i < 15) {
        console.log("Cooling down for 3 seconds...");
        execSync("node -e \"Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 3000)\"");
    }
}

console.log("\nSPRINT 2 Generation Complete!");
