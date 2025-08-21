# Door Waar — Developer README

Dev-focused overview. For the product vision and full specification, see docs/PRD.md.

## Stack
- Python 3.11
- FastAPI (API server)
- Uvicorn (dev), Gunicorn + UvicornWorker (prod)
- Deployed on platforms supporting Procfile (e.g., Heroku)

## Project Structure
- app/main.py — FastAPI app with WhatsApp webhook endpoints (GET verify, POST receive)
- Procfile — Production process definition
- requirements.txt — Python dependencies
- runtime.txt — Python runtime pin (Heroku)
- docs/PRD.md — Product Requirements Document

## Setup
1) Python environment
	- Create and activate a virtualenv or use pyenv/conda.
2) Install dependencies
	- pip install -r requirements.txt
3) Environment variables
	- WEBHOOK_VERIFY_TOKEN: token used for WhatsApp webhook verification
	- PORT (prod/heroku): automatically provided on Heroku
	- Copy .env.example to .env if using a local env loader (optional)

## Run (Local)
- Dev server:
  - uvicorn app.main:app --reload --port 8000
- Health check: GET http://localhost:8000/health
- Webhook verify (GET /webhook with hub.mode, hub.verify_token, hub.challenge)
- Webhook receive (POST /webhook) — send sample payloads via /test-webhook

## Deploy
- Procfile: web: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
- Ensure WEBHOOK_VERIFY_TOKEN is set in the environment

## Docs
- PRD: docs/PRD.md
