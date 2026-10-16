import time
import requests
import threading
from flask import Flask, request, redirect

app = Flask(__name__)

WALLET_ADDRESS = "0xB066d0aC0F00Db6Fc6410159ba5651642113B4e2"
POLYGON_RPC = "https://polygon-rpc.com"

@app.route('/')
def home():
    return "Komerza Vision Bot ist online!"

@app.route('/pay')
def pay():
    amount = request.args.get('amount', '1.0')
    order_id = request.args.get('order_id', '')

    # Direkte, stabile Weiterleitung zur Vision Wallet Einzahlungsseite
    target_url = f"https://visionw.app/extension/deposit-flow?address={WALLET_ADDRESS}&amount={amount}&network=polygon&commodity=USDT"
    
    return redirect(target_url)

def check_wallet_loop():
    while True:
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [WALLET_ADDRESS, "latest"],
                "id": 1
            }
            requests.post(POLYGON_RPC, json=payload, timeout=10)
            print(f"Wallet-Check aktiv für: {WALLET_ADDRESS}", flush=True)
        except Exception as e:
            print(f"Fehler beim Abfragen: {e}", flush=True)
        time.sleep(15)

threading.Thread(target=check_wallet_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
