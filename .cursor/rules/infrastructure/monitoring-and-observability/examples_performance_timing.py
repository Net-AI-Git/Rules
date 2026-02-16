"""
Performance Timing Implementation Example

This file demonstrates the PerformanceTimer context manager for latency measurement
with structured logging per monitoring-and-observability requirements.
Reference this example from RULE.mdc using @examples_performance_timing syntax.
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


class PerformanceTimer:
    """
    Context manager for automatic timing with structured logging.

    Logs start_timestamp, end_timestamp, duration_ms per monitoring-and-observability.
    Exposes duration_ms and duration_seconds for use in return values.
    """

    def __init__(
        self,
        operation_name: str,
        correlation_id: Optional[str] = None,
        **extra: Any,
    ) -> None:
        self.operation_name = operation_name
        self.correlation_id = correlation_id
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

            logger.info("operation_completed %s", json.dumps(log_data))
        finally:
            pass

    def __repr__(self) -> str:
        return f"PerformanceTimer({self.operation_name}, duration_ms={self.duration_ms})"


# Usage example (for documentation):
#
# with PerformanceTimer("execute_action", action_id="act_123") as timer:
#     result = do_work()
# execution_time = timer.duration_seconds  # Use in ActionResult
