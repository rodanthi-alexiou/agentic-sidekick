---
artifact: requirements
engagement: "Moda-Iberica-Shopping-Assistant"
customer: "Moda Ibérica"
captured_by: "[TBD — partner name]"
captured_on: "2026-05-27"
status: draft
---

# Requirements — Moda Ibérica

## 1. Business context
- **Industry:** Fashion retail (mid-market; physical stores + e-commerce)
- **Business outcome (one sentence):** Build a conversational "Shopping Assistant" for web/mobile and in-store tablets to help customers/associates discover products, get outfit recommendations, check store stock, and answer common service questions (returns, sizing, promotions).
- **Success metrics (6-month):**
  - 15% lift in online conversion for sessions that engage the assistant
  - 25% deflection of "where is my order" and "return policy" contacts from the call center (baseline: ~40K tickets/month)
  - Store associates rate it ≥4/5 on usefulness after 30 days
- **Sponsor / decision maker:** Chief Digital Officer (CDO), Elena Vargas
- **Budget owner:** [TBD — ask customer]
- **Year-one budget (build + run):** €600K (board approved)

## 2. Users and usage
- **Primary persona(s):**
  - Online customers (website + mobile app)
  - Store associates (tablets) supporting in-store customers
- **Concurrent users at peak:** ~2,000 (Black Friday estimate); typical 200–300
- **Geographic distribution:** Primarily Spain and Portugal
- **Channel:** Web + mobile app + in-store tablets
- **Languages:** Spanish, Catalan, Portuguese

## 3. AI capabilities needed
- **Pattern hypothesis:** [TBD — ask customer: confirm primary intent (RAG vs agentic actions) and any phased rollout]
- **Models customer asked for:** "GPT-5" (as stated by customer)
- **Core capabilities (as stated):**
  - Conversational product discovery and Q&A
  - Outfit recommendations
  - Answer questions about returns, sizing, and current promotions
  - "Where is my order" support (order status)
- **Additional capability request:** Generate product descriptions for new SKUs (to reduce copywriter workload)
- **Tools/actions the AI needs (systems to integrate):**
  - Product catalog lookup (SAP Commerce Cloud)
  - Real-time inventory per store (OMS REST API)
  - Order history and customer profile lookup (Salesforce Service Cloud)
  - Marketing content / campaign assets (SharePoint site)

## 4. Data
- **Sources (system, format, volume, classification per source):**
  - Product catalog: SAP Commerce Cloud; ~85,000 SKUs; updated nightly; classification [TBD — ask customer]
  - Inventory per store: OMS REST API; real-time; classification [TBD — ask customer]
  - Order history + customer profile: Salesforce Service Cloud; includes customer PII; classification confidential/regulated (GDPR)
  - Marketing content + campaign assets: SharePoint site; classification [TBD — ask customer]
  - Merchandising "style guide": PDF; ~200 pages; updated quarterly; classification [TBD — ask customer]
- **Update frequency:**
  - Catalog: nightly
  - Inventory: real-time
  - Style guide: quarterly
  - Other sources: [TBD — ask customer]
- **Sovereignty / residency:** Customer PII cannot leave the EU
- **Sensitivity:** Includes PII (GDPR); overall classification scheme [TBD — ask customer]
- **Retention and right-to-be-forgotten:** [TBD — ask customer]

## 5. Non-functional requirements
- **Latency target:** [TBD — ask customer: p50/p95 for chat responses and for transactional lookups]
- **Availability SLA:** [TBD — ask customer]
- **Throughput at peak:** [TBD — ask customer: expected chats/sec, tokens/min, and peak hours profile]
- **Cost ceiling (monthly):** [TBD — ask customer] (note: year-one budget stated as €600K)

## 6. Security, compliance, governance
- **Compliance scopes:** GDPR; Spanish LOPDGDD; DORA readiness work in progress
- **Identity provider:** [TBD — ask customer] (separate needs likely for customers vs store associates)
- **Network constraints:** [TBD — ask customer] (e.g., private endpoints only, no public endpoints, ExpressRoute, hub-spoke)
- **Existing CAF Platform Landing Zone:** No (Azure tenant exists but only dev subscriptions; "nothing serious")
- **Approved Azure regions:** [TBD — ask customer] (constraint stated: EU-only for PII)
- **Procurement / licensing:** Not yet engaged on model licensing

## 7. Delivery preferences
- **IaC tool:** [TBD — ask customer]
- **Source control:** Mixed today: Azure DevOps (commerce platform) and GitHub (data team)
- **CI/CD platform:** [TBD — ask customer]
- **Existing AI assets to reuse:** [TBD — ask customer]
- **Target environments:** [TBD — ask customer] (dev/test/prod and any pilot/staging needs)

## 8. Constraints and known unknowns
- **Hard deadlines:** Production by Oct 2026 to support Black Friday / Christmas 2026 peak; pilot live before peak season
- **Existing vendor lock-ins:** SAP Commerce Cloud; Salesforce Service Cloud; OMS (REST API); SharePoint
- **Explicit "do not want":** [TBD — ask customer]
- **Open questions from partner:**
  - "Should we just buy Copilot Studio? Why would we build this?" (IT lead)
  - Model choice and licensing approach (procurement not started)
  - EU-only handling of customer PII (CISO requirement)

---

## Intake summary (filled by Requirements agent at close)

- **Sections complete:** [TBD] / 8
- **Sections [TBD]:** [TBD]
- **Biggest gap blocking architecture work:** [TBD]
- **Ready for Challenger:** no
