# scrapers/yc.py
import requests
from bs4 import BeautifulSoup
from dateutil import parser

def scrape_yc():
    results = []
    url = "https://www.ycombinator.com/announcements"  # example page; replace if YC has different listing
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # This is an example; YC's structure may change. Adapt selectors accordingly.
        for item in soup.select("article")[:10]:
            title_tag = item.find("h2") or item.find("h3")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link_tag = item.find("a", href=True)
            link = "https://www.ycombinator.com" + link_tag["href"] if link_tag else url
            summary = item.get_text(separator=" ", strip=True)[:300]
            # parse date if available
            date = None
            date_tag = item.find("time")
            if date_tag and date_tag.has_attr("datetime"):
                date = parser.parse(date_tag["datetime"])
            results.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": "YCombinator",
                "posted_date": str(date) if date else None
            })
    except Exception as e:
        print("YC scraper error:", e)
    return results
