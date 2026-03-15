"""
Component Interfaces Examples

This file demonstrates complete ABC interface definitions for Planner, Memory, and Executor components.
Reference this example from RULE.mdc using @examples_interfaces.py syntax.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


# ============================================================================
# Interface Data Types
# ============================================================================

@dataclass
class UserRequest:
    """User request structure."""
    request_id: str
    content: str
    context: Dict[str, Any]


@dataclass
class PlanningContext:
    """Planning context structure."""
    user_id: str
    available_resources: List[str]
    constraints: Dict[str, Any]
    historical_context: Optional[Dict[str, Any]] = None


@dataclass
class StrategicPlan:
    """Strategic plan structure."""
    plan_id: str
    goals: List[str]
    action_sequence: List[str]
    risk_assessments: List[Dict[str, Any]]


@dataclass
class Action:
    """Action structure."""
    action_id: str
    action_type: str
    parameters: Dict[str, Any]


@dataclass
class ActionEvaluation:
    """Action evaluation structure."""
    action_id: str
    risk_level: str
    cost_estimate: Dict[str, Any]
    benefit_score: float
    recommendation: bool


@dataclass
class Goals:
    """Goals structure."""
    main_goals: List[str]
    sub_goals: List[str]
    constraints: List[str]


@dataclass
class MemoryContext:
    """Memory context structure."""
    user_id: str
    query: str
    top_k: int = 5


@dataclass
class Memory:
    """Memory structure."""
    memory_id: str
    content: str
    relevance_score: float
    metadata: Dict[str, Any]


@dataclass
class Experience:
    """Experience structure."""
    experience_id: str
    actions: List[Dict[str, Any]]
    context: Dict[str, Any]
    results: Dict[str, Any]
    success: bool


@dataclass
class Feedback:
    """Feedback structure."""
    feedback_id: str
    insights: List[str]
    patterns: List[str]
    recommendations: List[str]
    confidence: float


@dataclass
class ExecutionContext:
    """Execution context structure."""
    user_id: str
    available_workers: List[str]
    resource_limits: Dict[str, Any]


@dataclass
class ConcreteAction:
    """Concrete action structure."""
    action_id: str
    action_type: str
    parameters: Dict[str, Any]
    dependencies: List[str]


@dataclass
class ActionResult:
    """Action result structure."""
    action_id: str
    success: bool
    result_data: Dict[str, Any]
    error: Optional[str] = None


@dataclass
class ExecutionStatus:
    """Execution status structure."""
    status: str
    completed_actions: int
    total_actions: int
    results: List[ActionResult]


# ============================================================================
# Component Interfaces
# ============================================================================

class IPlanner(ABC):
    """
    Planner interface using ABC.
    
    This demonstrates:
    - Abstract base class definition
    - Required method signatures
    - Interface contract enforcement
    """
    
    @abstractmethod
    def plan(self, user_request: UserRequest, context: PlanningContext) -> StrategicPlan:
        """
        Create strategic plan from user request.
        
        Args:
            user_request: User's request
            context: Planning context
            
        Returns:
            Strategic plan with goals and actions
        """
        pass
    
    @abstractmethod
    def evaluate_actions(self, actions: List[Action], 
                        context: PlanningContext) -> List[ActionEvaluation]:
        """
        Evaluate actions by risk, cost, and benefit.
        
        Args:
            actions: Actions to evaluate
            context: Planning context
            
        Returns:
            List of action evaluations
        """
        pass
    
    @abstractmethod
    def set_goals(self, user_request: UserRequest) -> Goals:
        """
        Set goals and sub-goals from user request.
        
        Args:
            user_request: User's request
            
        Returns:
            Goals structure
        """
        pass


class IMemoryNode(ABC):
    """
    Memory Node interface using ABC.
    
    This demonstrates:
    - Abstract base class definition
    - Required method signatures
    - Interface contract enforcement
    """
    
    @abstractmethod
    def retrieve_memories(self, context: MemoryContext) -> List[Memory]:
        """
        Retrieve relevant memories.
        
        Args:
            context: Memory context
            
        Returns:
            List of relevant memories
        """
        pass
    
    @abstractmethod
    def store_experience(self, experience: Experience, 
                        context: MemoryContext) -> str:
        """
        Store experience for future learning.
        
        Args:
            experience: Experience to store
            context: Memory context
            
        Returns:
            Memory ID of stored experience
        """
        pass
    
    @abstractmethod
    def provide_feedback(self, plan: StrategicPlan, 
                         context: MemoryContext) -> Feedback:
        """
        Provide feedback to Planner.
        
        Args:
            plan: Strategic plan to provide feedback on
            context: Memory context
            
        Returns:
            Feedback for Planner
        """
        pass


class IExecutor(ABC):
    """
    Executor interface using ABC.
    
    This demonstrates:
    - Abstract base class definition
    - Required method signatures
    - Interface contract enforcement
    """
    
    @abstractmethod
    def translate_plan(self, plan: StrategicPlan, 
                      context: ExecutionContext) -> List[ConcreteAction]:
        """
        Translate strategic plan to concrete actions.
        
        Args:
            plan: Strategic plan
            context: Execution context
            
        Returns:
            List of concrete actions
        """
        pass
    
    @abstractmethod
    def execute_action(self, action: ConcreteAction, 
                        context: ExecutionContext) -> ActionResult:
        """
        Execute a concrete action.
        
        Args:
            action: Action to execute
            context: Execution context
            
        Returns:
            Action result
        """
        pass
    
    @abstractmethod
    def monitor_execution(self, actions: List[ConcreteAction]) -> ExecutionStatus:
        """
        Monitor execution of actions.
        
        Args:
            actions: Actions being executed
            
        Returns:
            Execution status
        """
        pass


# ============================================================================
# Example Implementations
# ============================================================================

class BasicPlanner(IPlanner):
    """
    Basic Planner implementation.
    
    This demonstrates:
    - Implementing interface
    - Providing concrete implementation
    - Maintaining interface contract
    """
    
    def plan(self, user_request: UserRequest, context: PlanningContext) -> StrategicPlan:
        """Create strategic plan."""
        return StrategicPlan(
            plan_id="plan_1",
            goals=["Complete user request"],
            action_sequence=["action_1", "action_2"],
            risk_assessments=[]
        )
    
    def evaluate_actions(self, actions: List[Action], 
                        context: PlanningContext) -> List[ActionEvaluation]:
        """Evaluate actions."""
        return [
            ActionEvaluation(
                action_id=action.action_id,
                risk_level="medium",
                cost_estimate={"tokens": 1000},
                benefit_score=0.8,
                recommendation=True
            )
            for action in actions
        ]
    
    def set_goals(self, user_request: UserRequest) -> Goals:
        """Set goals."""
        return Goals(
            main_goals=["Complete request"],
            sub_goals=["Understand", "Plan", "Execute"],
            constraints=[]
        )


class BasicMemoryNode(IMemoryNode):
    """
    Basic Memory Node implementation.
    
    This demonstrates:
    - Implementing interface
    - Providing concrete implementation
    - Maintaining interface contract
    """
    
    def retrieve_memories(self, context: MemoryContext) -> List[Memory]:
        """Retrieve memories."""
        return [
            Memory(
                memory_id="mem_1",
                content="Example memory",
                relevance_score=0.8,
                metadata={}
            )
        ]
    
    def store_experience(self, experience: Experience, 
                        context: MemoryContext) -> str:
        """Store experience."""
        return "memory_id_1"
    
    def provide_feedback(self, plan: StrategicPlan, 
                         context: MemoryContext) -> Feedback:
        """Provide feedback."""
        return Feedback(
            feedback_id="feedback_1",
            insights=["Insight 1"],
            patterns=["Pattern 1"],
            recommendations=["Recommendation 1"],
            confidence=0.8
        )


class BasicExecutor(IExecutor):
    """
    Basic Executor implementation.
    
    This demonstrates:
    - Implementing interface
    - Providing concrete implementation
    - Maintaining interface contract
    """
    
    def translate_plan(self, plan: StrategicPlan, 
                      context: ExecutionContext) -> List[ConcreteAction]:
        """Translate plan to actions."""
        return [
            ConcreteAction(
                action_id=f"action_{i}",
                action_type="api_call",
                parameters={},
                dependencies=[]
            )
            for i, action_name in enumerate(plan.action_sequence)
        ]
    
    def execute_action(self, action: ConcreteAction, 
                      context: ExecutionContext) -> ActionResult:
        """Execute action."""
        return ActionResult(
            action_id=action.action_id,
            success=True,
            result_data={"status": "success"}
        )
    
    def monitor_execution(self, actions: List[ConcreteAction]) -> ExecutionStatus:
        """Monitor execution."""
        return ExecutionStatus(
            status="completed",
            completed_actions=len(actions),
            total_actions=len(actions),
            results=[]
        )
