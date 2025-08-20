from flask import Flask, render_template, request
import requests
import math
import os

app = Flask(__name__)

API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY")  # Replace with your API key if not using env
BASE_URL = "https://newsapi.org/v2/top-headlines"
PAGE_SIZE = 4  # show 4 articles per page


def fetch_articles(page=1, topic="technology"):
    params = {
        "apiKey": API_KEY,
        "country": "us",
        "pageSize": PAGE_SIZE,
        "page": page
    }
    if topic:
        params["category"] = topic

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return [], 1

    total_results = data.get("totalResults", 0)
    total_pages = max(1, math.ceil(total_results / PAGE_SIZE))

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title"),
            "content": article.get("description") or "",
            "image_url": article.get("urlToImage"),
            "source_url": article.get("url"),
            "timestamp": article.get("publishedAt"),
            "source": article.get("source", {}).get("name", "Unknown")
        })

    return articles, total_pages


@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    topic = request.args.get("topic", "technology")  # default = technology

    articles, total_pages = fetch_articles(page, topic)

    return render_template("index.html",
                           articles=articles,
                           page=page,
                           total_pages=total_pages,
                           topic=topic)


if __name__ == "__main__":
    app.run(debug=True)
