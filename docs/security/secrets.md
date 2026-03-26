# Secrets and Credential Handling

This public repo documents the handling model, not the secret material itself.

## Principles

- Never commit plaintext credentials, private keys, or state files.
- Keep encrypted secrets in a private source repository or secret manager.
- Prefer prompted values or environment injection over inline literals.
- Treat CA key material, provisioner credentials, and Terraform state as separate high-risk assets.

## Required Controls

- Run the denylist scan before publishing any branch or tag from this repo.
- Keep backend credentials in ignored `*.tfvars` files or environment variables.
- Keep Terraform-managed secrets out of resource data so they do not land in state.
- Treat shell history, `/tmp`, CI logs, and build artifacts as potential secret leak surfaces.

## Terraform State Warning

Even when the repo source looks clean, secret values can still leak into Terraform state. The public example therefore references externally managed TLS secrets and avoids creating secret material directly through Terraform resources.

## Handling Rules

- Do not paste secret values into CLI flags that will land in shell history.
- Remove transient files from `/tmp` and ad hoc working directories after use.
- Mask or avoid printing sensitive values in CI output.
- Expire build artifacts that contain rendered config or logs as quickly as possible.

## Break-Glass Rotation

1. Revoke or replace the affected credential at the source system.
2. Update the private source of truth or secret manager entry.
3. Re-run the minimal automation needed to re-render the dependent configuration.
4. Validate the affected service locally before restoring normal rollout flow.
5. Run the denylist scan again before publishing anything.

## Publication Gate

- export snapshots are convenience artifacts, not a publication decision
- publication requires passing the denylist scan and fixture tests
- final publication still requires manual review of generated diffs
