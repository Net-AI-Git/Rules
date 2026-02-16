"""
Executor Node Implementation Example

This file demonstrates the Executor node implementation following READ→DO→WRITE→CONTROL pattern.
Reference this example from RULE.mdc using @examples_executor_node.py syntax.
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import TypedDict, List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# See @examples_performance_timing in monitoring-and-observability for full implementation.
logger = logging.getLogger(__name__)


class PerformanceTimer:
    """Minimal PerformanceTimer for structured latency logging (start/end/duration_ms)."""

    def __init__(self, operation_name: str, **extra: Any) -> None:
        self.operation_name = operation_name
        self.extra = extra
        self.duration_seconds: float = 0.0
        self._start: float = 0.0
        self._start_ts: str = ""

    def __enter__(self) -> "PerformanceTimer":
        self._start = time.perf_counter()
        self._start_ts = datetime.now(timezone.utc).isoformat()
        return self

    def __exit__(self, *args: Any) -> None:
        end_ts = datetime.now(timezone.utc).isoformat()
        self.duration_seconds = time.perf_counter() - self._start
        duration_ms = self.duration_seconds * 1000
        log_data = {
            "timestamp": end_ts,
            "operation_name": self.operation_name,
            "start_timestamp": self._start_ts,
            "end_timestamp": end_ts,
            "duration_ms": round(duration_ms, 2),
            **self.extra,
        }
        logger.info("operation_completed %s", json.dumps(log_data))


# ============================================================================
# Executor Node State Types
# ============================================================================

@dataclass
class StrategicPlan:
    """Strategic plan from Planner."""
    plan_id: str
    goals: List[str]
    action_sequence: List[str]
    dependencies: Dict[str, List[str]]


@dataclass
class ConcreteAction:
    """Concrete action ready for execution."""
    action_id: str
    action_type: str  # api_call, tool_invocation, file_operation, etc.
    parameters: Dict[str, Any]
    dependencies: List[str]
    retry_config: Optional[Dict[str, Any]] = None


@dataclass
class ActionResult:
    """Result from action execution."""
    action_id: str
    success: bool
    result_data: Dict[str, Any]
    error: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class ExecutionStatus:
    """Execution status for monitoring."""
    status: str  # pending, in_progress, completed, failed
    completed_actions: int
    total_actions: int
    results: List[ActionResult]
    errors: List[str]


class ExecutorState(TypedDict):
    """State structure for Executor node."""
    strategic_plan: Optional[StrategicPlan]
    sections: Optional[List[Dict[str, Any]]]
    context: Dict[str, Any]
    concrete_actions: Optional[List[ConcreteAction]]
    execution_status: Optional[ExecutionStatus]
    results: Optional[List[ActionResult]]


# ============================================================================
# Executor Node Implementation
# ============================================================================

class ExecutorNode:
    """
    Executor node implementation following READ→DO→WRITE→CONTROL pattern.
    
    This demonstrates:
    - READ: Read strategic plan, SECTIONS, and execution context
    - DO: Translate plans to actions, coordinate execution, monitor results
    - WRITE: Write actions, execution status, and results to state
    - CONTROL: Route to Workers, Memory Node, or next node
    """
    
    def __init__(self):
        """Initialize Executor node."""
        pass
    
    def executor_node(self, state: ExecutorState) -> ExecutorState:
        """
        Executor node following READ→DO→WRITE→CONTROL pattern.
        
        Args:
            state: Current state with strategic_plan, sections, context
            
        Returns:
            Updated state with concrete_actions, execution_status, results
        """
        # READ: Read inputs from state
        strategic_plan = state.get("strategic_plan")
        sections = state.get("sections")
        context = state.get("context", {})
        
        # DO: Translate and execute
        if strategic_plan:
            concrete_actions = self._translate_plan(strategic_plan, context)
            execution_status = self._coordinate_execution(concrete_actions, context)
            results = execution_status.results
        elif sections:
            concrete_actions = self._translate_sections(sections, context)
            execution_status = self._coordinate_execution(concrete_actions, context)
            results = execution_status.results
        else:
            concrete_actions = []
            execution_status = ExecutionStatus(
                status="failed",
                completed_actions=0,
                total_actions=0,
                results=[],
                errors=["No plan or sections provided"]
            )
            results = []
        
        # WRITE: Write results to state
        state["concrete_actions"] = concrete_actions
        state["execution_status"] = execution_status
        state["results"] = results
        
        # CONTROL: State updated, routing handled by graph
        return state
    
    def _translate_plan(self, plan: StrategicPlan, context: Dict[str, Any]) -> List[ConcreteAction]:
        """
        Translate strategic plan to concrete actions.
        
        This demonstrates:
        - Plan parsing
        - Action conversion
        - Parameter extraction
        - Dependency mapping
        """
        actions = []
        for i, action_name in enumerate(plan.action_sequence):
            action = ConcreteAction(
                action_id=f"action_{i+1}",
                action_type="api_call",  # Would be determined from plan
                parameters={"name": action_name, "context": context},
                dependencies=plan.dependencies.get(action_name, [])
            )
            actions.append(action)
        return actions
    
    def _translate_sections(self, sections: List[Dict[str, Any]], 
                           context: Dict[str, Any]) -> List[ConcreteAction]:
        """
        Translate SECTIONS to concrete actions.
        
        This demonstrates:
        - SECTION parsing
        - Action creation from SECTIONS
        - Worker coordination preparation
        """
        actions = []
        for section in sections:
            action = ConcreteAction(
                action_id=section.get("section_id", "unknown"),
                action_type="worker_task",
                parameters={"section": section, "context": context},
                dependencies=section.get("dependencies", [])
            )
            actions.append(action)
        return actions
    
    def _coordinate_execution(self, actions: List[ConcreteAction], 
                            context: Dict[str, Any]) -> ExecutionStatus:
        """
        Coordinate action execution.
        
        This demonstrates:
        - Action dispatch
        - Dependency management
        - Parallel execution coordination
        - Result collection
        """
        results = []
        errors = []
        completed = 0
        
        # Execute actions (simplified - in production would handle dependencies and parallel execution)
        for action in actions:
            try:
                result = self._execute_action(action, context)
                results.append(result)
                if result.success:
                    completed += 1
                else:
                    errors.append(f"Action {action.action_id} failed: {result.error}")
            except Exception as e:
                errors.append(f"Action {action.action_id} error: {str(e)}")
                results.append(ActionResult(
                    action_id=action.action_id,
                    success=False,
                    result_data={},
                    error=str(e)
                ))
        
        status = ExecutionStatus(
            status="completed" if completed == len(actions) else "partial",
            completed_actions=completed,
            total_actions=len(actions),
            results=results,
            errors=errors
        )
        
        return status
    
    def _execute_action(self, action: ConcreteAction, context: Dict[str, Any]) -> ActionResult:
        """
        Execute a single action.

        This demonstrates:
        - Action execution
        - Error handling
        - Result formatting
        - Structured latency logging via PerformanceTimer
        """
        correlation_id = context.get("correlation_id")
        result_data: Dict[str, Any] = {}
        error_msg: Optional[str] = None
        success = False

        with PerformanceTimer(
            "execute_action",
            action_id=action.action_id,
            correlation_id=correlation_id or "",
        ) as timer:
            try:
                if action.action_type == "api_call":
                    result_data = {"status": "success", "data": "mock_result"}
                elif action.action_type == "tool_invocation":
                    result_data = {"tool_result": "mock_tool_output"}
                elif action.action_type == "worker_task":
                    result_data = {"worker_output": "mock_worker_result"}
                else:
                    raise ValueError(f"Unknown action type: {action.action_type}")
                success = True
            except Exception as e:
                error_msg = str(e)

        return ActionResult(
            action_id=action.action_id,
            success=success,
            result_data=result_data,
            error=error_msg,
            execution_time=timer.duration_seconds,
        )
