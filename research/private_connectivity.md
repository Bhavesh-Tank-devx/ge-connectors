# Networking & Private Connectivity

## 1. What network architecture is required for private/self-hosted systems?
**FACT**: Gemini Enterprise supports accessing private on-premise or VPC-enclosed data via VPC Service Controls (VPC-SC) ingress restrictions.

*Source: https://cloud.google.com/vpc-service-controls/docs/supported-products*

## 2. Tenant Isolation
**FACT**: Dedicated Data Stores and separated IAM configurations are the standard GCP methods for multi-tenant isolation at the infrastructure level.

## 3. Advanced Networking for Private Connectivity (VPC-SC & PSC)
**FACT**: Federated Custom MCP Servers hosted on Cloud Run can use **Direct VPC Egress** (`vpc-egress=private-ranges-only`) to route traffic straight into customer VPC subnets, crossing into on-premises infrastructure via Cloud Interconnect or HA VPN.
**FACT**: Enabling a VPC Service Controls (VPC-SC) perimeter around `discoveryengine.googleapis.com` blocks public ingress/egress. If a project already has Data Stores, they must be deleted and recreated *after* the perimeter is established.

## 4. Egress Security and Agent Gateway
**FACT**: By default, outbound traffic to Custom MCP servers does *not* route through Agent Gateway. Centralized egress proxying must be explicitly configured in the Advanced Options. Standard Cloud Run egress (`vpc-egress=private-ranges-only`) is used to route traffic straight into customer VPC subnets.
