# Threat Model

## Assumptions

- There is a small set of trusted operators with shell access to the management workstation.
- The internal CA private material is kept outside this public repository.
- A compromised node must not automatically imply trust in every other service.
- The public repo may be read by anyone and therefore cannot rely on obscurity.

## Primary Trust Boundaries

- **Operator boundary**: trusted operators versus untrusted clients on the network.
- **Edge boundary**: ingress, VPN termination, and object storage live on the edge host and are treated as higher-risk surfaces.
- **Cluster boundary**: Kubernetes nodes are trusted only after baseline configuration, trust-root installation, and package validation.
- **CA boundary**: issuing keys and provisioner material stay isolated from normal workload hosts.

## Plausible Failure Modes

- A host is rebuilt from stale or drifting automation.
- A generated public export still contains a private literal.
- Secret material leaks through Terraform state, logs, shell history, or CI output.
- Runtime config exists on disk but the relevant service was never restarted or validated.
- Monitoring examples compile but are not actually self-contained.

## Controls In This Repo

- explicit version pinning for infrastructure-facing examples
- handler-driven restarts instead of unconditional “changed” reporting
- post-apply validation tasks and health checks
- denylist scanning and fixture tests for sanitization
- CI checks for Ansible syntax, OpenTofu validation, and compose rendering
