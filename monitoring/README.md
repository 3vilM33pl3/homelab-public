# Monitoring and Ingress Patterns

The private homelab uses a single edge host for ingress, telemetry collection, and a few infrastructure-facing services. This public version keeps the pattern without publishing the real endpoints.

## Preserved Ideas

- a reverse proxy terminates internal TLS using certificates from the private CA
- telemetry receivers stay reachable on stable internal ports
- storage and monitoring have explicit host paths and retention settings
- mTLS is used to protect especially sensitive internal surfaces

## Included Examples

- `compose.yml`: minimal observability stack shape
- `caddy/Caddyfile`: internal ingress, ACME against the private CA, and an mTLS-protected endpoint

## Example Ports

- OTLP gRPC: `4317`
- OTLP HTTP: `4318`
- object storage API: `9000`
- object storage console: `9001`
- mTLS test endpoint: `18080`
