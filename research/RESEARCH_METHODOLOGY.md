# Research Methodology for Gemini Enterprise Connector POC

This methodology governs all research, documentation, and architectural design for the Gemini Enterprise Connector POC project. It ensures high quality, accuracy, and traceability.

## 1. Primary Source Hierarchy
Use sources in the following strict order of precedence:
1. Official Google Cloud / Gemini Enterprise documentation
2. Official Google API/reference documentation
3. Official Google release notes
4. Official Google Cloud blogs / announcements
5. Official third-party vendor documentation
6. Technical articles/blogs
7. GitHub issues/discussions
8. Reddit / X / community discussions

## 2. Fact vs Interpretation
Every important claim must be explicitly classified as:
- **FACT:** Directly supported by a primary source.
- **INFERENCE:** Derived from documented behavior; the reasoning must be explained.
- **COMMUNITY REPORT:** Reported by users, not independently verified.
- **OPEN QUESTION:** Documentation is insufficient or contradictory.

## 3. Currentness
Since Gemini Enterprise evolves rapidly:
- Record source publication/update date when available.
- Record product status (e.g., GA, Preview, Private Preview, deprecated).
- Prefer current documentation over older blog posts.
- Explicitly flag potentially outdated information.

## 4. No Assumptions from API Enums
Do not infer that the existence of an API enum, field, connector type, or internal resource automatically means a customer can configure or implement that capability. Require customer-facing documentation or reproducible evidence.

## 5. Connector-Specific Behavior
Never generalize behavior from one connector to all connectors. Record connector-specific limitations separately.

## 6. Evidence
Every important architectural or security claim must have:
- Source URL
- Exact relevant section/page
- Short evidence summary
- Confidence level (e.g., High, Medium, Low)

## 7. Conflicting Sources
When sources disagree:
- Do not silently choose one.
- Identify the conflict.
- Prefer newer authoritative documentation.
- Record the unresolved issue in `open_questions.md`.

## 8. Architecture
For every architecture, explicitly capture:
- Components
- Request/data flow
- Where data resides
- Authentication
- Identity propagation
- Authorization / ACL enforcement
- Synchronization/freshness
- Failure points
- Networking
- Operational responsibilities

## 9. Demo vs Production
Clearly distinguish:
- What we can realistically demonstrate in the POC.
- What is production architecture.
- What is only conceptual because the required capability is unavailable in the current environment.

## 10. Open Questions
Maintain a running list of questions in `research/open_questions.md`. Never fill an unresolved question with a guess.

## 11. Traceability
Each conclusion in the final architecture presentation must be traceable back to the research documents, and ultimately to its source evidence in the `EVIDENCE_INDEX.md`.

## 12. Research Output Format
Each research document should follow this structure:
- Scope
- Executive summary
- Current documented behavior
- Architecture
- Authentication / identity
- ACL / authorization
- Operational considerations
- Limitations
- Evidence table
- Open questions
