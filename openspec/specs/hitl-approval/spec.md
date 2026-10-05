# HITL approval

## Purpose
Prevent sensitive escalation actions until an engineer approves them.

## Requirements
### Requirement: Sensitive actions require approval
The agent MUST pause before any model message containing a sensitive tool call.
#### Scenario: Approved escalation executes
- GIVEN a paused thread
- WHEN an engineer approves
- THEN the sensitive call executes once
#### Scenario: Rejected escalation is not executed
- GIVEN a paused thread
- WHEN an engineer rejects
- THEN every pending call receives a rejection ToolMessage and no sensitive call executes
