# Triage API

## Purpose
Expose incident triage and approval through HTTP endpoints.

## Requirements
### Requirement: HTTP workflow
The API SHALL expose `/chat`, `/approve`, and `/healthz`.
#### Scenario: Missing approval
- GIVEN a thread without pending approval
- WHEN `/approve` is called
- THEN HTTP 400 is returned
