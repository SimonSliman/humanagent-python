# Changelog

## 0.1.0 (2026-03-26)

Initial release.

- `HumanAgent` client with API key authentication
- `checkpoint()` — create and optionally poll until result
- `create_checkpoint()` — fire-and-forget creation
- `get_checkpoint()` — poll status by ID
- Custom exceptions: `AuthenticationError`, `CheckpointNotFoundError`, `CheckpointExpiredError`
- Support for credentials, SLA, budget, priority, webhooks
