from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/..."  # 🔒 keep this secure in prod

@app.route("/")
def home():
    return "Slack bot is running!"

@app.route("/post-investment-update", methods=["POST"])
def post_to_slack():
    data = request.json
    message = data.get("message", "No update provided.")

    slack_data = {
        "text": message
    }

    print("Sending to Slack:", slack_data)  # ✅ useful debug output in Render logs

    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)

    if response.status_code != 200:
        return jsonify({
            "error": "Slack API failed",
            "details": response.text
        }), 500

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    # ✅ Required for Render: use PORT from environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
