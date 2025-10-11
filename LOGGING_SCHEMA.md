# Logging Schema

This document defines the schema for the structured logs in `logs/activity.log.jsonl`.

Each log entry is a JSON object with the following fields:

- `timestamp`: ISO 8601 timestamp of the event.
- `task_id`: A unique identifier for the task being executed.
- `action_type`: The type of action being performed (e.g., `TOOL_CALL`, `PLAN_SET`, `MESSAGE_USER`).
- `details`: An object containing details specific to the action type.
- `valuation`: An object containing `positive` and `negative` valuations of the action, reflecting the paraconsistent logging model.
  - `positive`: Justification for the action.
  - `negative`: Risk assessment for the action.
- `status`: The status of the action (e.g., `SUCCESS`, `FAILURE`).
- `critic_feedback`: Any feedback from the internal critic model.