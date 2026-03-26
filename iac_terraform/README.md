# OpenTofu Infrastructure Patterns

This directory shows the cluster-side half of the homelab: provider setup, shared variables, and a generic workload definition that covers the main patterns without naming the real services.

## Patterns Preserved

- Kubernetes resources managed through OpenTofu
- object storage-backed state
- explicit namespaces and labels
- TLS secrets injected from external values
- PVC-backed workloads rather than purely ephemeral containers

## File Guide

- `main.tf`: providers and backend shape
- `variables.tf`: cluster, ingress, and storage inputs
- `workloads-example.tf`: one generic workload showing namespace, secret, service, ingress, and persistent storage

## Typical Flow

```bash
tofu init -backend-config=backend.tfvars
tofu plan
tofu apply
```

The examples assume Kubernetes access is already working and that object storage credentials come from ignored files or environment variables.
