# Changelog

## 0.1.0 (2026-03-26)

- Initial release
- `HumanAgent` client with `checkpoint()`, `create_checkpoint()`, `get_checkpoint()`
- Custom exceptions: `AuthenticationError`, `CheckpointNotFoundError`, `CheckpointExpiredError`
- Blocking mode (poll until result) and fire-and-forget mode (webhook callback)
- Supports credential types: bar_licensed, cpa, cfa, architect, general
- SLA tiers: 90s, 5min, 15min, 30min, 1hr, 2hr, 4hr
