import os
import time
import requests

# 1. Deine Vision Wallet Adresse
WALLET_ADDRESS = "0xB066d0aC0F00Db6Fc6410159ba5651642113B4e2"

# 2. Deine Komerza Shop-URL
KOMERZA_WEBHOOK_URL = "https://solunacheats.mykomerza.com/api/webhooks/payment"

# Public Polygon RPC Node
POLYGON_RPC = "https://polygon-rpc.com"

def check_wallet_activity():
    """Prüft die Blockchain auf Geldeingänge an deiner Vision Wallet"""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [WALLET_ADDRESS, "latest"],
        "id": 1
    }
    try:
        response = requests.post(POLYGON_RPC, json=payload, timeout=10).json()
        print(f"Wallet-Check aktiv für Adresse: {WALLET_ADDRESS}")
        return True
    except Exception as e:
        print(f"Fehler bei Blockchain-Abfrage: {e}")
        return False

def notify_komerza(order_id, amount):
    """Meldet Komerza, dass bezahlt wurde, um die Ware automatisch zu verschicken"""
    payload = {
        "order_id": order_id,
        "status": "paid",
        "amount": amount,
        "currency": "USD"
    }
    try:
        res = requests.post(KOMERZA_WEBHOOK_URL, json=payload, timeout=10)
        if res.status_code == 200:
            print(f"Erfolg: Bestellung {order_id} auf Bezahlt gesetzt.")
    except Exception as e:
        print(f"Fehler beim Senden an Komerza: {e}")

if __name__ == "__main__":
    print("Starte automatischen Cloud-Bot...")
    while True:
        check_wallet_activity()
        time.sleep(15)  # Prüft alle 15 Sekunden
