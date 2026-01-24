"""
Execution Coordination Examples

This file demonstrates coordination patterns with Workers and Tools, parallel execution, dependency management, and result collection.
Reference this example from RULE.mdc using @examples_execution_coordination.py syntax.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque


# ============================================================================
# Execution Coordination Types
# ============================================================================

@dataclass
class ConcreteAction:
    """Concrete action ready for execution."""
    action_id: str
    action_type: str
    parameters: Dict[str, Any]
    dependencies: List[str]
    worker_id: Optional[str] = None


@dataclass
class ActionResult:
    """Result from action execution."""
    action_id: str
    success: bool
    result_data: Dict[str, Any]
    error: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class ExecutionPlan:
    """Execution plan with sequencing."""
    sequential_actions: List[List[ConcreteAction]]  # Each inner list can run in parallel
    total_actions: int
    estimated_time: float


class ExecutionStatus(str, Enum):
    """Execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


# ============================================================================
# Execution Coordination Service
# ============================================================================

class ExecutionCoordinationService:
    """
    Service for coordinating action execution.
    
    This demonstrates:
    - Action dispatch
    - Dependency management
    - Parallel execution coordination
    - Result collection
    """
    
    def create_execution_plan(self, actions: List[ConcreteAction]) -> ExecutionPlan:
        """
        Create execution plan with dependency management.
        
        This demonstrates:
        - Dependency analysis
        - Sequential vs parallel grouping
        - Execution sequencing
        
        Args:
            actions: List of actions to execute
            
        Returns:
            Execution plan with sequencing
        """
        # Build dependency graph
        dependency_graph = self._build_dependency_graph(actions)
        
        # Topological sort to determine execution order
        execution_groups = self._topological_sort(actions, dependency_graph)
        
        # Calculate estimated time
        estimated_time = sum(
            max(action.parameters.get("estimated_time", 10) for action in group)
            for group in execution_groups
        )
        
        plan = ExecutionPlan(
            sequential_actions=execution_groups,
            total_actions=len(actions),
            estimated_time=estimated_time
        )
        
        return plan
    
    def _build_dependency_graph(self, actions: List[ConcreteAction]) -> Dict[str, Set[str]]:
        """
        Build dependency graph from actions.
        
        Args:
            actions: List of actions
            
        Returns:
            Dependency graph (action_id -> set of dependent action_ids)
        """
        graph = defaultdict(set)
        action_map = {action.action_id: action for action in actions}
        
        for action in actions:
            for dep_id in action.dependencies:
                if dep_id in action_map:
                    graph[action.action_id].add(dep_id)
        
        return dict(graph)
    
    def _topological_sort(self, actions: List[ConcreteAction], 
                         dependency_graph: Dict[str, Set[str]]) -> List[List[ConcreteAction]]:
        """
        Topological sort to group actions by execution level.
        
        Args:
            actions: List of actions
            dependency_graph: Dependency graph
            
        Returns:
            List of action groups (each group can run in parallel)
        """
        action_map = {action.action_id: action for action in actions}
        in_degree = {action.action_id: 0 for action in actions}
        
        # Calculate in-degrees
        for action in actions:
            for dep_id in dependency_graph.get(action.action_id, set()):
                if dep_id in in_degree:
                    in_degree[action.action_id] += 1
        
        # Topological sort
        execution_groups = []
        queue = deque([action_id for action_id, degree in in_degree.items() if degree == 0])
        
        while queue:
            current_level = []
            level_size = len(queue)
            
            for _ in range(level_size):
                action_id = queue.popleft()
                current_level.append(action_map[action_id])
                
                # Update in-degrees of dependent actions
                for dependent_id in dependency_graph.get(action_id, set()):
                    if dependent_id in in_degree:
                        in_degree[dependent_id] -= 1
                        if in_degree[dependent_id] == 0:
                            queue.append(dependent_id)
            
            if current_level:
                execution_groups.append(current_level)
        
        return execution_groups
    
    def coordinate_parallel_execution(self, action_group: List[ConcreteAction], 
                                     context: Dict[str, Any]) -> List[ActionResult]:
        """
        Coordinate parallel execution of action group.
        
        This demonstrates:
        - Parallel execution coordination
        - Worker dispatch
        - Result collection
        
        Args:
            action_group: Group of actions to execute in parallel
            context: Execution context
            
        Returns:
            List of action results
        """
        import asyncio
        
        async def execute_action_async(action: ConcreteAction) -> ActionResult:
            """Execute single action asynchronously."""
            return self._execute_action(action, context)
        
        # Execute all actions in parallel
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            asyncio.gather(*[execute_action_async(action) for action in action_group])
        )
        
        return results
    
    def coordinate_sequential_execution(self, action_groups: List[List[ConcreteAction]], 
                                      context: Dict[str, Any]) -> List[ActionResult]:
        """
        Coordinate sequential execution of action groups.
        
        This demonstrates:
        - Sequential execution
        - Group-by-group execution
        - Result aggregation
        
        Args:
            action_groups: Groups of actions to execute sequentially
            context: Execution context
            
        Returns:
            List of all action results
        """
        all_results = []
        
        for group in action_groups:
            # Execute group in parallel
            group_results = self.coordinate_parallel_execution(group, context)
            all_results.extend(group_results)
            
            # Check for failures that might affect subsequent groups
            failures = [r for r in group_results if not r.success]
            if failures and self._should_stop_on_failure(context):
                break
        
        return all_results
    
    def dispatch_to_worker(self, action: ConcreteAction, worker_id: str, 
                          context: Dict[str, Any]) -> ActionResult:
        """
        Dispatch action to worker.
        
        This demonstrates:
        - Worker selection
        - Action dispatch
        - Worker coordination
        
        Args:
            action: Action to dispatch
            worker_id: ID of worker to use
            context: Execution context
            
        Returns:
            Action result from worker
        """
        # Set worker ID in action
        action.worker_id = worker_id
        
        # Dispatch to worker (simplified - in production would use actual worker communication)
        result = self._execute_action(action, context)
        
        return result
    
    def collect_results(self, results: List[ActionResult]) -> Dict[str, Any]:
        """
        Collect and aggregate execution results.
        
        This demonstrates:
        - Result aggregation
        - Success/failure analysis
        - Performance metrics
        
        Args:
            results: List of action results
            
        Returns:
            Aggregated results
        """
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        total_time = sum(r.execution_time for r in results)
        avg_time = total_time / len(results) if results else 0
        
        aggregated = {
            "total_actions": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(results) if results else 0,
            "total_execution_time": total_time,
            "average_execution_time": avg_time,
            "results": results,
            "errors": [r.error for r in failed if r.error]
        }
        
        return aggregated
    
    def _execute_action(self, action: ConcreteAction, context: Dict[str, Any]) -> ActionResult:
        """
        Execute a single action (simplified).
        
        Args:
            action: Action to execute
            context: Execution context
            
        Returns:
            Action result
        """
        import time
        start_time = time.time()
        
        try:
            # Simplified execution
            result_data = {"action_id": action.action_id, "status": "success"}
            execution_time = time.time() - start_time
            
            return ActionResult(
                action_id=action.action_id,
                success=True,
                result_data=result_data,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ActionResult(
                action_id=action.action_id,
                success=False,
                result_data={},
                error=str(e),
                execution_time=execution_time
            )
    
    def _should_stop_on_failure(self, context: Dict[str, Any]) -> bool:
        """
        Determine if execution should stop on failure.
        
        Args:
            context: Execution context
            
        Returns:
            True if should stop on failure
        """
        return context.get("stop_on_failure", False)
