# Ansible Infrastructure Patterns

This directory shows the host-side automation style used in the private homelab: small playbooks, shared task files, prompted secrets only when necessary, and a strong bias toward convergent configuration.

## Included Examples

- `inventory.example.ini`: generic host groups and role-oriented names
- `install-baremetal.yml`: base node configuration and CA trust distribution
- `install-kubernetes.yml`: cluster prerequisites and kubelet/containerd setup
- `install-minio.yml`: object storage for state and internal artifacts
- `tasks/`: compact reusable task files
- `ca/README.md`: the dedicated CA host operating model

## Operating Pattern

- bootstrap SSH once, then move toward certificate-backed access
- install the internal trust root on every managed node
- keep cluster-node setup separate from edge services
- prompt for bootstrap secrets instead of storing them in playbooks

## Example Commands

```bash
ansible-playbook -i inventory.example.ini install-baremetal.yml
ansible-playbook -i inventory.example.ini install-kubernetes.yml
ansible-playbook -i inventory.example.ini install-minio.yml --limit edge-1
```

## Notes

- The examples are intentionally generic and omit private mount layouts, service catalogs, and recovery procedures.
- Sanitized snapshots from the private repo land in `generated/` when the export tool is run.
