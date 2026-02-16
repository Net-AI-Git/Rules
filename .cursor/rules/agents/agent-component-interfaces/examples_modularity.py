"""
Modularity and Implementation Swapping Examples

This file demonstrates implementation swapping patterns, dependency injection, and A/B testing examples.
Reference this example from RULE.mdc using @examples_modularity.py syntax.
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
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
# Interface Definitions (from examples_interfaces.py)
# ============================================================================

class IPlanner(ABC):
    """Planner interface."""
    
    @abstractmethod
    def plan(self, user_request: Any, context: Any) -> Any:
        """Create strategic plan."""
        pass


class IMemoryNode(ABC):
    """Memory Node interface."""
    
    @abstractmethod
    def retrieve_memories(self, context: Any) -> list:
        """Retrieve memories."""
        pass


class IExecutor(ABC):
    """Executor interface."""
    
    @abstractmethod
    def translate_plan(self, plan: Any, context: Any) -> list:
        """Translate plan to actions."""
        pass


# ============================================================================
# Multiple Implementations
# ============================================================================

class BasicPlanner(IPlanner):
    """Basic Planner implementation."""
    
    def plan(self, user_request: Any, context: Any) -> Any:
        """Basic planning."""
        return {"plan_id": "basic_plan", "goals": ["Complete request"]}


class AdvancedPlanner(IPlanner):
    """Advanced Planner implementation with ML."""
    
    def plan(self, user_request: Any, context: Any) -> Any:
        """Advanced planning with ML."""
        return {"plan_id": "advanced_plan", "goals": ["Complete request", "Optimize resources"]}


class LocalMemoryNode(IMemoryNode):
    """Local memory implementation."""
    
    def retrieve_memories(self, context: Any) -> list:
        """Retrieve from local storage."""
        return [{"memory_id": "local_1", "content": "Local memory"}]


class CloudMemoryNode(IMemoryNode):
    """Cloud memory implementation."""
    
    def retrieve_memories(self, context: Any) -> list:
        """Retrieve from cloud storage."""
        return [{"memory_id": "cloud_1", "content": "Cloud memory"}]


class SequentialExecutor(IExecutor):
    """Sequential execution implementation."""
    
    def translate_plan(self, plan: Any, context: Any) -> list:
        """Translate for sequential execution."""
        return [{"action_id": "seq_1", "type": "sequential"}]


class ParallelExecutor(IExecutor):
    """Parallel execution implementation."""
    
    def translate_plan(self, plan: Any, context: Any) -> list:
        """Translate for parallel execution."""
        return [{"action_id": "par_1", "type": "parallel"}]


# ============================================================================
# Dependency Injection and Factory Patterns
# ============================================================================

class PlannerType(str, Enum):
    """Planner type enumeration."""
    BASIC = "basic"
    ADVANCED = "advanced"


class MemoryType(str, Enum):
    """Memory type enumeration."""
    LOCAL = "local"
    CLOUD = "cloud"


class ExecutorType(str, Enum):
    """Executor type enumeration."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class ComponentFactory:
    """
    Factory for creating component implementations.
    
    This demonstrates:
    - Factory pattern for implementation selection
    - Dependency injection setup
    - Configuration-based selection
    """
    
    @staticmethod
    def create_planner(planner_type: PlannerType = PlannerType.BASIC) -> IPlanner:
        """
        Create Planner implementation.
        
        Args:
            planner_type: Type of planner to create
            
        Returns:
            Planner implementation
        """
        planners = {
            PlannerType.BASIC: BasicPlanner,
            PlannerType.ADVANCED: AdvancedPlanner
        }
        planner_class = planners.get(planner_type, BasicPlanner)
        return planner_class()
    
    @staticmethod
    def create_memory_node(memory_type: MemoryType = MemoryType.LOCAL) -> IMemoryNode:
        """
        Create Memory Node implementation.
        
        Args:
            memory_type: Type of memory to create
            
        Returns:
            Memory Node implementation
        """
        memories = {
            MemoryType.LOCAL: LocalMemoryNode,
            MemoryType.CLOUD: CloudMemoryNode
        }
        memory_class = memories.get(memory_type, LocalMemoryNode)
        return memory_class()
    
    @staticmethod
    def create_executor(executor_type: ExecutorType = ExecutorType.SEQUENTIAL) -> IExecutor:
        """
        Create Executor implementation.
        
        Args:
            executor_type: Type of executor to create
            
        Returns:
            Executor implementation
        """
        executors = {
            ExecutorType.SEQUENTIAL: SequentialExecutor,
            ExecutorType.PARALLEL: ParallelExecutor
        }
        executor_class = executors.get(executor_type, SequentialExecutor)
        return executor_class()


# ============================================================================
# Dependency Injection Container
# ============================================================================

class DIContainer:
    """
    Dependency injection container.
    
    This demonstrates:
    - Dependency injection pattern
    - Component registration
    - Component resolution
    """
    
    def __init__(self):
        """Initialize container."""
        self._components: Dict[str, Any] = {}
    
    def register(self, interface: type, implementation: Any):
        """
        Register component implementation.
        
        Args:
            interface: Interface type
            implementation: Implementation instance
        """
        interface_name = interface.__name__
        self._components[interface_name] = implementation
    
    def resolve(self, interface: type) -> Any:
        """
        Resolve component implementation.
        
        Args:
            interface: Interface type to resolve
            
        Returns:
            Implementation instance
            
        Raises:
            ValueError: If component not registered
        """
        interface_name = interface.__name__
        if interface_name not in self._components:
            raise ValueError(f"Component {interface_name} not registered")
        return self._components[interface_name]


# ============================================================================
# A/B Testing Pattern
# ============================================================================

class ABTestingService:
    """
    Service for A/B testing different implementations.
    
    This demonstrates:
    - A/B testing pattern
    - Implementation comparison
    - Performance tracking
    """
    
    def __init__(self):
        """Initialize A/B testing service."""
        self.results: Dict[str, list] = {}
    
    def test_planners(self, user_request: Any, context: Any, 
                     iterations: int = 10) -> Dict[str, Any]:
        """
        A/B test different Planner implementations.
        
        Args:
            user_request: User request to test
            context: Planning context
            iterations: Number of test iterations
            
        Returns:
            Test results comparison
        """
        basic_planner = BasicPlanner()
        advanced_planner = AdvancedPlanner()
        
        basic_results = []
        advanced_results = []
        
        for i in range(iterations):
            with PerformanceTimer("ab_test_basic_planner", iteration=i) as t_basic:
                basic_plan = basic_planner.plan(user_request, context)
            basic_results.append({"time": t_basic.duration_seconds, "plan": basic_plan})

            with PerformanceTimer("ab_test_advanced_planner", iteration=i) as t_adv:
                advanced_plan = advanced_planner.plan(user_request, context)
            advanced_results.append({"time": t_adv.duration_seconds, "plan": advanced_plan})
        
        # Calculate statistics
        basic_avg_time = sum(r["time"] for r in basic_results) / len(basic_results)
        advanced_avg_time = sum(r["time"] for r in advanced_results) / len(advanced_results)
        
        return {
            "basic": {
                "avg_time": basic_avg_time,
                "results": basic_results
            },
            "advanced": {
                "avg_time": advanced_avg_time,
                "results": advanced_results
            },
            "recommendation": "basic" if basic_avg_time < advanced_avg_time else "advanced"
        }
    
    def swap_implementation(self, interface: type, new_implementation: Any, 
                          container: DIContainer):
        """
        Swap implementation at runtime.
        
        This demonstrates:
        - Runtime implementation swapping
        - Zero-downtime updates
        - Hot swapping
        
        Args:
            interface: Interface to swap
            new_implementation: New implementation
            container: DI container
        """
        container.register(interface, new_implementation)


# ============================================================================
# Usage Examples
# ============================================================================

def example_factory_usage():
    """Example of using factory pattern."""
    # Create components using factory
    planner = ComponentFactory.create_planner(PlannerType.ADVANCED)
    memory = ComponentFactory.create_memory_node(MemoryType.CLOUD)
    executor = ComponentFactory.create_executor(ExecutorType.PARALLEL)
    
    # Use components
    plan = planner.plan({"request": "test"}, {"context": "test"})
    memories = memory.retrieve_memories({"query": "test"})
    actions = executor.translate_plan(plan, {"context": "test"})


def example_di_usage():
    """Example of using dependency injection."""
    # Create container
    container = DIContainer()
    
    # Register implementations
    container.register(IPlanner, AdvancedPlanner())
    container.register(IMemoryNode, CloudMemoryNode())
    container.register(IExecutor, ParallelExecutor())
    
    # Resolve and use
    planner = container.resolve(IPlanner)
    plan = planner.plan({"request": "test"}, {"context": "test"})


def example_ab_testing():
    """Example of A/B testing."""
    ab_service = ABTestingService()
    results = ab_service.test_planners(
        {"request": "test"},
        {"context": "test"},
        iterations=10
    )
    
    # Use recommended implementation
    recommended = results["recommendation"]
    if recommended == "basic":
        planner = BasicPlanner()
    else:
        planner = AdvancedPlanner()
