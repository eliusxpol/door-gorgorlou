# Door Waar — Product Requirements Document (PRD)

Last updated: 2025-08-21
Owner: Product (Door Waar)
Status: Draft v1 (for review)

## 1) Summary
Door Waar helps clients find the right service provider for any service category (home services like plumbing/electrical, as well as broader services such as IT support, tutoring, errands, etc.) via WhatsApp. An AI agent converses with the client to understand the need, collects constraints (location, time, budget, urgency), and proposes the best available, nearby, and qualified provider from the Door Waar catalog. The client can review, confirm, schedule, and receive updates—all within WhatsApp. Providers ("technicians" or more generally "service providers") also interact via WhatsApp to receive offers, accept/decline, coordinate, and report completion.

## 2) Goals and Non‑Goals

Goals (MVP)
- Provide a WhatsApp-first experience to request home services in minutes.
- Use an AI agent to understand user need and gather key details with minimal friction.
- Match clients to suitable technicians based on proximity, availability, skills, ratings, and price.
- Coordinate booking, confirmations, and reminders within WhatsApp.
- Provide a basic operator/admin workflow to intervene and resolve issues.
 - Support technician/provider-side interactions via WhatsApp: receive job proposals, accept/decline, lightweight coordination.

Non-Goals (MVP)
- Full-featured consumer mobile apps (iOS/Android) beyond WhatsApp.
- In-app payments and escrow at launch (plan for future phases).
- Complex pricing/quotations; MVP supports fixed/indicative pricing then offline confirmation.
- Full-blown technician marketplace growth tooling (ad campaigns, etc.).
 - Monetization live at beta: technician credits planned but disabled during test/beta; no client charges initially.

## 3) Target Users and Personas

- Client (Requester): Any person needing a service (e.g., “Sink is clogged”). Values speed, reliability, clear pricing.
- Technician / Service Provider: Vetted professionals with known service areas, skills, and availability. Values job volume, fair pricing, low no-show rate. Interacts mainly via WhatsApp.
- Operator (Support): Handles escalations, disputes, manual matches, and quality control.
- Admin (Internal): Manages catalog, technician onboarding, quality, analytics.

## 4) Key Use Cases

- UC1: Client sends a WhatsApp message describing a need (e.g., “Water in my kitchen sink does not go” or “I need help setting up my Wi‑Fi”).
- UC2: AI agent clarifies: location, urgency, access time, constraints, images/videos if helpful.
- UC3: System finds suitable technicians and proposes 1–3 options; client picks one.
- UC4: Booking is created; both parties get confirmations and reminders in WhatsApp. Operator can intervene.
- UC5: Post-service feedback collected; ratings update technician reputation.
- UC6: Technician/provider onboarding: KYC, skills, service areas, preferred schedule, pricing. Entirely via WhatsApp or a lightweight link flow.
- UC7: Technician/provider accepts/declines offers via WhatsApp; limited client-provider mediated chat if needed (with operator override).
- UC8: Operator tools: search requests, reassign technicians, message templates, status changes.

## 5) Scope (MVP vs. Next)

MVP
- WhatsApp conversational flow (inbound, templates for outbound when needed).
- AI agent for intent detection, slot-filling, and summarization of requirements.
- Provider catalog & matching engine (scoring by distance, availability, rating, price fit).
- Booking lifecycle: propose → confirm → remind → complete → rate.
- Basic media handling (client can send images/videos; stored securely; technician can receive link/previews).
- Technician/provider-side WhatsApp interactions: receive/propose, accept/decline, arrival/complete toggles.
- Operator console (lean) or simple back office with spreadsheet export if needed.

Next
- Payments integration (mobile money/Stripe/Paystack) with optional deposit/escrow.
- Dynamic pricing/quotation, multi-offer negotiation, and upsells.
- SLA guarantees, insurance, dispute workflows.
- Growth loops: referrals, loyalty, re-engagement.
 - Monetization: technician credit purchases, billing/reconciliation, adjustable credit burn rules.

## 6) Assumptions & Constraints

- WhatsApp Business API/Cloud API is permitted and templates adhere to Meta policies.
- Geography focus: initial city/region with high provider density; service expansion later.
- Languages: English + French (and local language variants as feasible) with runtime detection.
- Accurate location sharing via WhatsApp location or address text plus geocoding.
- MVP runs on a reliable cloud platform (e.g., Heroku) with Postgres; media storage on S3-compatible storage.

## 7) Functional Requirements

7.1 WhatsApp Entry Points
- Support wa.me link, QR code, and saved contact inbound.
- Auto-replies during off-hours with template guiding to leave details.
- Template requirements: approved categories for notifications (booking confirmation, reminder, completion).

7.2 Conversation & AI Agent
- Detect service intent from free text; classify into catalog category/subcategory.
- Slot collection: address/location, preferred time window, urgency, budget range, property type, access notes, media.
- Confirmation: summarize understanding and ask client to confirm or edit.
- Proposal: present 1–3 providers with name (or anonymized alias), ETA, price/price range, rating, and distance.
- Selection & booking: allow quick selection, reschedule, or ask for alternates.
- Fallback: if AI confidence low, request human operator or ask clarifying questions.
- Handoff: operator can jump in; agent pauses automatically.

7.3 Catalog & Metadata
- Service categories (e.g., Plumbing → Clogged sink, Leak repair, Installation).
- Each subcategory defines standard slots to collect and recommended add-on questions.
- Provider skill tags mapped to subcategories; minimum skill threshold required.

7.4 Technician/Provider Onboarding
- KYC and verification (ID, phone, references where applicable).
- Profile: skills, years of experience, service areas (polygons or radius), base pricing, availability schedule, max jobs per day.
- Device and WhatsApp number for notifications; opt-in to receive job pings.
- WhatsApp-based flows to accept terms, set availability, toggle online/offline, and respond to offers.

7.5 Matching Engine
- Inputs: required skills, location, requested time, urgency, budget, ratings, historical reliability, active jobs.
- Scoring: weighted sum with tunable weights; tie-breaker by proximity and reliability.
- Hard constraints: must be available, in service area, pass vetting.
- Fallback tiers: expand radius, flex time window, lower rating threshold (with client disclosure), or escalate to operator.

7.6 Booking Lifecycle
- States: Draft → Proposed → ClientSelected → TechnicianAccepted → Confirmed → InProgress → Completed → Cancelled → Failed.
- Notifications: WhatsApp messages to client and technician at key transitions (with approved templates when required).
- Reschedule/cancel rules and penalties (MVP: simple; document policy in templates).

7.7 Media Handling
- Client can send images/videos. System stores and shares controlled links to technician.
- Virus scanning and size/type validation. Redact PII from filenames.

7.8 Ratings & Feedback
- 1–5 star rating + free text from client post-service. Optional tip note for future payments integration.
- Aggregate rating with recency weighting; visible to matching engine.

7.9 Operator/Admin Tools (Lean)
- Search service requests by status, phone, location, technician.
- Force assign/replace technician; pause/close requests.
- Message snippets/templates for common replies.
- Export CSV for accounting and quality.

7.10 Technician/Provider–Client Interaction (WhatsApp)
- Offer receipt and accept/decline via quick-reply buttons or numbered replies.
- Arrival and completion toggles via WhatsApp (buttons or keywords).
- Optional proxied messaging between client and provider for logistics; messages logged in conversation history and can be muted by operator.

## 8) Non‑Functional Requirements

- Reliability: 99.5% monthly uptime for conversational backend; queueing for transient failures.
- Performance: P95 messaging round-trip < 2s server-side; LLM response < 4s average for standard prompts.
- Security: Encrypt PII at rest and in transit; enforce scoped access; audit trails.
- Privacy: Data minimization; retention policy (e.g., conversations 12 months, media 6 months unless required longer).
- Compliance: Meta WhatsApp policies, local consumer protection laws, and basic KYC standards for providers.
- Observability: Structured logs, traces, metrics (success rates, matching accuracy, time to match, drop-offs).
 - Billing integrity (post-beta): accurate credit accounting and idempotent ledger writes; reconciliation jobs.

## 9) AI/Agent Design

- NLU & Orchestration: Intent classification + slot filling with an LLM; deterministic tool calls (geocode, match).
- Guardrails: JSON schema outputs for slots; content moderation for unsafe requests; policy hints for pricing claims.
- Retrieval: Catalog and city-specific knowledge (e.g., typical plumbing issues) via lightweight vector or keyword retrieval.
- Prompting: System prompt sets persona, scope, disallowed promises; few-shot examples per service category.
- Confidence: If classification confidence < threshold, ask clarifying questions or route to operator.
- Localization: Multilingual prompts, locale-aware formatting; fail-safe to English.
- Cost & Latency: Use small/fast model for classification; escalate to larger model for complex clarifications.

Provider-side Agent Considerations
- Keep provider prompts short and action-oriented (accept/decline, propose alternate time).
- Respect do-not-disturb and availability windows; avoid over-pinging.

## 10) System Architecture (High-Level)

Components
- WhatsApp Gateway: Webhook receiver + template sender (Meta Cloud API) for both client and provider interactions.
- Conversation Service: Manages sessions, state, and agent orchestration.
- Matching Service: Scores technicians and returns ranked list.
- Scheduler/Notifications: Reminders and status updates.
- Back Office: Minimal operator UI/API.
- Data: Postgres (core), Object storage (media), Redis (cache/queues), Geocoding (Google/OSM), Maps/distance matrix.
- Deployment: Containerized app on Heroku; Procfile-driven; autoscaling enabled.

Data Flow
1) WA message → Webhook → Conversation Service → Agent (slots) → Tools (geocode, catalog) → Matching Service → Proposals → WA reply.
2) Client confirms → Booking stored → Provider notified → Accept/decline via WhatsApp → Confirmed → Reminders → Completion → Rating.

Monetization (Planned; Beta Disabled)
- Technician/provider buys credits in-app (link) or externally; credits are consumed per defined interaction event (TBD: e.g., receiving an offer, accepting a job, client contact reveal, or successful completion). No client charges.
- During test/beta: no fees; credits system disabled or credits granted freely for experimentation.
- Post-beta: credit packages, burn rules, caps, and promotions.

## 11) Data Model (MVP, conceptual)

- User(id, phone, role[client|technician|operator], locale, wa_opt_in, created_at)
- Technician(id, user_id, kyc_status, skills[], service_area, base_price, rating, jobs_completed, reliability_score)
- ServiceCategory(id, name, parent_id, slot_schema, prompts)
- ServiceRequest(id, client_id, category_id, description, slots(json), media[], location(geo), status, created_at)
- Offer(id, request_id, technician_id, score, price_estimate, eta, expires_at)
- Booking(id, request_id, technician_id, scheduled_time, state, notes)
- Message(id, request_id, from[user|system|tech|operator], channel, body, media, direction[in|out], created_at)
- Rating(id, booking_id, score, comment, created_at)
- AuditLog(id, actor, action, entity, details, created_at)

Monetization Entities (Post-Beta)
- CreditWallet(id, technician_id, balance, currency, created_at)
- CreditTransaction(id, wallet_id, type[debit|credit], reason[offer|accept|contact_reveal|completion|adjustment], amount, reference, created_at)
- TariffRule(id, reason, price_per_event, city, service_category, effective_from, effective_to)

## 12) Key APIs (Internal)

- POST /webhook/whatsapp → inbound messages
- POST /agent/reply → returns reply segments + next state
- POST /match → body: { request_id } → returns ranked offers
- POST /booking/{id}/confirm | /cancel | /reschedule
- GET /requests?filters… | GET /bookings/{id}
- POST /operator/assign → body: { request_id, technician_id }
 - POST /provider/availability/toggle → body: { technician_id, online }
 - POST /provider/accept → body: { offer_id }

## 13) Conversation Flows (Happy Path)

Example: “Water in my kitchen sink does not go.”
1) Greet + understand: Detect Plumbing → Clogged sink.
2) Ask: “Where is this? Share location or type address.”
3) Ask: “When can someone come? Today within 2–4 hours or later?”
4) Optional: “A quick photo/video helps.”
5) Summarize: “Clogged kitchen sink, today afternoon, location X. OK to proceed?”
6) Propose: “I found 2 plumbers nearby: A (15 min away, 4.7★, from 10k) and B (25 min, 4.6★, from 9k). Which should I book?”
7) Confirm booking → notifications sent.
8) Post-service → ask for rating.

Provider Flow (WhatsApp)
1) Receive offer: “Job near you: Clogged sink at X, today 4–6pm. Estimated payout Y. Reply 1 to accept, 2 to decline.”
2) Provider replies 1 → state moves to TechnicianAccepted; client notified.
3) Before arrival, provider can toggle “On my way” → arrival ETA to client.
4) After completion, provider marks “Complete” → triggers client rating.

Edge Cases
- Ambiguous request → ask clarifying questions.
- No technicians available → offer alternate time, expand radius, or waitlist + operator.
- Technician decline/no-show → re-match with priority; notify client.
- Off-hours → collect details, promise follow-up window.

## 14) Matching Algorithm (Initial)

Score = w1*distance_score + w2*availability_score + w3*rating_score + w4*price_fit + w5*reliability
- distance_score: inverse of km; 0 outside max radius.
- availability_score: binary for requested slot; partial for near slots.
- rating_score: normalized 0–1 with recency.
- price_fit: 1 if within client budget; tapered outside.
- reliability: declines with recent cancellations/no-shows.
Constraints: vetted, skill match, capacity not exceeded.

## 15) Compliance, Trust & Safety

- WhatsApp: template categories, opt-in, 24-hour session rules.
- PII: phone and address treated as sensitive; access logged and restricted.
- Content moderation: detect violent/illegal/off-policy requests; safe declines or operator review.
- Disputes: operator mediation; document process for refunds (future when payments added).

## 16) Analytics & KPIs

- Time to First Response (TTFR)
- Match Rate (requests with ≥1 proposal)
- Time to Confirmed Booking
- Completion Rate and On-Time Arrival
- CSAT/NPS; 1–5 star average
- Technician Acceptance Rate and No-Show Rate
- Re-engagement Rate (repeat clients)
- Cost per Conversation and per Booking
 - Post-beta monetization: credit burn per active provider, offer→accept conversion cost, revenue retention per cohort

## 17) Milestones & Timeline (Indicative)

Phase 0 (2–3 weeks)
- WA Business setup, webhook, hello world. Minimal catalog, 10 vetted technicians.
- Basic agent with intent + slots for top 3 categories.

Phase 1 (3–5 weeks)
- Matching engine v1, booking states, operator tools, reminders.
- Ratings, media handling, Spanish/French/English or locale of focus.

 Phase 2 (4–6 weeks)
 - Payments pilot (mobile money), deposit option, dispute basics.
 - SLA tiering, improved reliability scoring, growth loops.
 - Monetization scaffolding (credit wallet + ledger + admin pricing), initially off in beta.

## 18) Risks & Mitigations

- Supply scarcity in peak times → waitlist, incentives, surge pricing (later), operator fallback.
- Address accuracy → push for live location + geocode validation; technician call pre-dispatch.
- LLM hallucinations → constrained prompts, function-calling, explicit disclaimers.
- WhatsApp template rejections → pre-approval cycles; backup templates; clean wording.
- No-shows → reliability score, penalties, quick re-match.
- Fraud → KYC, anomaly detection, restricted media links.

## 19) Acceptance Criteria (MVP)

- From a cold WhatsApp start, a client can complete a booking in ≤ 6 conversational turns median.
- ≥ 90% of Plumbing/Electricity requests correctly classified into the right subcategory.
- ≥ 80% of requests get ≥ 1 proposal within 2 minutes.
- ≥ 70% technician acceptance rate in first city.
- P95 server round-trip under 2 seconds (excluding LLM); P95 end-to-end proposal under 15 seconds.
- Operator can reassign a job and notify both parties in < 60 seconds.

## 20) Open Questions

- Which city/country first? Impacts payments, languages, compliance, and technician supply.
- Payment method priority (Wave/Orange Money/Paystack/Stripe?) and fee structure.
- Pricing model: fixed per category vs. range + on-site confirmation.
- Technician incentives and retention plan.
- SLA/guarantee level for early cohorts.
 - Monetization details: define "interaction" for credit burn (offer receipt, accept, contact reveal, completion?), pricing per event, free tier caps during beta.

## 21) Appendix: WhatsApp Notes

- Use session messages for conversational flow; use pre-approved templates for outside 24-hour window notifications (confirmations, reminders).
- Templates must not be promotional for utility category; keep neutral, clear, and localized.
- Media size and format limits; compress images server-side when relaying.
 - Maintain separate, concise templates for provider flows (offer, accept confirm, on-my-way, completion) and for client flows (proposal, confirm, reminder, completion, rating).
