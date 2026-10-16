import time
import requests
import threading
from flask import Flask

# Flask Server, damit Render den Service als dauerhaft aktiven Web Service erkennt
app = Flask(__name__)

WALLET_ADDRESS = "0xB066d0aC0F00Db6Fc6410159ba5651642113B4e2"
KOMERZA_WEBHOOK_URL = "https://solunacheats.mykomerza.com/api/webhooks/payment"
POLYGON_RPC = "https://polygon-rpc.com"

@app.route('/')
def home():
    return "Bot läuft aktiv!"

def check_wallet_loop():
    while True:
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [WALLET_ADDRESS, "latest"],
                "id": 1
            }
            res = requests.post(POLYGON_RPC, json=payload, timeout=10).json()
            print(f"Wallet-Check aktiv für: {WALLET_ADDRESS}")
        except Exception as e:
            print(f"Fehler beim Abfragen: {e}")
        time.sleep(15)

# Startet die Wallet-Prüfung im Hintergrund
threading.Thread(target=check_wallet_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
