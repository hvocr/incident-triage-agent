# Triage UI

## Purpose
Provide a browser interface for triage and escalation approval.

## Requirements
### Requirement: Approval controls
The UI SHALL provide trigger, approve, reject, thread, and rejection-reason controls.
#### Scenario: Reject action
- GIVEN a thread awaiting approval
- WHEN the reject control is used
- THEN the shared service rejects the action
