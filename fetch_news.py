import feedparser
import pandas as pd
from datetime import datetime

SOURCES = {
    "Thailand": {
        "Bangkok Post": "https://www.bangkokpost.com/rss/data/topstories.xml",
        "The Nation Thailand": "https://www.nationthailand.com/rss",
        "Reuters": "https://www.reuters.com/world/asia-pacific/rss",
        "Lianhe Zaobao": "https://www.zaobao.com.sg/rss.xml"
    },
    "Cambodia": {
        "Khmer Times": "https://www.khmertimeskh.com/feed/",
        "Cambodia China Times": "https://www.cc-times.com/feed/",
        "Cambodian Chinese Daily": "https://www.ccdnews.com/feed/"
    },
    "Indonesia": {
        "Antara": "https://en.antaranews.com/rss/news",
        "Reuters": "https://www.reuters.com/world/asia-pacific/rss",
        "Lianhe Zaobao": "https://www.zaobao.com.sg/rss.xml"
    }
}

KEYWORDS = [
    "scam", "fraud", "trafficking", "cybercrime", "money laundering",
    "terror", "terrorism", "extremism", "insurgency", "separatist",
    "security", "military", "army", "police", "defence",
    "minister", "government", "diplomacy", "bilateral",
    "talks", "summit", "election",
    "economy", "trade", "investment", "inflation",
    "development", "policy",
    "ASEAN", "border", "regional", "maritime"
]

results = []

for country, feeds in SOURCES.items():
    for source, url in feeds.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "")
            if any(k.lower() in title.lower() for k in KEYWORDS):
                results.append({
                    "country": country,
                    "source": source,
                    "title": title,
                    "link": entry.get("link", ""),
                    "published": entry.get("published", "")
                })

df = pd.DataFrame(results)

today = datetime.now().strftime("%Y-%m-%d")
filename = f"weekly_news_{today}.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"Saved {len(df)} records to {filename}")
