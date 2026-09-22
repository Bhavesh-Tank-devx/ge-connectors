# Gemini Enterprise Data Connectivity Master Summary

This document synthesizes all validated research regarding Gemini Enterprise Data Connectors.

## Architectural Planes
1. **Ingestion (Indexed Search)**: Best for documents. High availability, bounded freshness. Server-side ACL enforcement.
2. **Federation (Delegated Search)**: Best for remote enterprise search engines (Drive, Jira). Zero duplication.
3. **Custom MCP (Live Tooling)**: Best for transactional APIs, mutations, and strict zero-trust boundary wrapping of legacy APIs (like Razorpay).

## Validation of ADR-001 (Razorpay)
The original ADR correctly identified that custom middleware (Option C/D) was required. However, it falsely classified "Federation" as the broadly available mode for generic APIs. **Custom MCP (Public Preview)** is the correct architectural path for wrapping an org-level API key with per-user OIDC validation.

## Red Team Clarification (Razorpay)
**IMPORTANT**: The mapping of the OAuth identity to the Razorpay org-level API key is *not* a built-in platform feature. Gemini Enterprise natively forwards the user's OAuth token. The mapping to `employee_id` and the secure injection of the org-key is executed exclusively by the custom middleware logic hosted inside the Cloud Run MCP Server.
