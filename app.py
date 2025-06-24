from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Actual Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

@app.route("/")
def home():
    return "Slack bot is running!"

@app.route("/post-investment-update", methods=["POST"])
def post_to_slack():
    data = request.json
    message = data.get("message", "No update provided.")

    slack_data = { "text": message }
    print("Sending to Slack:", slack_data)

    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    print("Slack response:", response.status_code, response.text)

    if response.status_code != 200:
        return jsonify({"error": "Slack API failed", "details": response.text}), 500

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
