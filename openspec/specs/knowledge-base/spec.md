# Knowledge base

## Purpose
Store and retrieve incident runbooks using pgvector embeddings.

## Requirements
### Requirement: Runbook storage
The system SHALL store runbooks with JSON metadata and 768-dimensional embeddings.
#### Scenario: Schema matches embedding size
- GIVEN the migration is applied
- WHEN a 768-dimensional vector is inserted
- THEN the insert succeeds and other dimensions are rejected
### Requirement: Idempotent seeding
The seed process SHALL avoid duplicate content on repeated runs.
#### Scenario: Re-running the seed
- GIVEN the runbooks already exist
- WHEN the seed runs again
- THEN no duplicate rows are created
