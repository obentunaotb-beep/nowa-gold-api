from flask import Flask, jsonify
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)

# ------------------------
# Fiyat ve Buton Çekme Fonksiyonu
# ------------------------
async def fetch_price_and_button(url, button_text):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")  # Tüm JS yüklenene kadar bekle

        # Fiyatı çek
        price_element = await page.query_selector("span[data-type='price']")
        price = await price_element.inner_text() if price_element else None

        # Buton aktif mi?
        button_element = await page.query_selector(f"button:has-text('{button_text}')")
        active = False
        if button_element:
            disabled = await button_element.get_attribute("disabled")
            active = disabled is None

        await browser.close()
        return {"price": price, "active": active}

# ------------------------
# Flask Route
# ------------------------
@app.route("/gold")
def gold():
    urls = {
    "ares": {
        "buy": "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-10-gb",
        "sell": "https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb"
    },
    "ultimate": {
        "buy": "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-ultimate-1m",
        "sell": "https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-ultimate-1m"
    }
}

import asyncio
from playwright.async_api import async_playwright

async def install_browsers():
    from playwright._impl._driver import get_driver
    await get_driver().install()
