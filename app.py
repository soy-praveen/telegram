from flask import Flask, request, render_template
import hashlib
import hmac
import os

app = Flask(__name__)

# Replace with your Telegram bot token
BOT_TOKEN = "7593282767:AAFUinSBdi9MDzzoRzw2RKEcB3BkH7qA_rQ"

def verify_telegram_payload(payload: dict, bot_token: str) -> bool:
    """
    Verifies the Telegram payload using the provided bot token.
    """
    auth_data = {k: v for k, v in payload.items() if k != "hash"}
    data_string = "\n".join(f"{k}={v}" for k, v in sorted(auth_data.items()))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()
    return calculated_hash == payload.get("hash")

@app.route("/")
def index():
    # Extract Telegram initData
    init_data = request.args.to_dict()

    # Validate payload
    if not verify_telegram_payload(init_data, BOT_TOKEN):
        return "Invalid payload!", 403

    # Pass data to frontend
    return render_template("index.html", user_data=init_data)

if __name__ == "__main__":
    app.run(debug=True)
