# Ansible Infrastructure Patterns

This directory shows the host-side automation style used in the private homelab: explicit scope boundaries, handler-driven convergence, pinned versions for infrastructure-facing services, and validation steps that prove the rendered configuration is usable.

## Included Examples

- `inventory.example.ini`: role-oriented groups with clearer host boundaries
- `group_vars/` and `host_vars/`: layered inventory examples
- `install-edge.yml`: edge-host baseline
- `install-baremetal.yml`: cluster-node baseline
- `install-kubernetes.yml`: Kubernetes prerequisite bootstrap
- `install-minio.yml`: pinned edge-host object storage bootstrap

## Operating Pattern

- keep edge bootstrap separate from cluster-node bootstrap
- install the internal trust root only when the source changes, then refresh trust via handlers
- validate service state after rendering configuration
- prefer assertions and explicit failure over optimistic drift

## Example Commands

```bash
ansible-playbook -i inventory.example.ini install-edge.yml
ansible-playbook -i inventory.example.ini install-baremetal.yml
ansible-playbook -i inventory.example.ini install-kubernetes.yml
ansible-playbook -i inventory.example.ini install-minio.yml
```

## Validation Goals

- rerunning a play should not report changes unless an input changed
- trust refresh happens only when the CA placeholder changes
- containerd and kubelet configuration writes trigger the right restart handlers
- the MinIO example verifies mount presence, free space, and local health before reporting success
