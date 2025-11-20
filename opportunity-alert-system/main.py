# main.py
import os
from datetime import datetime
from scrapers.yc import scrape_yc
from scrapers.t_hub import scrape_t_hub
from scrapers.startup_india import scrape_startup_india
from classifier.predict import is_relevant, load_model
from storage.firestore_client import get_client
from notifiers.sendgrid_notifier import send_email
from notifiers.telegram_notifier import send_telegram
from notifiers.push_placeholder import send_push
import hashlib
import time

# configuration
TO_EMAILS = os.getenv("ALERT_TO_EMAILS", "")  # comma separated
TO_EMAILS = [e.strip() for e in TO_EMAILS.split(",") if e.strip()]

def doc_id_from_link(link):
    return hashlib.sha256(link.encode("utf-8")).hexdigest()

def short_description(text, max_chars=250):
    # keep small: 2-3 lines ≈ 200-300 chars
    return (text[:max_chars] + "...") if len(text) > max_chars else text

def run():
    # load model (ensures model exists)
    try:
        load_model()
    except Exception as e:
        print("Classifier not ready:", e)
        # we can continue but mark everything as relevant by default? Here stop.
        return

    client = get_client()
    opportunities_col = client.collection("opportunities")

    # run scrapers
    scraped = []
    scraped.extend(scrape_yc())
    scraped.extend(scrape_t_hub())
    scraped.extend(scrape_startup_india())

    # process each item
    new_items = []
    for item in scraped:
        link = item.get("link")
        if not link:
            continue
        doc_id = doc_id_from_link(link)
        doc_ref = opportunities_col.document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            # already seen
            continue

        title = item.get("title", "")[:200]
        summary = item.get("summary", "") or ""
        combined_text = f"{title} {summary} {item.get('source','')}"
        try:
            relevant = is_relevant(combined_text)
        except Exception as e:
            print("Predict error:", e)
            relevant = False

        if relevant:
            # create record
            record = {
                "title": title,
                "link": link,
                "summary": summary,
                "source": item.get("source"),
                "posted_date": item.get("posted_date"),
                "date_scraped": datetime.utcnow(),
                "relevant": True,
                "notified": False
            }
            # save to firestore
            doc_ref.set(record)
            new_items.append((doc_id, record))
        else:
            # store as not relevant to track
            doc_ref.set({
                "title": title,
                "link": link,
                "summary": summary,
                "source": item.get("source"),
                "posted_date": item.get("posted_date"),
                "date_scraped": datetime.utcnow(),
                "relevant": False,
                "notified": False
            })

    # send notifications for new items
    for doc_id, record in new_items:
        title = record["title"]
        link = record["link"]
        summary = short_description(record.get("summary",""))
        # Telegram
        try:
            send_telegram(title, link, summary)
        except Exception as e:
            print("Telegram error:", e)
        # Email: form HTML
        if TO_EMAILS:
            html = f"<h3>{title}</h3><p>{summary}</p><p><a href='{link}'>Open</a></p><p>Source: {record.get('source')}</p>"
            try:
                send_email(subject=f"[Opportunity] {title}", html_content=html, to_emails=TO_EMAILS)
            except Exception as e:
                print("SendGrid email error:", e)
        # push placeholder
        send_push(title, summary, target="all")
        # mark notified
        client.collection("opportunities").document(doc_id).update({"notified": True, "notified_at": datetime.utcnow()})
        # small pause
        time.sleep(1)

if __name__ == "__main__":
    run()
