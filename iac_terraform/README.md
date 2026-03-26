# OpenTofu Infrastructure Patterns

This directory shows the cluster-side half of the homelab: provider setup, backend expectations, and a generic workload example that favors reliability patterns over raw object creation.

## Backend Expectations

- object storage state must use TLS
- state locking must be enabled where the backend supports it
- backend credentials belong in ignored files or environment variables
- state buckets should be versioned and backed up independently of the repo

An example backend config lives in `backend.example.hcl`. It is illustrative, not committed with real values.

## Validation Flow

```bash
tofu init -backend=false
tofu fmt -check
tofu validate
tofu plan -detailed-exitcode
```

## Drift And Lifecycle Expectations

- use `plan -detailed-exitcode` in CI or review scripts to distinguish no-op, drift, and error
- import pre-existing resources before claiming they are managed here
- promote reusable workload logic into modules rather than duplicating flat resources

## File Guide

- `main.tf`: providers and backend shape
- `backend.example.hcl`: backend safety expectations
- `variables.tf`: validated inputs
- `workloads-example.tf`: module instantiation for a generic service
- `modules/app-workload/`: deployment, service, storage, ingress, PDB, and network policy example
