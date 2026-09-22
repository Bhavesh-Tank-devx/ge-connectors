import re

with open('research/security_failure_modes.md', 'r') as f:
    content = f.read()

# Fix Section 4
content = re.sub(
    r"\*\*FACT\*\*: Gemini Enterprise Agents operate using short-lived SPIFFE identities. Outbound token theft is neutralized via \*\*DPoP \(Demonstrating Proof of Possession - RFC 9449\)\*\*, cryptographically binding the token to a private key in the agent runtime\. Replaying an intercepted bearer token from an attacker's machine will fail\.",
    r"**FACT**: The Agent Runtime authenticates to custom MCP servers via Google-signed OIDC ID tokens (`X-Serverless-Authorization`) protecting against direct token replay outside of Cloud Run IAM.",
    content
)

# Fix Section 5
content = re.sub(
    r"\*\*FACT\*\*: The system utilizes \*\*Model Armor\*\* for inline prompt-injection screening \(up to 65,536 tokens\)\.",
    r"**FACT**: Google Cloud provides **Model Armor** for pre- and post-inference screening, but it is a separate service.",
    content
)

with open('research/security_failure_modes.md', 'w') as f:
    f.write(content)
print("Updated security_failure_modes.md")
