# scrapers/t_hub.py
import requests
from bs4 import BeautifulSoup

def scrape_t_hub():
    url = "https://www.t-hub.co/in"  # placeholder; find actual announcements page
    results = []
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Example parsing - adapt to real structure
        for item in soup.select(".news-item")[:8]:
            title = item.select_one(".news-title").get_text(strip=True)
            link = item.select_one("a")["href"]
            if link.startswith("/"):
                link = "https://www.t-hub.co" + link
            summary = item.select_one(".news-excerpt").get_text(strip=True)[:300]
            results.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": "T-Hub",
                "posted_date": None
            })
    except Exception as e:
        print("T-Hub scraper error:", e)
    return results
