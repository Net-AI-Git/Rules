"""
Audit Logging Implementation Example

This file demonstrates the generic audit log structure and event logging pattern.
Reference this example from RULE.mdc using @examples_audit_logging.py syntax.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Literal
from dataclasses import dataclass, asdict
import hashlib


# ============================================================================
# Audit Log Structure
# ============================================================================

@dataclass
class AuditLogEntry:
    """
    Generic audit log entry structure following audit protocol requirements.
    
    This demonstrates the required fields for all audit log entries:
    - timestamp: ISO 8601 format with timezone
    - event_type: Categorized event type
    - actor_id: User ID or agent ID
    - actor_type: Type of actor performing the action
    - resource: Resource being accessed or modified
    - action: Specific action performed
    - result: Outcome of the action
    - correlation_id: Request/transaction ID for tracing
    - tenant_id: Tenant identifier (if multi-tenant)
    - metadata: Additional context
    """
    timestamp: str
    event_type: str
    actor_id: str
    actor_type: Literal["user", "agent", "system"]
    resource: str
    action: str
    result: Literal["success", "failure", "denied"]
    correlation_id: str
    tenant_id: str | None
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log entry to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize audit log entry to JSON."""
        return json.dumps(self.to_dict(), default=str)
    
    def compute_hash(self) -> str:
        """
        Compute cryptographic hash for log integrity verification.
        
        Returns:
            str: SHA-256 hash of the log entry
        """
        log_str = self.to_json()
        return hashlib.sha256(log_str.encode()).hexdigest()


# ============================================================================
# Audit Logger Implementation
# ============================================================================

class AuditLogger:
    """
    Generic audit logger for structured audit log entries.
    
    This demonstrates the pattern for logging audit events with:
    - Structured JSON format
    - Immutable append-only logging
    - Cryptographic hashing for integrity
    """
    
    def __init__(self, storage_backend: Any):
        """
        Initialize audit logger.
        
        Args:
            storage_backend: Storage backend for audit logs (database, file, SIEM)
        """
        self.storage = storage_backend
        self.logger = logging.getLogger(__name__)
    
    def log_event(
        self,
        event_type: str,
        actor_id: str,
        actor_type: Literal["user", "agent", "system"],
        resource: str,
        action: str,
        result: Literal["success", "failure", "denied"],
        correlation_id: str,
        tenant_id: str | None = None,
        metadata: Dict[str, Any] | None = None
    ) -> None:
        """
        Log an audit event with all required fields.
        
        This method demonstrates the pattern for creating and storing
        audit log entries following the audit protocol structure.
        
        Args:
            event_type: Type of event (tool_call, state_change, api_request, etc.)
            actor_id: ID of the actor performing the action
            actor_type: Type of actor (user, agent, system)
            resource: Resource being accessed or modified
            action: Specific action performed
            result: Outcome of the action
            correlation_id: Request/transaction ID for tracing
            tenant_id: Tenant identifier if multi-tenant
            metadata: Additional context as JSON object
        """
        entry = AuditLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            actor_id=actor_id,
            actor_type=actor_type,
            resource=resource,
            action=action,
            result=result,
            correlation_id=correlation_id,
            tenant_id=tenant_id,
            metadata=metadata or {}
        )
        
        log_hash = entry.compute_hash()
        entry_dict = entry.to_dict()
        entry_dict["log_hash"] = log_hash
        
        self._write_log(entry_dict)
    
    def _write_log(self, entry: Dict[str, Any]) -> None:
        """
        Write audit log entry to storage (append-only).
        
        This demonstrates immutable logging - entries are never
        updated or deleted, only appended.
        
        Args:
            entry: Audit log entry dictionary
        """
        try:
            self.storage.append(entry)
            self.logger.debug(f"Audit log entry written: {entry['correlation_id']}")
        except Exception as e:
            self.logger.error(f"Failed to write audit log: {e}", exc_info=True)
            raise
