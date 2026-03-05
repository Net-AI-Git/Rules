"""
Prompt Registry with Splunk Logging Example

This file demonstrates a prompt registry that logs usage and version events to Splunk (via HEC).
Reference this example from RULE.mdc using @examples_prompt_registry_splunk.py syntax.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class PromptVersion:
    """Prompt version with metadata."""
    name: str
    version: str
    content: str
    tags: list[str]
    description: str = ""


class PromptRegistry:
    """
    In-app prompt registry. Load prompts from YAML/config; log all retrieval and
    version usage to Splunk via the provided sink (e.g., Splunk HEC client).
    """

    def __init__(self, splunk_sink: Optional[Any] = None) -> None:
        self._prompts: Dict[str, PromptVersion] = {}
        self.splunk_sink = splunk_sink  # e.g., SplunkHECClient from @examples_splunk_hec

    def register(self, key: str, prompt: PromptVersion) -> None:
        """Register a prompt version; send event to Splunk for audit."""
        self._prompts[key] = prompt
        if self.splunk_sink:
            self._log_to_splunk(
                event_type="prompt_registered",
                key=key,
                version=prompt.version,
                name=prompt.name,
            )

    def get(self, key: str, correlation_id: Optional[str] = None) -> Optional[PromptVersion]:
        """Retrieve prompt; log usage to Splunk."""
        prompt = self._prompts.get(key)
        if prompt and self.splunk_sink and correlation_id:
            self._log_to_splunk(
                event_type="prompt_retrieved",
                key=key,
                version=prompt.version,
                name=prompt.name,
                correlation_id=correlation_id,
            )
        return prompt

    def _log_to_splunk(self, event_type: str, key: str, version: str, name: str, correlation_id: str = "") -> None:
        """Send prompt event to Splunk (HEC)."""
        if not self.splunk_sink:
            return
        event: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "prompt_key": key,
            "prompt_name": name,
            "prompt_version": version,
        }
        if correlation_id:
            event["correlation_id"] = correlation_id
        if hasattr(self.splunk_sink, "send_event"):
            self.splunk_sink.send_event(event)


# Usage: registry = PromptRegistry(splunk_sink=hec_client); registry.register("system", p); registry.get("system", correlation_id="req-123")
