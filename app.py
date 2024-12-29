import os
from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

# Replace this with your actual Telegram bot token
BOT_TOKEN = "7593282767:AAFUinSBdi9MDzzoRzw2RKEcB3BkH7qA_rQ"

def verify_telegram_payload(payload: dict, bot_token: str) -> bool:
    """
    Verifies Telegram WebApp payload using the provided bot token.
    """
    try:
        # Exclude hash from the payload for verification
        auth_data = {k: v for k, v in payload.items() if k != "hash"}
        data_string = "\n".join(f"{k}={v}" for k, v in sorted(auth_data.items()))
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()
        return calculated_hash == payload.get("hash")
    except Exception as e:
        print(f"Error in payload verification: {e}")
        return False

@app.route("/")
def index():
    # Extract Telegram initData from the request
    init_data = request.args.to_dict()

    # Log the received initData for debugging
    print("Received initData:", init_data)

    # Check if the 'hash' field is missing
    if "hash" not in init_data:
        print("Error: 'hash' field missing from initData!")
        return "Invalid payload: Missing hash!", 403

    # Log the raw hash and the calculated hash for debugging
    calculated_hash = verify_telegram_payload(init_data, BOT_TOKEN)
    print("Calculated Hash:", calculated_hash)

    # Validate payload using the hash verification
    if not calculated_hash:
        print("Invalid payload detected. InitData:", init_data)
        return "Invalid payload!", 403

    # If valid, return user details
    return jsonify({
        "status": "success",
        "message": "Payload verified successfully!",
        "user_data": init_data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
