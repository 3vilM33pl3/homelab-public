# Documentation Index

This public documentation stays focused on architecture and operating principles.

## Start Here

- `../README.md`: scope of the public repo
- `architecture/homelab-public.dot`: architecture source
- `security/secrets.md`: secret-handling model
- `../iac_ansible/README.md`: host automation patterns
- `../iac_terraform/README.md`: cluster resource patterns
- `../monitoring/README.md`: observability and ingress patterns

## Design Principles

- network location is not enough to earn trust
- private PKI is part of routine operations
- secrets are encrypted or injected, not embedded in code
- public examples explain the system without exposing the real topology
