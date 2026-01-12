import feedparser
import pandas as pd
from datetime import datetime

SOURCES = {
    "Thailand": {
        "Bangkok Post": "https://www.bangkokpost.com/rss/data/topstories.xml",
        "The Nation": "https://www.nationthailand.com/rss",
        "Reuters": "https://www.reuters.com/world/asia-pacific/thailand/rss",
        "Lianhe Zaobao": "https://www.zaobao.com.sg/realtime/world/thailand/rss"
    },
    "Cambodia": {
        "Khmer Times": "https://www.khmertimeskh.com/feed/",
        "Cambodia China Times": "https://www.cctimeskh.com/feed/",
        "Cambodia Huashang": "https://cc-times.com/feed/"
    },
    "Indonesia": {
        "Antara": "https://en.antaranews.com/rss/news",
        "Reuters": "https://www.reuters.com/world/asia-pacific/indonesia/rss",
        "Lianhe Zaobao": "https://www.zaobao.com.sg/realtime/world/indonesia/rss"
    }
}

KEYWORDS = [
    # 安全 / 犯罪 / 反诈
    "scam", "fraud", "cybercrime", "online scam", "call center",
    "human trafficking", "trafficking", "illegal gambling",
    "terrorism", "counter-terrorism", "extremism",
    "separatist", "insurgency",

    # 政治 / 外交
    "government", "minister", "cabinet", "parliament",
    "foreign ministry", "diplomacy", "bilateral", "multilateral",
    "ASEAN", "China", "United States",

    # 经济 / 区域安全
    "economy", "trade", "investment", "sanctions",
    "border security", "maritime", "South China Sea"
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
