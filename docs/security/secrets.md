# Secrets and Credential Handling

This public repo documents the handling model, not the secret material itself.

## Principles

- Never commit plaintext credentials, private keys, or state files.
- Keep encrypted secrets in a private source repository or secret manager.
- Prefer prompted values or environment injection over inline literals.
- Treat CA key material and provisioner credentials as a separate risk class from normal service credentials.

## Public-Friendly Pattern

- Store long-lived configuration in encrypted files managed with SOPS and AGE.
- Keep backend credentials in ignored `*.tfvars` files or environment variables.
- Prompt for one-time bootstrap secrets in Ansible when human confirmation is appropriate.
- Create Kubernetes secrets from external values rather than hard-coded manifests.

## Redaction Rules

- Hostnames, domains, and CIDRs are examples only.
- Workload-specific names are generalized.
- Export snapshots from the private repo must be reviewed before commit.

## Verification

- Search the repo for accidental literals before publishing.
- Keep decrypted files out of working directories.
- Validate changed credentials with the smallest possible service check, then remove transient artifacts.
