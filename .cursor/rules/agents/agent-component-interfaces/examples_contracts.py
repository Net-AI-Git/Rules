"""
Input/Output Contracts Examples

This file demonstrates input/output contract definitions and validation patterns.
Reference this example from RULE.mdc using @examples_contracts.py syntax.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, validator
from dataclasses import dataclass


# ============================================================================
# Contract Data Models (Pydantic)
# ============================================================================

class UserRequest(BaseModel):
    """User request contract with validation."""
    request_id: str = Field(..., description="Unique request identifier")
    content: str = Field(..., description="User request content", min_length=1)
    context: Dict[str, Any] = Field(default_factory=dict, description="Request context")
    
    @validator('request_id')
    def validate_request_id(cls, v):
        """Validate request ID format."""
        if not v or len(v) < 3:
            raise ValueError("Request ID must be at least 3 characters")
        return v


class PlanningContext(BaseModel):
    """Planning context contract with validation."""
    user_id: str = Field(..., description="User identifier")
    available_resources: List[str] = Field(default_factory=list, description="Available resources")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Planning constraints")
    historical_context: Optional[Dict[str, Any]] = Field(None, description="Historical context")


class StrategicPlan(BaseModel):
    """Strategic plan contract with validation."""
    plan_id: str = Field(..., description="Plan identifier")
    goals: List[str] = Field(..., description="List of goals", min_items=1)
    action_sequence: List[str] = Field(..., description="Action sequence", min_items=1)
    risk_assessments: List[Dict[str, Any]] = Field(default_factory=list, description="Risk assessments")
    
    @validator('goals')
    def validate_goals(cls, v):
        """Validate goals are not empty."""
        if not v or any(not goal.strip() for goal in v):
            raise ValueError("Goals must be non-empty strings")
        return v


class ActionEvaluation(BaseModel):
    """Action evaluation contract with validation."""
    action_id: str = Field(..., description="Action identifier")
    risk_level: str = Field(..., description="Risk level", regex="^(low|medium|high|critical)$")
    cost_estimate: Dict[str, Any] = Field(..., description="Cost estimate")
    benefit_score: float = Field(..., description="Benefit score", ge=0.0, le=1.0)
    recommendation: bool = Field(..., description="Recommendation flag")


class MemoryContext(BaseModel):
    """Memory context contract with validation."""
    user_id: str = Field(..., description="User identifier")
    query: str = Field(..., description="Query for memory retrieval", min_length=1)
    top_k: int = Field(default=5, description="Number of memories to retrieve", ge=1, le=100)


class Experience(BaseModel):
    """Experience contract with validation."""
    experience_id: str = Field(..., description="Experience identifier")
    actions: List[Dict[str, Any]] = Field(..., description="Actions taken", min_items=1)
    context: Dict[str, Any] = Field(..., description="Context when actions occurred")
    results: Dict[str, Any] = Field(..., description="Results of actions")
    success: bool = Field(..., description="Success indicator")


class Feedback(BaseModel):
    """Feedback contract with validation."""
    feedback_id: str = Field(..., description="Feedback identifier")
    insights: List[str] = Field(..., description="Insights", min_items=0)
    patterns: List[str] = Field(..., description="Patterns", min_items=0)
    recommendations: List[str] = Field(..., description="Recommendations", min_items=0)
    confidence: float = Field(..., description="Confidence score", ge=0.0, le=1.0)


class ExecutionContext(BaseModel):
    """Execution context contract with validation."""
    user_id: str = Field(..., description="User identifier")
    available_workers: List[str] = Field(default_factory=list, description="Available workers")
    resource_limits: Dict[str, Any] = Field(default_factory=dict, description="Resource limits")


class ConcreteAction(BaseModel):
    """Concrete action contract with validation."""
    action_id: str = Field(..., description="Action identifier")
    action_type: str = Field(..., description="Action type")
    parameters: Dict[str, Any] = Field(..., description="Action parameters")
    dependencies: List[str] = Field(default_factory=list, description="Action dependencies")


class ActionResult(BaseModel):
    """Action result contract with validation."""
    action_id: str = Field(..., description="Action identifier")
    success: bool = Field(..., description="Success indicator")
    result_data: Dict[str, Any] = Field(..., description="Result data")
    error: Optional[str] = Field(None, description="Error message if failed")


# ============================================================================
# Contract Validation Service
# ============================================================================

class ContractValidationService:
    """
    Service for validating input/output contracts.
    
    This demonstrates:
    - Input validation at interface boundary
    - Output validation before returning
    - Pydantic model validation
    - Error handling for invalid contracts
    """
    
    def validate_planner_input(self, user_request: Dict[str, Any], 
                              context: Dict[str, Any]) -> tuple[UserRequest, PlanningContext]:
        """
        Validate Planner input contracts.
        
        Args:
            user_request: User request data
            context: Planning context data
            
        Returns:
            Validated UserRequest and PlanningContext
            
        Raises:
            ValueError: If validation fails
        """
        try:
            validated_request = UserRequest(**user_request)
            validated_context = PlanningContext(**context)
            return validated_request, validated_context
        except Exception as e:
            raise ValueError(f"Invalid Planner input: {str(e)}")
    
    def validate_planner_output(self, plan: Dict[str, Any]) -> StrategicPlan:
        """
        Validate Planner output contract.
        
        Args:
            plan: Strategic plan data
            
        Returns:
            Validated StrategicPlan
            
        Raises:
            ValueError: If validation fails
        """
        try:
            validated_plan = StrategicPlan(**plan)
            return validated_plan
        except Exception as e:
            raise ValueError(f"Invalid Planner output: {str(e)}")
    
    def validate_memory_input(self, context: Dict[str, Any]) -> MemoryContext:
        """
        Validate Memory Node input contract.
        
        Args:
            context: Memory context data
            
        Returns:
            Validated MemoryContext
            
        Raises:
            ValueError: If validation fails
        """
        try:
            validated_context = MemoryContext(**context)
            return validated_context
        except Exception as e:
            raise ValueError(f"Invalid Memory Node input: {str(e)}")
    
    def validate_memory_output(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate Memory Node output contract.
        
        Args:
            memories: List of memory data
            
        Returns:
            Validated memories
            
        Raises:
            ValueError: If validation fails
        """
        # Validate each memory has required fields
        for memory in memories:
            if not memory.get("memory_id"):
                raise ValueError("Memory must have memory_id")
            if not memory.get("content"):
                raise ValueError("Memory must have content")
            if "relevance_score" not in memory:
                raise ValueError("Memory must have relevance_score")
        
        return memories
    
    def validate_executor_input(self, plan: Dict[str, Any], 
                               context: Dict[str, Any]) -> Tuple[StrategicPlan, ExecutionContext]:
        """
        Validate Executor input contracts.
        
        Args:
            plan: Strategic plan data
            context: Execution context data
            
        Returns:
            Validated StrategicPlan and ExecutionContext
            
        Raises:
            ValueError: If validation fails
        """
        try:
            validated_plan = StrategicPlan(**plan)
            validated_context = ExecutionContext(**context)
            return validated_plan, validated_context
        except Exception as e:
            raise ValueError(f"Invalid Executor input: {str(e)}")
    
    def validate_executor_output(self, actions: List[Dict[str, Any]]) -> List[ConcreteAction]:
        """
        Validate Executor output contract.
        
        Args:
            actions: List of action data
            
        Returns:
            Validated ConcreteActions
            
        Raises:
            ValueError: If validation fails
        """
        validated_actions = []
        for action_data in actions:
            try:
                validated_action = ConcreteAction(**action_data)
                validated_actions.append(validated_action)
            except Exception as e:
                raise ValueError(f"Invalid action in Executor output: {str(e)}")
        
        return validated_actions
