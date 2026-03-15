"""
Performance Timing Implementation Example

This file demonstrates the PerformanceTimer context manager for latency measurement
with structlog per monitoring-and-observability requirements. Logs are
suitable for Splunk ingestion (e.g., via HEC); optionally pass a Splunk HEC client
to send timed events directly to Splunk.
Reference this example from RULE.mdc using @examples_performance_timing syntax.
"""

import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)


class PerformanceTimer:
    """
    Context manager for automatic timing with structured logging.

    Uses `time.perf_counter()` per monitoring-and-observability for high-resolution
    duration measurement. Logs start_timestamp, end_timestamp, duration_ms. When
    splunk_hec is provided (e.g., SplunkHECClient from @examples_splunk_hec), also
    sends the timed event to Splunk via HEC for SPL analysis.
    """

    def __init__(
        self,
        operation_name: str,
        correlation_id: Optional[str] = None,
        splunk_hec: Optional[Any] = None,
        **extra: Any,
    ) -> None:
        self.operation_name = operation_name
        self.correlation_id = correlation_id
        self.splunk_hec = splunk_hec
        self.extra = extra
        self.start_timestamp: Optional[str] = None
        self.end_timestamp: Optional[str] = None
        self.duration_ms: float = 0.0
        self.duration_seconds: float = 0.0
        self._start_time: float = 0.0

    def __enter__(self) -> "PerformanceTimer":
        self._start_time = time.perf_counter()
        self.start_timestamp = datetime.now(timezone.utc).isoformat()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            self.end_timestamp = datetime.now(timezone.utc).isoformat()
            elapsed = time.perf_counter() - self._start_time
            self.duration_seconds = elapsed
            self.duration_ms = elapsed * 1000.0

            log_data: Dict[str, Any] = {
                "timestamp": self.end_timestamp,
                "operation_name": self.operation_name,
                "start_timestamp": self.start_timestamp,
                "end_timestamp": self.end_timestamp,
                "duration_ms": round(self.duration_ms, 2),
                **self.extra,
            }
            if self.correlation_id:
                log_data["correlation_id"] = self.correlation_id

            logger.info("operation_completed", **log_data)

            if self.splunk_hec is not None and self.start_timestamp and self.end_timestamp:
                self.splunk_hec.send_timed_operation(
                    operation_name=self.operation_name,
                    correlation_id=self.correlation_id or "",
                    start_timestamp=self.start_timestamp,
                    end_timestamp=self.end_timestamp,
                    duration_ms=self.duration_ms,
                    **self.extra,
                )
        finally:
            pass

    def __repr__(self) -> str:
        return f"PerformanceTimer({self.operation_name}, duration_ms={self.duration_ms})"


# Usage example (for documentation):
#
# with PerformanceTimer("execute_action", correlation_id="req-123", action_id="act_123") as timer:
#     result = do_work()
# execution_time = timer.duration_seconds  # Use in ActionResult
#
# With Splunk HEC (see @examples_splunk_hec):
# hec = SplunkHECClient(hec_url="...", hec_token="...", index="main")
# with PerformanceTimer("llm_call", correlation_id="req-123", splunk_hec=hec, model="gpt-4") as timer:
#     response = llm.invoke(...)
