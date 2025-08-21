# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Door Waar (Door Gorgorlou) is a WhatsApp-first service marketplace that connects clients with service providers (technicians) for various services including home services, IT support, tutoring, and errands. The system uses an AI agent to understand customer needs, gather requirements, and match them with suitable providers - all through WhatsApp conversations.

## Development Commands

### Run locally
```bash
# Start development server with hot reload
uvicorn app.main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/test-webhook -X POST -H "Content-Type: application/json" -d '{"test": "data"}'
```

### Environment setup
```bash
# Create virtual environment (if not exists)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env to set WEBHOOK_VERIFY_TOKEN
```

### Production deployment
```bash
# Uses Procfile for Heroku/similar platforms
# Runs: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

## Architecture & Key Components

### Core Application Structure
- **FastAPI Application** (`app/main.py`): Central API server handling WhatsApp webhooks
  - GET `/webhook`: WhatsApp webhook verification endpoint using Query aliases for hub.* parameters
  - POST `/webhook`: Receives and processes WhatsApp messages
  - Webhook verification uses `WEBHOOK_VERIFY_TOKEN` environment variable
  - Basic message type handling (text, image, audio) with logging

### Planned Architecture (from PRD)
The system will expand to include:

1. **Conversation Service**: AI agent orchestration for understanding user needs
   - Intent detection and service category classification
   - Slot collection (location, time, urgency, budget)
   - Multi-language support (English, French, local variants)

2. **Matching Engine**: Provider selection algorithm
   - Scoring based on distance, availability, rating, price fit, reliability
   - Hard constraints: availability, service area, vetting status
   - Fallback tiers for expanding search criteria

3. **Booking Lifecycle**: State management system
   - States: Draft → Proposed → ClientSelected → TechnicianAccepted → Confirmed → InProgress → Completed
   - WhatsApp template notifications at key transitions

4. **Provider Management**: Technician onboarding and interaction
   - KYC verification and skill mapping
   - WhatsApp-based job offers and acceptance/decline flow
   - Availability and scheduling management

5. **Data Storage** (Future):
   - PostgreSQL for core data
   - S3-compatible storage for media files
   - Redis for caching and queues

## WhatsApp Integration Notes

- Uses WhatsApp Business API/Cloud API
- Webhook verification requires exact match of `hub.mode`, `hub.verify_token`, and `hub.challenge` parameters
- Messages arrive as JSON with structure: `object` → `entry[]` → `changes[]` → `value` → `messages[]`
- Support for multiple message types: text, image, audio, location
- Template messages required for notifications outside 24-hour window
- Session messages for conversational flow within 24-hour window

## Key Implementation Priorities

1. **AI Agent Development**: Implement conversation service with LLM integration for intent detection and slot filling
2. **Provider Catalog**: Build service category taxonomy and provider skill mapping
3. **Matching Algorithm**: Implement scoring system with configurable weights
4. **WhatsApp Templates**: Create and get approval for notification templates
5. **Media Handling**: Implement secure storage and controlled sharing of images/videos
6. **Provider Interface**: Build WhatsApp-based provider interaction flows

## Important Environment Variables

- `WEBHOOK_VERIFY_TOKEN`: Required for WhatsApp webhook verification
- `PORT`: Automatically provided on Heroku for production deployment
- Future: `WHATSAPP_API_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID` for WhatsApp API calls

## Service Categories & Use Cases

The system handles diverse service requests:
- Home services: plumbing, electrical, repairs
- Professional services: IT support, tutoring
- Personal services: errands, assistance
- Each category requires specific slot collection and matching criteria

## Quality & Compliance Requirements

- 99.5% monthly uptime for conversational backend
- P95 messaging round-trip < 2s server-side
- LLM response < 4s average for standard prompts
- WCAG compliance for any web interfaces
- WhatsApp Business API policy compliance
- Data encryption at rest and in transit
- GDPR/privacy compliance with retention policies