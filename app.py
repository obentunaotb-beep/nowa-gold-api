from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price_and_status(url, button_text):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Fiyat çekme
    price_tag = soup.find("span", {"data-type": "price"})
    price = price_tag.text.strip() if price_tag else None

    # Buton kontrolü
    button = soup.find("button", string=lambda text: text and button_text in text)
    active = False

    if button and not button.has_attr("disabled"):
        active = True

    return {
        "price": price,
        "active": active
    }

@app.route("/gold")
def gold():

    ares_buy_url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb"
    ares_sell_url = "https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb"

    ultimate_buy_url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-ultimate-1m"
    ultimate_sell_url = "https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-ultimate-1m"

    return jsonify({
        "ares": {
            "buy": get_price_and_status(ares_buy_url, "Sepete Ekle"),
            "sell": get_price_and_status(ares_sell_url, "Satış Yap")
        },
        "ultimate": {
            "buy": get_price_and_status(ultimate_buy_url, "Sepete Ekle"),
            "sell": get_price_and_status(ultimate_sell_url, "Satış Yap")
        }
    })

if __name__ == "__main__":
    app.run()
import asyncio
from playwright.async_api import async_playwright

async def install_browsers():
    from playwright._impl._driver import get_driver
    await get_driver().install()
