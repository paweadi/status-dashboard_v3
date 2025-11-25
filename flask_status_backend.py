from flask import Flask, jsonify
import requests

app = Flask(__name__)

services = {
    "azure": {"url": "https://status.azure.com/en-us/status", "type": "html"},
    "azuredevops": {"url": "https://status.dev.azure.com", "type": "html"},
    "databricks": {"url": "https://status.azuredatabricks.net/api/v2/status.json", "type": "json"},
    "jfrog": {"url": "https://status.jfrog.io/api/v2/status.json", "type": "json"},
    "elastic": {"url": "https://status.elastic.co/api/v2/status.json", "type": "json"},
    "octopus": {"url": "https://status.octopus.com/api/v2/status.json", "type": "json"},
    "lucid": {"url": "https://status.lucid.co/api/v2/status.json", "type": "json"},
    "jira": {"url": "https://status.atlassian.com/api/v2/status.json", "type": "json"},
    "confluence": {"url": "https://status.atlassian.com/api/v2/status.json", "type": "json"},
    "cucumber": {"url": "https://status.cucumberstudio.com/api/v2/status.json", "type": "json"},
    "fivetran": {"url": "https://status.fivetran.com/api/v2/status.json", "type": "json"},
    "brainboard": {"url": "https://status.brainboard.co", "type": "html"},
    "port": {"url": "https://status.port.io/api/v2/status.json", "type": "json"}
}

def parse_html_status(text):
    if "Operational" in text:
        return "All Systems Operational", "up"
    elif "Outage" in text:
        return "Major Outage", "down"
    elif "Degraded" in text:
        return "Degraded Performance", "degraded"
    else:
        return "Check site", "degraded"

@app.route('/status', methods=['GET'])
def get_status():
    results = {}
    for service, config in services.items():
        try:
            if config["type"] == "json":
                r = requests.get(config["url"], timeout=10)
                data = r.json()
                status_text = data.get("status", {}).get("description", "Unknown")
                badge_class = "up" if "Operational" in status_text else ("down" if "Outage" in status_text else "degraded")
            else:
                r = requests.get(config["url"], timeout=10)
                status_text, badge_class = parse_html_status(r.text)
            results[service] = {"status": status_text, "badge": badge_class}
        except Exception as e:
            results[service] = {"status": "Error", "badge": "degraded", "error": str(e)}
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
