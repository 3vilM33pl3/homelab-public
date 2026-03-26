# Monitoring and Ingress Patterns

This directory is a runnable example for ingress, telemetry ingestion, and client-certificate enforcement. Object storage is managed separately by the MinIO Ansible example so the monitoring example can stay self-contained.

## What This Example Demonstrates

- a reverse proxy that trusts an internal CA endpoint
- an OpenTelemetry collector with an explicit mounted config
- a dedicated mTLS test service behind client-certificate auth
- pinned image versions, restart policies, and health checks

## Validation Flow

```bash
docker compose -f compose.yml config
docker compose -f compose.yml up -d
docker compose -f compose.yml ps
```

## Required Local Inputs

- replace `caddy/roots.example.pem` with the trust bundle used for client certificate validation
- ensure the CA endpoint configured in `caddy/Caddyfile` is reachable from the edge host
- keep telemetry and mTLS endpoints on the private side of the network boundary
