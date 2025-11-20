# Opportunity Alert System

Detects startup grants, incubators, pitch competitions and similar opportunities — stores in Firestore and notifies via SendGrid + Telegram.

## Setup

1. Create a Google Cloud project and Firestore DB (Native mode).
2. Create a service account with Firestore access. Download JSON.

### On Vercel
- In Vercel dashboard > Project > Settings > Environment Variables:
  - Add `SENDGRID_API_KEY`, `SENDGRID_FROM_EMAIL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `FIRESTORE_PROJECT_ID` etc.
- For service account JSON:
  - Add it as a Vercel secret (e.g. `gcp-service-account`) and during runtime write it to `/tmp/service-account.json` and set `GOOGLE_APPLICATION_CREDENTIALS=/tmp/service-account.json`. (Use a small wrapper script to write env var to file.)

### Locally
- Set `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`
- `export SENDGRID_API_KEY=...`
- `export SENDGRID_FROM_EMAIL=...`
- `export TELEGRAM_BOT_TOKEN=...`
- `export TELEGRAM_CHAT_ID=...`
- Optionally `export ALERT_TO_EMAILS="you@domain.com,cofounder@domain.com"`

## Train classifier (locally)
```bash
pip install -r requirements.txt
python classifier/train_model.py
