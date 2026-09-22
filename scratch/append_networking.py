import os

private_connectivity_updates = """
## 3. Advanced Networking for Private Connectivity (VPC-SC & PSC)
**FACT**: When connecting to private on-premises backend APIs, Gemini Enterprise utilizes Private Service Connect (PSC) bound to a Service Directory resource `projects/*/locations/*/namespaces/*/services/*`. 
**FACT**: Federated Custom MCP Servers hosted on Cloud Run can use **Direct VPC Egress** (`vpc-egress=private-ranges-only`) to route traffic straight into customer VPC subnets, crossing into on-premises infrastructure via Cloud Interconnect or HA VPN.
**FACT**: Enabling a VPC Service Controls (VPC-SC) perimeter around `discoveryengine.googleapis.com` blocks public ingress/egress. If a project already has Data Stores, they must be deleted and recreated *after* the perimeter is established.

## 4. Egress Security and Agent Gateway
**FACT**: The Agent Gateway proxies all outbound traffic and explicitly enforces Agent Registry allowlists. SSRF vulnerabilities (like accessing internal `169.254.169.254` metadata IPs) are structurally mitigated by Gateway domain allowlisting and HTTP client restrictions.
"""

with open('research/private_connectivity.md', 'a') as f:
    f.write(private_connectivity_updates)

security_failure_updates = """
## 4. Agent Identity and Token Forgery Protection
**FACT**: Gemini Enterprise Agents operate using short-lived SPIFFE identities. Outbound token theft is neutralized via **DPoP (Demonstrating Proof of Possession - RFC 9449)**, cryptographically binding the token to a private key in the agent runtime. Replaying an intercepted bearer token from an attacker's machine will fail.

## 5. Defense against Direct & Indirect Prompt Injection
**FACT**: The system utilizes **Model Armor** for inline prompt-injection screening (up to 65,536 tokens). 
**INFERENCE**: The ultimate defense against prompt injection remains the Data-Layer Non-Bypassable Principle: Data access is filtered server-side (Ingestion) or via middleware OIDC verification (Custom MCP). Unauthorized data is physically never placed into the LLM context window, making it impossible for a compromised LLM to leak it.

## 6. Grounding Validation
**FACT**: The `Check Grounding API` verifies factual consistency between the generated response and the retrieved context chunks. Malicious or hallucinated payloads result in low grounding scores and system fallback warnings.
"""

with open('research/security_failure_modes.md', 'a') as f:
    f.write(security_failure_updates)

# Appending uniquely numbered evidence from networking subagent
new_evidence = """| EVI-026 | `discoveryengine.googleapis.com` is a supported service for VPC Service Controls. Existing data stores must be recreated when applying perimeters. | FACT | https://cloud.google.com/vpc-service-controls/docs/supported-products |
| EVI-027 | Cloud Run supports Direct VPC Egress without Serverless VPC Access connectors (up to 1 Gbps/instance). | FACT | https://cloud.google.com/run/docs/configuring/vpc-direct-vpc |
| EVI-028 | Agent Gateway secures outbound traffic against Agent Registry allowlists and IAM policies. | FACT | https://cloud.google.com/agent-gateway/docs |
| EVI-029 | Agent Identity provisions short-lived SPIFFE IDs and X.509 certs, using mTLS and RFC 9449 DPoP. | FACT | https://datatracker.ietf.org/doc/html/rfc9449 |
| EVI-030 | Model Armor provides pre- and post-inference screening up to 65,536 tokens for prompt injection and jailbreaks. | FACT | https://cloud.google.com/security/products/model-armor |
| EVI-031 | The Check Grounding API validates factual support scores between generated text and retrieved chunks. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/check-grounding |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Networking and Security Evidence updated successfully.")
