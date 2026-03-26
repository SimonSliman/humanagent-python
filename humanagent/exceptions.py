class HumanAgentError(Exception):
    """Base exception for HumanAgent SDK."""
    pass


class AuthenticationError(HumanAgentError):
    """Invalid or missing API key."""
    pass


class CheckpointNotFoundError(HumanAgentError):
    """Checkpoint ID not found."""
    pass


class CheckpointExpiredError(HumanAgentError):
    """Checkpoint has expired."""
    pass
