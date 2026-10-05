# Triage agent

## Purpose
Investigate incidents using safe health and runbook tools.

## Requirements
### Requirement: Investigate incidents
The agent SHALL inspect service health and relevant runbooks before responding.
#### Scenario: Safe investigation
- GIVEN an incident message without escalation
- WHEN triage runs
- THEN health and runbook tools execute and a completed response is returned
