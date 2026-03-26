# Public Homelab Reference

This repository is a sanitized, public-facing version of a private homelab. The goal is to show the ideas, layout, and security model without exposing the exact installation.

## What Stays Visible

- Ansible for host provisioning and edge-service setup
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

- `docs/`: public architecture and security notes
- `iac_ansible/`: curated host-side automation examples
- `iac_terraform/`: generic workload and provider examples
- `monitoring/`: observability and reverse-proxy examples
- `tools/`: sanitization tooling used to create export snapshots

## Export Workflow

The private repo remains the source of truth. Running the export tool produces sanitized source snapshots in `iac_ansible/generated/` so the public curation process stays inspectable:

```bash
python3 tools/export-public-homelab.py \
  --source /path/to/private/homelab \
  --dest .
```

The hand-maintained public docs and examples are the primary interface. Generated snapshots are review material, not a publish-by-default output.
