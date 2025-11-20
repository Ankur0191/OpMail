# scrapers/startup_india.py
import requests
from bs4 import BeautifulSoup

def scrape_startup_india():
    url = "https://www.startupindia.gov.in/content/sih/en/government-schemes.html"  # example
    results = []
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.select(".card")[:12]:
            title_tag = item.select_one(".card-title") or item.select_one("h3")
            if not title_tag: continue
            title = title_tag.get_text(strip=True)
            link_tag = item.select_one("a[href]")
            link = link_tag["href"] if link_tag else url
            summary = item.get_text(" ", strip=True)[:300]
            results.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": "Startup India",
                "posted_date": None
            })
    except Exception as e:
        print("Startup India scraper error:", e)
    return results
