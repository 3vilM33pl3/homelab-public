# CA Host Automation

The private homelab keeps the certificate authority on a dedicated host. The public version keeps only the operating model.

## Why Separate The CA

- certificate issuance stays isolated from general workloads
- trust-root distribution is explicit and auditable
- recovery steps can be reasoned about independently from the cluster

## Operating Modes

- Converge mode: update packages, policies, and service configuration without replacing key material.
- Bootstrap mode: restore CA material from a private secret store during first setup or disaster recovery.

## Managed Concerns

- `step-ca` and `step-cli` installation
- public distribution of the trust root
- ACME for internal reverse proxies
- a locked-down firewall posture for the CA host
- optional SSH certificate issuance for administrators and nodes

## Public Guidance

- keep issuing keys private
- automate root distribution but not root-key exposure
- prefer short-lived leaf certificates over long-lived static cert files
- treat CA bootstrap as a recovery workflow, not a routine change path
