"""
Splunk HEC (HTTP Event Collector) Ingestion Example

This file demonstrates sending structured logs and metric events to Splunk via HEC.
Reference this example from RULE.mdc using @examples_splunk_hec.py syntax.
All events MUST include mandatory fields: timestamp, correlation_id, operation_name (or equivalent).
"""

import logging
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)


class SplunkHECClient:
    """
    Minimal client for sending events to Splunk HTTP Event Collector (HEC).

    Events are sent as JSON. Required fields per monitoring-and-observability:
    timestamp, correlation_id, operation_name (or stage). Optional: start_timestamp,
    end_timestamp, duration_ms for timing.
    """

    def __init__(
        self,
        hec_url: str,
        hec_token: str,
        index: Optional[str] = None,
        source: Optional[str] = None,
        sourcetype: str = "_json",
    ) -> None:
        self.hec_url = hec_url.rstrip("/") + "/services/collector/event"
        self.hec_token = hec_token
        self.index = index
        self.source = source
        self.sourcetype = sourcetype

    def send_event(self, event: Dict[str, Any]) -> bool:
        """
        Send a single event to Splunk HEC.

        Args:
            event: Dict with mandatory fields (timestamp, correlation_id, operation_name)
                   and any optional fields. Will be sent as JSON in the 'event' payload.

        Returns:
            True if accepted by Splunk, False otherwise.
        """
        payload: Dict[str, Any] = {"event": event, "sourcetype": self.sourcetype}
        if self.index:
            payload["index"] = self.index
        if self.source:
            payload["source"] = self.source

        headers = {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json",
        }
        try:
            with httpx.Client() as client:
                resp = client.post(self.hec_url, json=payload, headers=headers, timeout=10.0)
            if resp.status_code == 200:
                return True
            logger.warning("splunk_hec_error", status_code=resp.status_code, response=resp.text)
            return False
        except Exception as e:
            logger.error("splunk_hec_send_failed", error=str(e), exc_info=True)
            return False

    def send_timed_operation(
        self,
        operation_name: str,
        correlation_id: str,
        start_timestamp: str,
        end_timestamp: str,
        duration_ms: float,
        **extra: Any,
    ) -> bool:
        """
        Send a timed operation event (span-like) to Splunk.

        Ensures mandatory fields for latency analysis and tracing in SPL.
        """
        event = {
            "timestamp": end_timestamp,
            "correlation_id": correlation_id,
            "operation_name": operation_name,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": round(duration_ms, 2),
            **extra,
        }
        return self.send_event(event)


# Usage example (for documentation):
#
# hec = SplunkHECClient(
#     hec_url="https://splunk.example.com:8088",
#     hec_token="<HEC_TOKEN>",
#     index="main",
#     source="my_app",
# )
# hec.send_event({
#     "timestamp": datetime.now(timezone.utc).isoformat(),
#     "correlation_id": "req-uuid-123",
#     "operation_name": "llm_call",
#     "duration_ms": 450.2,
#     "model": "gpt-4",
# })
# hec.send_timed_operation(
#     operation_name="tool_execute",
#     correlation_id="req-uuid-123",
#     start_timestamp="...",
#     end_timestamp="...",
#     duration_ms=120.5,
#     tool_name="search",
# )
