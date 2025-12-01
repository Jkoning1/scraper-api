from flask import Flask, request, jsonify
from scraper import funda_scrape

app = Flask(__name__)

@app.get("/scrape")
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is verplicht"}), 400
    try:
        data = funda_scrape(url)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/")
def home():
    return "Funda Scraper API draait."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
