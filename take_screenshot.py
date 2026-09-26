from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Desktop
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("http://localhost:3000/wedding-flowers/sage-green-wedding-flowers", wait_until="networkidle")
        page.screenshot(path=r"C:\Users\arezo\.gemini\antigravity-ide\brain\b6a5c05c-2a76-474c-9c92-8b41bd564c0e\desktop.png", full_page=True)
        
        # Mobile
        mobile_context = browser.new_context(
            viewport={"width": 375, "height": 812},
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        )
        mobile_page = mobile_context.new_page()
        mobile_page.goto("http://localhost:3000/wedding-flowers/sage-green-wedding-flowers", wait_until="networkidle")
        mobile_page.screenshot(path=r"C:\Users\arezo\.gemini\antigravity-ide\brain\b6a5c05c-2a76-474c-9c92-8b41bd564c0e\mobile.png", full_page=True)
        
        browser.close()

run()
