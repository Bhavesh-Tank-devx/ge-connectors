import re

with open('research/native_connectors.md', 'r') as f:
    content = f.read()

# Fix Section 5
content = re.sub(
    r"While the API exposes `ConnectorMode` enums for `DATA_INGESTION`, `ACTIONS`, and `END_USER_AUTHENTICATION`",
    r"The API exposes `ConnectorMode` enums for `DATA_INGESTION`, `FEDERATED`, `ACTIONS`, `EUA`, and `FEDERATED_AND_EUA`. While historically biased toward ingestion",
    content
)

# Fix Section 6 Table
content = re.sub(r"\| \*\*Jira \(Cloud/DC\)\*\* \| Ingestion \| Search \|", r"| **Jira (Cloud)** | Ingestion & Fed | Search & Actions |", content)
content = re.sub(r"\| \*\*Salesforce\*\* \| Ingestion \| Search \|", r"| **Salesforce** | Ingestion & Fed | Search |", content)

# Fix Section 9
content = re.sub(
    r"Native Data Connectors are overwhelmingly \*\*Search only\*\* \(read-only\)\. To perform actions/mutations, developers must use separate components",
    r"Historically Native Data Connectors were **Search only** (read-only), but Jira Cloud and Microsoft Connectors now natively support **Actions** (Preview). For other read-only connectors, developers must use Custom MCP servers",
    content
)

# Fix Section 15
content = re.sub(
    r"- \*\*Verdict:\*\* \*\*CONTRADICTED\*\*\. The Connector Catalog and Official Docs researchers confirmed that native third-party connectors \(Jira, Salesforce, Confluence\) default to \*\*Ingestion \(Indexing\)\*\*\. Native live federation for these systems requires separate Extensions or MCPs\.",
    r"- **Verdict:** **PARTIALLY CONTRADICTED**. Jira Cloud and Salesforce actually *do* support both Ingestion and Federation natively. However, Confluence, SharePoint, and Google Drive default strictly to **Ingestion (Indexing)** and do not natively support federation.",
    content
)

with open('research/native_connectors.md', 'w') as f:
    f.write(content)
print("Updated native_connectors.md")
