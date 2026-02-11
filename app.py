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
        await page.goto(url, wait_until="networkidle")  # JS yüklenene kadar bekle

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
# URL'ler
# ------------------------
urls = {
    "ares": {
        "buy": "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world
