from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# ✅ Your actual Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

@app.route("/")
def home():
    return "Slack bot is running!"

@app.route("/post-investment-update", methods=["POST"])
def post_to_slack():
    data = request.json
    message = data.get("message", "No update provided.")

    slack_data = { "text": message }
    print("Sending to Slack:", slack_data)  # ✅ useful debug output

    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    print("Slack response:", response.status_code, response.text)

    if response.status_code != 200:
        return jsonify({"error": "Slack API failed", "details": response.text}), 500

    return jsonify({"status": "success"}), 200

@app.route("/daily-summary", methods=["GET"])
def send_daily_summary():
    # Dummy data – replace with live data later
    week_start_date = "June 23, 2025"
    new_sites_reviewed = 26
    high_priority_sites = 3

    sites = [
        {"name": "Red Oak, TX", "score": 4.8, "url": "https://example.com/red-oak"},
        {"name": "Atlanta West", "score": 4.5, "url": "https://example.com/atl-west"},
        {"name": "Mesa, AZ", "score": 4.3, "url": "https://example.com/mesa-az"},
    ]

    site_lines = "\n".join([
        f"• {s['name']}: {s['score']}/5 – [View Listing]({s['url']})"
        for s in sites
    ])

    summary = f"""
📊 *Data Center Sites - Investment Summary – Week Commencing {week_start_date}*

• 🏗️ *New Sites Reviewed*: {new_sites_reviewed}  
• ✅ *High Priority Sites Identified*: {high_priority_sites}  
• 📌 *Site Name & Average Score*:  
{site_lines}

🛠️ Use our *Data Center Investment Radar* to evaluate, compare sites, and generate ICMs:  
👉 https://chatgpt.com/share/685af98b-f31c-8003-8a0b-bf37440419ca
""".strip()

    slack_data = { "text": summary }
    print("Sending daily summary to Slack...")
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    print("Slack response:", response.status_code, response.text)

    if response.status_code != 200:
        return jsonify({"error": "Slack post failed", "details": response.text}), 500

    return jsonify({"status": "summary sent"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
