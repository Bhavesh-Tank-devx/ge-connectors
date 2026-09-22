import re

with open('research/private_connectivity.md', 'r') as f:
    content = f.read()

# Fix Section 1
content = re.sub(
    r"\*\*OPEN QUESTION\*\*: Documentation for explicit egress via Private Service Connect \(PSC\) for Custom MCP servers remains sparse\.",
    r"",
    content
)

# Fix Section 3
content = re.sub(
    r"\*\*FACT\*\*: When connecting to private on-premises backend APIs, Gemini Enterprise utilizes Private Service Connect \(PSC\) bound to a Service Directory resource `projects/\*/locations/\*/namespaces/\*/services/\*`\. \n",
    r"",
    content
)

# Fix Section 4
content = re.sub(
    r"\*\*FACT\*\*: The Agent Gateway proxies all outbound traffic and explicitly enforces Agent Registry allowlists\. SSRF vulnerabilities \(like accessing internal `169\.254\.169\.254` metadata IPs\) are structurally mitigated by Gateway domain allowlisting and HTTP client restrictions\.",
    r"**FACT**: By default, outbound traffic to Custom MCP servers does *not* route through Agent Gateway. Centralized egress proxying must be explicitly configured in the Advanced Options. Standard Cloud Run egress (`vpc-egress=private-ranges-only`) is used to route traffic straight into customer VPC subnets.",
    content
)

with open('research/private_connectivity.md', 'w') as f:
    f.write(content)
print("Updated private_connectivity.md")
