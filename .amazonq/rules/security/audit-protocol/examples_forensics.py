"""
Forensic Analysis Pattern Example

This file demonstrates the generic timeline reconstruction and investigation pattern.
Reference this example from RULE.mdc using @examples_forensics.py syntax.
"""

from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass


# ============================================================================
# Forensic Analysis Pattern
# ============================================================================

@dataclass
class TimelineEvent:
    """
    Generic timeline event structure for forensic analysis.
    
    This demonstrates the pattern for reconstructing timelines from audit logs:
    - Event timestamp
    - Event type and details
    - Actor information
    - Resource and action
    """
    timestamp: datetime
    event_type: str
    actor_id: str
    resource: str
    action: str
    details: Dict[str, Any]


class ForensicAnalyzer:
    """
    Generic forensic analyzer pattern.
    
    This demonstrates the methodology for forensic analysis:
    - Timeline reconstruction from audit logs
    - User activity tracking across sessions
    - System state reconstruction
    """
    
    def __init__(self, audit_log_reader: Any):
        """
        Initialize forensic analyzer.
        
        Args:
            audit_log_reader: Reader for accessing audit logs
        """
        self.log_reader = audit_log_reader
    
    def reconstruct_timeline(
        self,
        correlation_id: str | None = None,
        actor_id: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None
    ) -> List[TimelineEvent]:
        """
        Reconstruct timeline of events from audit logs.
        
        This demonstrates the pattern for timeline reconstruction:
        - Filter events by correlation ID, actor, or time range
        - Order events chronologically
        - Extract relevant event details
        
        Args:
            correlation_id: Filter by correlation ID
            actor_id: Filter by actor ID
            start_time: Start of time range
            end_time: End of time range
            
        Returns:
            List of timeline events in chronological order
        """
        logs = self.log_reader.query(
            correlation_id=correlation_id,
            actor_id=actor_id,
            start_time=start_time,
            end_time=end_time
        )
        
        events = []
        for log_entry in logs:
            event = TimelineEvent(
                timestamp=datetime.fromisoformat(log_entry["timestamp"]),
                event_type=log_entry["event_type"],
                actor_id=log_entry["actor_id"],
                resource=log_entry["resource"],
                action=log_entry["action"],
                details=log_entry.get("metadata", {})
            )
            events.append(event)
        
        events.sort(key=lambda e: e.timestamp)
        return events
    
    def track_user_activity(
        self,
        user_id: str,
        session_id: str | None = None
    ) -> Dict[str, Any]:
        """
        Track all user activities across sessions.
        
        This demonstrates the pattern for user activity tracking:
        - Aggregate events by user
        - Group by session if provided
        - Identify activity patterns
        
        Args:
            user_id: User ID to track
            session_id: Optional session ID to filter
            
        Returns:
            Dict containing user activity summary
        """
        events = self.reconstruct_timeline(actor_id=user_id)
        
        if session_id:
            events = [
                e for e in events
                if e.details.get("session_id") == session_id
            ]
        
        return {
            "user_id": user_id,
            "session_id": session_id,
            "total_events": len(events),
            "event_types": self._group_by_event_type(events),
            "timeline": [self._event_to_dict(e) for e in events]
        }
    
    def _group_by_event_type(
        self,
        events: List[TimelineEvent]
    ) -> Dict[str, int]:
        """Group events by event type."""
        grouped = {}
        for event in events:
            grouped[event.event_type] = grouped.get(event.event_type, 0) + 1
        return grouped
    
    def _event_to_dict(self, event: TimelineEvent) -> Dict[str, Any]:
        """Convert timeline event to dictionary."""
        return {
            "timestamp": event.timestamp.isoformat(),
            "event_type": event.event_type,
            "resource": event.resource,
            "action": event.action,
            "details": event.details
        }
    
    def verify_log_integrity(
        self,
        events: List[TimelineEvent]
    ) -> Dict[str, Any]:
        """
        Verify integrity of audit log entries.
        
        This demonstrates the pattern for log integrity verification:
        - Verify cryptographic hashes
        - Check for missing entries
        - Validate timestamp sequence
        
        Args:
            events: List of timeline events to verify
            
        Returns:
            Dict containing integrity verification results
        """
        issues = []
        
        for i, event in enumerate(events):
            if i > 0 and events[i-1].timestamp > event.timestamp:
                issues.append({
                    "type": "timestamp_sequence",
                    "event_index": i,
                    "message": "Timestamp out of sequence"
                })
        
        return {
            "total_events": len(events),
            "issues_found": len(issues),
            "issues": issues,
            "integrity_verified": len(issues) == 0
        }
