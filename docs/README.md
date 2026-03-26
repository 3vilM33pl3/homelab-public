# Documentation Index

This public documentation focuses on trust boundaries, operating assumptions, and the controls that back up the repo’s claims.

## Start Here

- `../README.md`: scope, rebuild flow, and validation checklist
- `security/threat-model.md`: assumptions, trust boundaries, and operator model
- `security/secrets.md`: secret-handling, state sensitivity, and publication controls
- `../iac_ansible/README.md`: host automation patterns
- `../iac_terraform/README.md`: cluster resource patterns
- `../monitoring/README.md`: monitoring and ingress example

## Principle To Control Mapping

| Principle | Enforced by |
| --- | --- |
| Network location is not enough to earn trust | WireGuard admin path, mTLS example, explicit trust-boundary docs |
| Private PKI is part of routine operations | CA host model, trust-root distribution in Ansible, Caddy internal ACME example |
| Secrets are encrypted or injected, not embedded | `docs/security/secrets.md`, Terraform secret reference pattern, export denylist scan |
| Public examples must not leak private topology | `tools/export-public-homelab.py`, denylist scan, fixture tests, manual review gate |

## Trust Boundaries

- Remote operator to edge host: authenticated over WireGuard, then authorized per service.
- Edge host to internal services: TLS terminates explicitly, not implicitly through network location.
- CA host to managed nodes: trust-root distribution is deliberate and auditable.
- Public repo to private source of truth: one-way export plus denylist enforcement; no reverse sync.
