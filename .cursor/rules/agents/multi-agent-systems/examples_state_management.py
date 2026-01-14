"""
State Management Pattern Example

This file demonstrates the generic shared/worker state isolation pattern.
Reference this example from RULE.mdc using @examples_state_management.py syntax.
"""

from typing import Dict, Any, TypedDict, List


# ============================================================================
# State Management Pattern
# ============================================================================

class SharedState(TypedDict, total=False):
    """
    Generic shared state structure.
    
    This demonstrates the shared state pattern:
    - Common context for all agents
    - Read-only for workers (except designated write keys)
    - Contains input, intermediate results, documentation, decisions
    """
    input: str
    intermediate_results: List[Dict[str, Any]]
    documentation: Dict[str, Any]
    decisions: List[str]
    messages: List[Dict[str, Any]]


class WorkerState(TypedDict, total=False):
    """
    Generic worker state structure.
    
    This demonstrates the worker state pattern:
    - Task-specific details for each worker
    - Isolated from shared state
    - Contains assigned SECTION
    """
    worker_id: str
    section: Dict[str, Any]
    worker_specific_data: Dict[str, Any]


class StateManager:
    """
    Generic state management pattern.
    
    This demonstrates the pattern for state isolation:
    - Shared state: read-only for workers
    - Worker state: isolated per worker
    - Field ownership: each field owned by single node
    """
    
    def __init__(self):
        """Initialize state manager."""
        self.shared_state: SharedState = {
            "input": "",
            "intermediate_results": [],
            "documentation": {},
            "decisions": [],
            "messages": []
        }
        self.worker_states: Dict[str, WorkerState] = {}
    
    def get_shared_state(self) -> SharedState:
        """
        Get shared state (read-only for workers).
        
        This demonstrates the pattern for shared state access:
        - Workers can read shared state
        - Workers cannot modify shared state directly
        - Only designated nodes can write to shared state
        
        Returns:
            Shared state dictionary
        """
        return self.shared_state.copy()
    
    def get_worker_state(self, worker_id: str) -> WorkerState:
        """
        Get worker-specific state.
        
        This demonstrates the pattern for worker state isolation:
        - Each worker has isolated state
        - Worker state contains assigned SECTION
        - No cross-worker state access
        
        Args:
            worker_id: Worker identifier
            
        Returns:
            Worker state dictionary
        """
        if worker_id not in self.worker_states:
            self.worker_states[worker_id] = {
                "worker_id": worker_id,
                "section": {},
                "worker_specific_data": {}
            }
        return self.worker_states[worker_id]
    
    def update_shared_state(
        self,
        updates: Dict[str, Any],
        owner_node: str
    ) -> None:
        """
        Update shared state (only by owner node).
        
        This demonstrates the pattern for state field ownership:
        - Each state field assigned to single owner node
        - Only owner node can update its fields
        - Prevents accidental overwrites
        
        Args:
            updates: Dictionary of state updates
            owner_node: Node that owns these fields
        """
        for key, value in updates.items():
            if key in self.shared_state:
                self.shared_state[key] = value
