# Public Homelab Reference

This repository is a sanitized, public-facing version of a private homelab. It is meant to be a credible reference example: small enough to read quickly, but disciplined enough to demonstrate safe operating habits.

## What Stays Visible

- Ansible for host provisioning and edge-service bootstrap
- OpenTofu for Kubernetes resources and shared infrastructure
- a dedicated internal certificate authority
- WireGuard-based remote access
- object storage, observability, and backups as first-class infrastructure

## What Is Intentionally Removed

- real domains, hostnames, IP ranges, and operator identity
- private git history
- secrets, certificates, state files, and network scans
- workload-specific runbooks and service inventory

## Repository Layout

- `docs/`: architecture, trust model, and operational guidance
- `iac_ansible/`: convergent host-side automation examples
- `iac_terraform/`: generic cluster resource examples
- `monitoring/`: runnable ingress and telemetry examples
- `tools/`: export, sanitization, and validation tooling

## Golden Path Rebuild

1. Prepare hosts that match the example inventory and supported platform matrix.
2. Bootstrap the trust root and baseline host configuration with the edge and baremetal playbooks.
3. Run the Kubernetes prerequisite playbook on cluster nodes.
4. Bring up the monitoring example and confirm telemetry ingress and the mTLS test endpoint work.
5. Initialize OpenTofu with a non-committed backend config, then run `tofu plan` and `tofu apply`.
6. Run the validation checklist below before considering the rebuild healthy.

## Post-Deploy Verification

- all Ansible playbooks pass syntax checks
- trust-root file is present and trust refresh completed only when inputs changed
- containerd and kubelet are enabled and active on cluster nodes
- MinIO health endpoint responds on the edge host
- `tofu fmt -check` and `tofu validate` succeed
- `docker compose config` resolves cleanly for the monitoring stack
- repo denylist scan reports no forbidden private literals

## Managed Surface Matrix

| Area | Managed Here | Notes |
| --- | --- | --- |
| Base host bootstrap | Yes | Public example only, sanitized |
| Kubernetes node prerequisites | Yes | Package/install flow is explicit |
| Edge-host object storage | Yes | MinIO example with pinned version and health checks |
| Internal CA model | Yes | Operating model and trust boundaries are documented |
| Monitoring ingress example | Yes | Runnable compose example |
| Workload-specific service inventory | No | Intentionally excluded from the public repo |
| Private secrets and recovery material | No | Stay in the private source of truth |

## Supported Platforms

| Component | Tested expectation |
| --- | --- |
| Ansible examples | Debian-family systems with `update-ca-certificates` |
| Kubernetes bootstrap example | Debian-family systems with systemd |
| Monitoring example | Docker Compose v2 on Linux |
| OpenTofu examples | OpenTofu/Terraform 1.6+ with Kubernetes provider 2.29.x |

## Upgrade and Rollback Expectations

- Pin versions before changing runtime dependencies.
- Review diffs with `tofu plan`, compose config render, and Ansible syntax checks before applying.
- Upgrade one subsystem at a time: host bootstrap, monitoring stack, then cluster resources.
- Roll back by reverting the branch commit range, re-running the relevant playbook or compose stack, and validating the checklist again.

## Export Workflow

The private repo remains the source of truth. Running the export tool produces sanitized source snapshots in `iac_ansible/generated/` so the public curation process stays inspectable:

```bash
python3 tools/export-public-homelab.py \
  --source /path/to/private/homelab \
  --dest .
```

Generated snapshots are convenience artifacts. Publication safety depends on the denylist scan, fixture tests, and manual review gate, not regex replacement alone.
