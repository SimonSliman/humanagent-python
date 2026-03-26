# HumanAgent Python SDK

Human checkpoint infrastructure for AI workflows. When your AI agent needs judgment, trust, or a licensed signature — HumanAgent routes it.

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

# Fire and forget (use webhook)
created = client.checkpoint(
    task="Pick best 3 ad creatives",
    credential="general",
    sla="1hr",
    budget=5.00,
    callback_url="https://my-agent.com/webhook",
    wait=False
)
print(created["checkpoint_id"])
```

## API

### `HumanAgent(api_key, base_url=None, timeout=30)`

Initialize the client.

### `.checkpoint(task, credential, sla, budget, ...wait=True)`

Create a checkpoint. If `wait=True`, polls until result. If `wait=False`, returns immediately.

### `.create_checkpoint(task, credential, sla, budget, ...)`

Create without waiting.

### `.get_checkpoint(checkpoint_id)`

Poll status.

## More info

- Website: https://humanagent.net
- Docs: https://humanagent.net/docs (coming soon)
- Part of the AgentEazy ecosystem
