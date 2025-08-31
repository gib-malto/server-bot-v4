from seleniumbase import Driver
from selenium.webdriver.common.by import By
import time
import requests
import os
import platform

# ✅ Telegram Bot Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ✅ Target URL
URL = "https://androidmultitool.com/"
last_status = {}

# ✅ Only track these servers
TARGET_SERVERS = [
    "Infinix / Tecno / Itel Mediatek Auth",
    "Infinix / Tecno / Itel Spreadtrum Auth"
]


def notify(server, new_status):
    """Send Telegram notification for a specific server update"""
    if "online" in new_status.lower():
        msg = f"✅ {server} is ONLINE now!"
    elif "offline" in new_status.lower():
        msg = f"⚠️ {server} is OFFLINE now!"
    else:
        msg = f"ℹ️ {server} status: {new_status}"

    message = (
        "<b>AMT Server Status</b>\n"
        'by <a href="https://t.me/ryuofficial232">Ryu</a>\n\n'
        + msg
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        requests.post(url, data=data)
        print(f"[INFO] Telegram update sent: {msg}")
    except Exception as e:
        print("Error sending Telegram message:", e)

# ✅ Ensure PATH includes Chrome (important for Railway)
os.environ["PATH"] += os.pathsep + "/usr/bin"

# ✅ Launch undetected Chrome
driver = Driver(
    uc=True,
    headless=True,
    browser_path="/usr/bin/google-chrome-stable"  # force Railway Chrome
)
driver.uc_open_with_reconnect(URL, 15)

print("[INFO] Successfully bypassed Cloudflare")

first_run = True  # 👈 skip first-run notifications

while True:
    try:
        print("[INFO] Checking AMT Server Status...\n")

        # Example: find the server status table
        table = driver.find_element(By.CSS_SELECTOR, "table.table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                server_name = cols[0].text.strip()
                server_status = cols[1].text.strip()

                if server_name in TARGET_SERVERS:
                    print(f"{server_name}: {server_status}")

                    prev_status = last_status.get(server_name)

                    # ✅ Only notify if status changed AND not the first run
                    if prev_status != server_status and not first_run:
                        notify(server_name, server_status)

                    # ✅ Always update stored status
                    last_status[server_name] = server_status

        # after first loop, disable first-run skip
        if first_run:
            first_run = False

    except Exception as e:
        print("Error checking status:", e)

    time.sleep(10)  # wait before next check
    driver.refresh()
