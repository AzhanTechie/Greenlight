# Greenlight

**Greenlight** is a pre-publication brand governance tool. Creators paste draft content, the system checks it against an approved brand knowledge base (guideline rules, approved facts, and terms), and returns explained, cited findings. Every finding is either tied to a verified rule/fact or clearly labeled "Unverified." The AI never auto-applies changes — it only suggests; a human always decides.

Built for CodeStar 30 (Round 2 — The Build), by team MEGA SMASHERS (solo: Mohammed Azhan Tehami), for the problem statement by Inkloom AI.

## Core workflow

1. **Creator** pastes a draft on the Draft page and runs a review.
2. The system retrieves relevant rules/facts/terms and sends the draft to Google Gemini for analysis.
3. The AI returns findings (quote, category, severity, explanation, suggested minimal fix).
4. The system verifies every finding: the quoted text must exist in the draft, and any cited rule/fact ID must exist in the knowledge base. Claims with no matching approved fact are explicitly marked "Unverified."
5. On the **Findings** page, the Creator can Accept, Edit, or Dismiss each finding, then submit the draft for review.
6. On the **Reviewer** page, a Reviewer sees submitted drafts, findings, and decisions, can leave comments, and can Approve or Request Changes.
7. On the **Insights** page, a Manager can see aggregate stats: findings by category/severity/status, most triggered rules, most dismissed rules, and count of unverified claims.
8. On the **Admin** page, a Brand Admin can view and add guideline rules, approved facts, and terms.

## Features completed (Round 2)

- F1 — Brand knowledge base (rules, facts, terms with IDs), viewable and editable via Admin page
- F2 — AI-powered text review engine (tone, terminology, factual consistency, unsupported claims)
- F3 — Explainable, verified findings (quote + reason + severity + cited source; code-verified; unverifiable claims explicitly labeled)
- F4 — Accept / Edit / Dismiss suggestions (AI never auto-applies changes)
- F5 — Reviewer approval workflow (comments, approve, request changes, audit log)
- F6 — Basic insights dashboard (issue categories, severities, most triggered/dismissed rules, unverified claim count)

## Tech stack

- **Frontend/app:** Streamlit (Python)
- **Database:** Supabase (Postgres)
- **AI model:** Google Gemini API (`google-generativeai`)
- **Validation:** Pydantic
- **Data handling:** Pandas

## Known limitations (to be addressed in future rounds)

- No real authentication — roles are selected manually via a dropdown for demo purposes; Row Level Security is disabled on all tables for the MVP.
- Single draft/version flow; no concurrent multi-user conflict handling yet.
- Gemini free tier has a 5-requests-per-minute rate limit, which may cause brief delays under heavy testing.

## Planned for Round 3

1. Document review — upload .docx/.pdf/.txt files and map findings to their exact location in the document.
2. Image and accessibility checks — alt text, color contrast, logo/asset rule compliance.
3. Guideline-gap insights — detect rules that are frequently dismissed/overridden or low-confidence, and recommend brand admins clarify them.

## Running locally

1. Clone this repository.
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Create a `.streamlit/secrets.toml` file with your own `SUPABASE_URL`, `SUPABASE_KEY`, and `GEMINI_API_KEY`.
4. Run: `streamlit run app.py`

## Disclosures

This project uses Google Gemini (generative AI) for review analysis, Supabase for data storage, and Streamlit for the application framework/UI.