# Deployment

## Purpose
Describe deployment, health checks, and secret handling.

## Requirements
### Requirement: Render service
The service SHALL bind to `$PORT` and expose a dependency-free health endpoint.
#### Scenario: Health check
- GIVEN the service is running
- WHEN `/healthz` is requested
- THEN HTTP 200 is returned without Gemini or database access
