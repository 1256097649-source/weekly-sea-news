import feedparser
import pandas as pd
from datetime import datetime

SOURCES = {
    "Indonesia": {
        "Antara": "https://en.antaranews.com/rss/news"
    },
    "Cambodia": {
        "Reuters": "https://www.reuters.com/world/asia-pacific/rss"
    },
    "Thailand": {
        "Reuters": "https://www.reuters.com/world/asia-pacific/rss"
    }
}

KEYWORDS = [
    "security", "crime", "scam", "fraud",
    "diplomacy", "minister", "defence",
    "border", "ASEAN"
]

results = []

for country, feeds in SOURCES.items():
    for source, url in feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.lower()
            if any(k in title for k in KEYWORDS):
                results.append({
                    "country": country,
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "")
                })

df = pd.DataFrame(results)
today = datetime.now().strftime("%Y-%m-%d")
filename = f"weekly_news_{today}.csv"
df.to_csv(filename, index=False)

print(f"Saved {len(df)} news to {filename}")
