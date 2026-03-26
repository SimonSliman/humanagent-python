# HumanAgent Python SDK

Human checkpoint infrastructure for AI workflows. When your AI agent needs judgment, trust, or a licensed signature — HumanAgent routes it.

[![PyPI](https://img.shields.io/pypi/v/humanagent)](https://pypi.org/project/humanagent/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Install
```bash
pip install humanagent
```

## Quick start
```python
from humanagent import HumanAgent

client = HumanAgent(api_key="ha_live_...")

# Create a checkpoint and wait for result
result = client.checkpoint(
    task="Review NDA for compliance gaps",
    credential="bar_licensed:US",
    sla="30min",
    budget=25.00
)

if result["status"] == "completed":
    print(result["result"]["approved"])   # True/False
    print(result["result"]["notes"])      # Reviewer's notes
    print(result["audit_hash"])           # SHA-256 tamper-evident hash
```

## Fire and forget (webhook)
```python
created = client.checkpoint(
    task="Pick best 3 ad creatives",
    credential="general",
    sla="1hr",
    budget=5.00,
    callback_url="https://my-agent.com/webhook",
    wait=False
)
print(created["checkpoint_id"])  # Poll later or wait for webhook
```

## API Reference

### `HumanAgent(api_key, base_url=None, timeout=30)`

Initialize the client. API keys start with `ha_live_` or `ha_test_`.

### `.checkpoint(task, credential, sla, budget, ...wait=True)`

Create a checkpoint. If `wait=True` (default), polls until the human completes the review. If `wait=False`, returns immediately.

**Parameters:**
- `task` (str) — what the human needs to do
- `credential` (str, optional) — required credential, e.g. `"bar_licensed:US"`, `"cpa"`, `"architect"`
- `sla` (str) — time limit: `"90s"`, `"5min"`, `"30min"`, `"1hr"`, `"4hr"`
- `budget` (float, optional) — max USD willing to pay
- `priority` (str) — `"urgent"`, `"standard"`, or `"batch"`
- `payload_url` (str, optional) — URL to document for review
- `payload_meta` (dict, optional) — additional context
- `callback_url` (str, optional) — webhook URL for result delivery
- `wait` (bool) — block until result (default True)
- `poll_interval` (int) — seconds between polls (default 5)
- `max_wait` (int, optional) — max seconds to wait

### `.create_checkpoint(...)`

Same as `checkpoint()` but never waits. Returns immediately with `checkpoint_id`.

### `.get_checkpoint(checkpoint_id)`

Poll a checkpoint's current status.

## Exceptions

- `HumanAgentError` — base exception
- `AuthenticationError` — invalid or missing API key
- `CheckpointNotFoundError` — checkpoint ID not found
- `CheckpointExpiredError` — checkpoint SLA expired

## Credentials

Available credential types for the `credential` parameter:
- `bar_licensed` — licensed attorney (add jurisdiction: `bar_licensed:US`, `bar_licensed:US:CA`)
- `cpa` — Certified Public Accountant
- `cfa` — Chartered Financial Analyst
- `architect` — licensed architect
- `general` — general reviewer (no specific license required)

## Links

- **Website:** [humanagent.net](https://humanagent.net)
- **API docs:** [humanagent.net/agent.json](https://humanagent.net/agent.json)
- **Part of the [AgentEazy](https://agenteazy.com) ecosystem**

## License

MIT
