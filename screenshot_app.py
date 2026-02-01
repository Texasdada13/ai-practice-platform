"""
Screenshot Tool for AI Practice Platform
Automatically captures screenshots of all pages in the application.

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python screenshot_app.py
    python screenshot_app.py --mobile      # Include mobile/tablet views
    python screenshot_app.py --demo        # Use demo mode session
"""

import os
import sys
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Configuration
BASE_URL = "http://127.0.0.1:3847"
OUTPUT_DIR = "screenshots"

# Viewport configurations
VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
}

# Define all pages - organized by access requirements
LANDING_PAGES = [
    {
        "name": "Landing Page",
        "url": "/",
        "wait_for": "form"
    },
]

# Pages that require an assessment session (accessed via Demo Mode)
AUTHENTICATED_PAGES = [
    {
        "name": "Dashboard",
        "url": "/dashboard",
        "wait_for": ".score-circle"
    },
    {
        "name": "AI Chat",
        "url": "/chat",
        "wait_for": "#chatMessages"
    },
    {
        "name": "Frameworks",
        "url": "/frameworks",
        "wait_for": ".card"
    },
    {
        "name": "Roadmap",
        "url": "/roadmap",
        "wait_for": ".card"
    },
    {
        "name": "Use Cases",
        "url": "/use-cases",
        "wait_for": ".card"
    },
    {
        "name": "Documents",
        "url": "/documents",
        "wait_for": ".card"
    },
    {
        "name": "Results",
        "url": "/results",
        "wait_for": ".card"
    },
]

# Chat modes to capture
CHAT_MODES = [
    {"name": "General", "mode": "general"},
    {"name": "Strategy", "mode": "strategy"},
    {"name": "Governance", "mode": "governance"},
    {"name": "Technical", "mode": "technical"},
]


def sanitize_filename(name):
    """Convert a name to a safe filename."""
    return name.lower().replace(" ", "_").replace("/", "_").replace("?", "_").replace("&", "_")


async def take_screenshot(page, name, output_path):
    """Take a screenshot and save it."""
    await page.screenshot(path=output_path, full_page=True)
    print(f"  [OK] Captured: {name}")


async def capture_page(page, page_config, output_dir, viewport_name="desktop"):
    """Capture a single page."""
    name = page_config["name"]
    url = page_config["url"]
    wait_for = page_config.get("wait_for", "body")
    prefix = f"{viewport_name}_" if viewport_name != "desktop" else ""

    # Navigate to page
    await page.goto(f"{BASE_URL}{url}")

    # Wait for content to load
    try:
        await page.wait_for_selector(wait_for, timeout=10000)
    except:
        print(f"  [WARN] Warning: Could not find {wait_for} on {name}")

    # Small delay for any animations
    await asyncio.sleep(0.5)

    # Take main screenshot
    filename = f"{prefix}{sanitize_filename(name)}.png"
    await take_screenshot(
        page,
        f"{name} ({viewport_name})" if viewport_name != "desktop" else name,
        os.path.join(output_dir, filename)
    )


async def capture_chat_with_interaction(page, output_dir):
    """Capture chat page with sample interaction."""
    print("  Capturing chat interaction...")

    await page.goto(f"{BASE_URL}/chat")
    try:
        await page.wait_for_selector("#chatMessages", timeout=10000)
        await asyncio.sleep(1)  # Wait for chat session to initialize

        # Type a sample message
        input_field = await page.query_selector("#messageInput")
        if input_field:
            await input_field.fill("What are the key steps to build an AI strategy?")
            await asyncio.sleep(0.3)

            # Take screenshot with message typed
            await take_screenshot(
                page,
                "Chat - Message Typed",
                os.path.join(output_dir, "chat_message_typed.png")
            )

            # Submit the message
            submit_btn = await page.query_selector("#sendBtn")
            if submit_btn:
                await submit_btn.click()

                # Wait for response to start streaming
                await asyncio.sleep(2)

                await take_screenshot(
                    page,
                    "Chat - Response Streaming",
                    os.path.join(output_dir, "chat_response_streaming.png")
                )

                # Wait for response to complete
                await asyncio.sleep(5)

                await take_screenshot(
                    page,
                    "Chat - Conversation",
                    os.path.join(output_dir, "chat_conversation.png")
                )
    except Exception as e:
        print(f"    [WARN] Could not capture chat interaction: {e}")


async def capture_chat_modes(page, output_dir):
    """Capture chat in different modes."""
    for mode_config in CHAT_MODES:
        mode_name = mode_config["name"]
        mode_value = mode_config["mode"]

        print(f"  Capturing {mode_name} mode...")

        await page.goto(f"{BASE_URL}/chat")
        try:
            await page.wait_for_selector("#chatMessages", timeout=10000)
            await asyncio.sleep(0.5)

            # Click mode button if it exists
            mode_btn = await page.query_selector(f".mode-btn[data-mode='{mode_value}']")
            if mode_btn:
                await mode_btn.click()
                await asyncio.sleep(0.5)

            await take_screenshot(
                page,
                f"Chat - {mode_name} Mode",
                os.path.join(output_dir, f"chat_mode_{mode_value}.png")
            )
        except Exception as e:
            print(f"    [WARN] Could not capture {mode_name} mode: {e}")


async def capture_framework_generation(page, output_dir):
    """Capture framework generation page with generated content."""
    print("  Capturing framework generation...")

    await page.goto(f"{BASE_URL}/frameworks")
    try:
        await page.wait_for_selector(".card", timeout=10000)
        await asyncio.sleep(0.5)

        # Try to generate a strategy framework
        strategy_btn = await page.query_selector("button:has-text('Generate Strategy')")
        if strategy_btn:
            await strategy_btn.click()
            await asyncio.sleep(3)  # Wait for generation

            await take_screenshot(
                page,
                "Frameworks - Strategy Generated",
                os.path.join(output_dir, "frameworks_strategy_generated.png")
            )
    except Exception as e:
        print(f"    [WARN] Could not capture framework generation: {e}")


async def main():
    """Main function to capture all screenshots."""
    # Parse command line arguments
    include_mobile = "--mobile" in sys.argv
    use_demo = "--demo" in sys.argv or True  # Default to demo mode

    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(OUTPUT_DIR, timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Create subdirectories for mobile/tablet
    if include_mobile:
        os.makedirs(os.path.join(output_dir, "mobile"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "tablet"), exist_ok=True)

    print(f"\n{'='*60}")
    print("AI Practice Platform Screenshot Tool")
    print(f"{'='*60}")
    print(f"Output directory: {output_dir}")
    print(f"Base URL: {BASE_URL}")
    print(f"Options: mobile={include_mobile}, demo={use_demo}")
    print(f"{'='*60}\n")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)

        # Desktop context
        desktop_context = await browser.new_context(
            viewport=VIEWPORTS["desktop"]
        )
        page = await desktop_context.new_page()

        # Test connection
        print("Testing connection to application...")
        try:
            await page.goto(BASE_URL, timeout=5000)
            print("[OK] Connected successfully\n")
        except Exception as e:
            print(f"[ERROR] Could not connect to {BASE_URL}")
            print(f"  Make sure the Flask server is running:")
            print(f"    python web/app.py")
            await browser.close()
            return

        # Capture landing page
        print("Capturing landing page...")
        print("-" * 40)
        for page_config in LANDING_PAGES:
            try:
                await capture_page(page, page_config, output_dir, "desktop")
            except Exception as e:
                print(f"  [ERROR] Error capturing {page_config['name']}: {e}")

        print()

        # Enter demo mode to access authenticated pages
        if use_demo:
            print("Entering Demo Mode...")
            print("-" * 40)
            await page.goto(f"{BASE_URL}/demo")
            try:
                await page.wait_for_selector(".score-circle", timeout=10000)
                print("  [OK] Demo mode activated\n")
            except Exception as e:
                print(f"  [ERROR] Could not enter demo mode: {e}")
                await browser.close()
                return

        # Capture authenticated pages
        print("Capturing main pages (desktop)...")
        print("-" * 40)
        for page_config in AUTHENTICATED_PAGES:
            try:
                await capture_page(page, page_config, output_dir, "desktop")
            except Exception as e:
                print(f"  [ERROR] Error capturing {page_config['name']}: {e}")

        print()

        # Capture chat interactions
        print("Capturing chat interactions...")
        print("-" * 40)
        await capture_chat_with_interaction(page, output_dir)
        await capture_chat_modes(page, output_dir)

        print()

        # Capture framework generation
        print("Capturing framework generation...")
        print("-" * 40)
        await capture_framework_generation(page, output_dir)

        await desktop_context.close()

        # Mobile and tablet views
        if include_mobile:
            print()
            print("Capturing mobile and tablet views...")
            print("-" * 40)

            # Key pages to capture in mobile/tablet
            responsive_pages = [
                {"name": "Landing Page", "url": "/", "wait_for": "form"},
                {"name": "Dashboard", "url": "/dashboard", "wait_for": ".score-circle"},
                {"name": "AI Chat", "url": "/chat", "wait_for": "#chatMessages"},
                {"name": "Frameworks", "url": "/frameworks", "wait_for": ".card"},
            ]

            for viewport_name in ["tablet", "mobile"]:
                print(f"  {viewport_name.title()} viewport...")
                context = await browser.new_context(viewport=VIEWPORTS[viewport_name])
                resp_page = await context.new_page()

                # Enter demo mode for this context
                await resp_page.goto(f"{BASE_URL}/demo")
                await asyncio.sleep(1)

                for page_config in responsive_pages:
                    try:
                        await capture_page(
                            resp_page,
                            page_config,
                            os.path.join(output_dir, viewport_name),
                            viewport_name
                        )
                    except Exception as e:
                        print(f"    [ERROR] Error: {e}")

                await context.close()

        await browser.close()

    # Summary
    total_screenshots = 0
    for root, dirs, files in os.walk(output_dir):
        total_screenshots += len([f for f in files if f.endswith('.png')])

    print(f"\n{'='*60}")
    print(f"Complete! Captured {total_screenshots} screenshots")
    print(f"Location: {os.path.abspath(output_dir)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
