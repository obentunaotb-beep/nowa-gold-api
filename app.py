from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def parse_klasgame_buy(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Burada fiyat ve buton durumu aranacak
    # Örnek: fiyat <span class="price">123.45 TL</span> gibi olabilir
    price = None
    buy_active = False

    # Örnek: fiyat bulmak için (sayfa yapısına göre ayarla)
    price_tag = soup.find("span", class_="price")
    if price_tag:
        price = price_tag.text.strip()

    # Buton aktif mi diye kontrol (örnek: buton sınıfında "disabled" varsa pasif say)
    buy_button = soup.find("button", string=lambda text: text and "Sepete Ekle" in text)
    if buy_button and "disabled" not in buy_button.attrs:
        buy_active = True

    return {
        "price": price,
        "buy_active": buy_active
    }

def parse_klasgame_sell(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    price = None
    sell_active = False

    price_tag = soup.find("span", class_="price")
    if price_tag:
        price = price_tag.text.strip()

    sell_button = soup.find("button", string=lambda text: text and "Satış Yap" in text)
    if sell_button and "disabled" not in sell_button.attrs:
        sell_active = True

    return {
        "price": price,
        "sell_active": sell_active
    }

@app.route("/gold")
def gold():
    # URL'ler
    ares_buy_url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb"
    ares_sell_url = "https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb"

    ultimate_buy_url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-ultimate-1m"
    ultimate_sell_url = "https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-ultimate-1m"

    return jsonify({
        "ares": {
            "buy": parse_klasgame_buy(ares_buy_url),
            "sell": parse_klasgame_sell(ares_sell_url)
        },
        "ultimate": {
            "buy": parse_klasgame_buy(ultimate_buy_url),
            "sell": parse_klasgame_sell(ultimate_sell_url)
        }
    })

if __name__ == "__main__":
    app.run()
