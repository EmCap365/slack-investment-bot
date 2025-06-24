from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

@app.route("/post-investment-update", methods=["POST"])
def post_to_slack():
    data = request.json
    message = data.get("message", "No update provided.")

    slack_data = {
        "text": message
    }

    print("Sending to Slack:", slack_data)
    
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)

    if response.status_code != 200:
        return jsonify({"error": "Slack API failed", "details": response.text}), 500

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=5000)
