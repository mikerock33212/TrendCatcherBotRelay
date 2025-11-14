import os
import requests
from flask import Flask, request

# Create the Flask web application instance. This is the core of our service.
app = Flask(__name__)

# The Discord Webhook URL will be stored as a secure environment variable.
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')


@app.route("/", methods=["POST"])
def discord_proxy_sender():
    """
    This is the main function that handles incoming HTTP POST requests.
    It acts as a secure relay to forward messages to Discord.
    """
    if not DISCORD_WEBHOOK_URL:
        print("FATAL ERROR: DISCORD_WEBHOOK_URL environment variable is not set.")
        return "Server configuration error.", 500

    request_json = request.get_json(silent=True)
    if not request_json or 'message' not in request_json:
        return "Invalid request: Body must be JSON with a 'message' field.", 400

    message_content = request_json['message']
    discord_payload = {'content': message_content}

    try:
        # Make the outbound request to Discord from the Google Cloud server.
        response = requests.post(DISCORD_WEBHOOK_URL, json=discord_payload)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        print(f"Successfully relayed message to Discord: {message_content}")
        return "Message relayed successfully.", 200

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Discord's webhook URL: {e}")
        return "Failed to relay message to Discord.", 502  # 502 Bad Gateway is appropriate here


# This block is NOT used by Cloud Run, but is essential for local testing.
# Cloud Run uses the command from the Dockerfile to start the server.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
