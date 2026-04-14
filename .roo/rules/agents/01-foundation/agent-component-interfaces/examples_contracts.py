"""
Input/Output contract examples (Pydantic v2).

Validates payloads at component boundaries. In production, pair with
@monitoring-and-observability and @audit-protocol for Splunk HEC events.

Reference from RULE.mdc: @examples_contracts.py
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Contract models (Pydantic v2)
# -----------------------------------------------------------------------------


class UserRequest(BaseModel):
    """User request contract with validation."""

    model_config = {"extra": "forbid"}

    request_id: str = Field(..., description="Unique request identifier")
    content: str = Field(..., description="User request content", min_length=1)
    context: Dict[str, Any] = Field(default_factory=dict, description="Request context")

    @field_validator("request_id")
    @classmethod
    def request_id_min_length(cls, v: str) -> str:
        if not v or len(v) < 3:
            raise ValueError("Request ID must be at least 3 characters")
        return v


class PlanningContext(BaseModel):
    model_config = {"extra": "forbid"}

    user_id: str = Field(..., description="User identifier")
    available_resources: List[str] = Field(default_factory=list, description="Available resources")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Planning constraints")
    historical_context: Optional[Dict[str, Any]] = Field(None, description="Historical context")


class StrategicPlan(BaseModel):
    model_config = {"extra": "forbid"}

    plan_id: str = Field(..., description="Plan identifier")
    goals: List[str] = Field(..., description="List of goals", min_length=1)
    action_sequence: List[str] = Field(..., description="Action sequence", min_length=1)
    risk_assessments: List[Dict[str, Any]] = Field(default_factory=list, description="Risk assessments")

    @field_validator("goals")
    @classmethod
    def goals_non_empty_strings(cls, v: List[str]) -> List[str]:
        if not v or any(not g.strip() for g in v):
            raise ValueError("Goals must be non-empty strings")
        return v


class ActionEvaluation(BaseModel):
    model_config = {"extra": "forbid"}

    action_id: str = Field(..., description="Action identifier")
    risk_level: str = Field(
        ...,
        description="Risk level",
        pattern="^(low|medium|high|critical)$",
    )
    cost_estimate: Dict[str, Any] = Field(..., description="Cost estimate")
    benefit_score: float = Field(..., description="Benefit score", ge=0.0, le=1.0)
    recommendation: bool = Field(..., description="Recommendation flag")


class MemoryContext(BaseModel):
    model_config = {"extra": "forbid"}

    user_id: str = Field(..., description="User identifier")
    query: str = Field(..., description="Query for memory retrieval", min_length=1)
    top_k: int = Field(default=5, description="Number of memories to retrieve", ge=1, le=100)


class Experience(BaseModel):
    model_config = {"extra": "forbid"}

    experience_id: str = Field(..., description="Experience identifier")
    actions: List[Dict[str, Any]] = Field(..., description="Actions taken", min_length=1)
    context: Dict[str, Any] = Field(..., description="Context when actions occurred")
    results: Dict[str, Any] = Field(..., description="Results of actions")
    success: bool = Field(..., description="Success indicator")


class Feedback(BaseModel):
    model_config = {"extra": "forbid"}

    feedback_id: str = Field(..., description="Feedback identifier")
    insights: List[str] = Field(default_factory=list, description="Insights")
    patterns: List[str] = Field(default_factory=list, description="Patterns")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    confidence: float = Field(..., description="Confidence score", ge=0.0, le=1.0)


class ExecutionContext(BaseModel):
    model_config = {"extra": "forbid"}

    user_id: str = Field(..., description="User identifier")
    available_workers: List[str] = Field(default_factory=list, description="Available workers")
    resource_limits: Dict[str, Any] = Field(default_factory=dict, description="Resource limits")


class ConcreteAction(BaseModel):
    model_config = {"extra": "forbid"}

    action_id: str = Field(..., description="Action identifier")
    action_type: str = Field(..., description="Action type")
    parameters: Dict[str, Any] = Field(..., description="Action parameters")
    dependencies: List[str] = Field(default_factory=list, description="Action dependencies")


class ActionResult(BaseModel):
    model_config = {"extra": "forbid"}

    action_id: str = Field(..., description="Action identifier")
    success: bool = Field(..., description="Success indicator")
    result_data: Dict[str, Any] = Field(..., description="Result data")
    error: Optional[str] = Field(None, description="Error message if failed")


# -----------------------------------------------------------------------------
# Boundary validation service (example)
# -----------------------------------------------------------------------------


class ContractValidationService:
    """Validate dict payloads into contracts at Planner / Memory / Executor edges."""

    def validate_planner_input(
        self, user_request: Dict[str, Any], context: Dict[str, Any]
    ) -> Tuple[UserRequest, PlanningContext]:
        try:
            return UserRequest(**user_request), PlanningContext(**context)
        except Exception as e:
            logger.warning(json.dumps({"event": "planner_input_validation_failed", "error": str(e)}))
            raise ValueError(f"Invalid Planner input: {e}") from e

    def validate_planner_output(self, plan: Dict[str, Any]) -> StrategicPlan:
        try:
            return StrategicPlan(**plan)
        except Exception as e:
            logger.warning(json.dumps({"event": "planner_output_validation_failed", "error": str(e)}))
            raise ValueError(f"Invalid Planner output: {e}") from e

    def validate_memory_input(self, context: Dict[str, Any]) -> MemoryContext:
        try:
            return MemoryContext(**context)
        except Exception as e:
            raise ValueError(f"Invalid Memory Node input: {e}") from e

    def validate_memory_output(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for memory in memories:
            if not memory.get("memory_id"):
                raise ValueError("Memory must have memory_id")
            if not memory.get("content"):
                raise ValueError("Memory must have content")
            if "relevance_score" not in memory:
                raise ValueError("Memory must have relevance_score")
        return memories

    def validate_executor_input(
        self, plan: Dict[str, Any], context: Dict[str, Any]
    ) -> Tuple[StrategicPlan, ExecutionContext]:
        try:
            return StrategicPlan(**plan), ExecutionContext(**context)
        except Exception as e:
            raise ValueError(f"Invalid Executor input: {e}") from e

    def validate_executor_output(self, actions: List[Dict[str, Any]]) -> List[ConcreteAction]:
        out: List[ConcreteAction] = []
        for action_data in actions:
            try:
                out.append(ConcreteAction(**action_data))
            except Exception as e:
                raise ValueError(f"Invalid action in Executor output: {e}") from e
        return out
