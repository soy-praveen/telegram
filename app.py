import os
from flask import Flask, request, render_template
import hashlib
import hmac

app = Flask(__name__)

# Replace with your Telegram bot token
BOT_TOKEN = "7593282767:AAFUinSBdi9MDzzoRzw2RKEcB3BkH7qA_rQ"

def verify_telegram_payload(payload: dict, bot_token: str) -> bool:
    """
    Verifies the Telegram payload using the provided bot token.
    """
    try:
        auth_data = {k: v for k, v in payload.items() if k != "hash"}
        data_string = "\n".join(f"{k}={v}" for k, v in sorted(auth_data.items()))
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()
        return calculated_hash == payload.get("hash")
    except Exception as e:
        print(f"Error during payload verification: {e}")
        return False

@app.route("/")
def index():
    # Extract Telegram initData
    init_data = request.args.to_dict()

    # Debug: Print the received initData
    print("Received initData:", init_data)

    # Validate payload
    if not verify_telegram_payload(init_data, BOT_TOKEN):
        print("Invalid payload received:", init_data)  # Debugging info
        return "Invalid payload!", 403

    # Debug: Print valid initData
    print("Valid initData:", init_data)

    # Pass data to frontend
    return render_template("index.html", user_data=init_data)

if __name__ == "__main__":
    # Use environment variable for the port, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
