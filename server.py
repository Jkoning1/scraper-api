from flask import Flask, request, jsonify
from scraper import funda_scrape

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing url"}), 400

    try:
        results = funda_scrape(url)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Funda Scraper API is running 👋"

