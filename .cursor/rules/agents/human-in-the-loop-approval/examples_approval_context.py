"""
Approval Context Examples

This file demonstrates Approval Context Schema patterns and builder implementation.
Reference this example from RULE.mdc using @examples_approval_context.py syntax.
"""

from typing import TypedDict, Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Approval Context Schema
# ============================================================================

class RiskLevel(Enum):
    """
    Risk levels for approval requests.
    
    This demonstrates risk classification:
    - Low: Read-only, non-destructive, low-cost
    - Medium: Write with rollback, moderate cost
    - High: Destructive, high cost, irreversible
    - Critical: System-level, production, security, financial
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalContext(TypedDict, total=False):
    """
    Approval Context Schema.
    
    This demonstrates the mandatory approval context structure:
    - Required fields: risk_level, estimated_cost, proposed_diff, etc.
    - Optional fields: alternatives, impact_analysis, rollback_plan
    """
    # Required fields
    risk_level: str  # RiskLevel enum value
    estimated_cost: float  # USD
    proposed_diff: Dict[str, Any]  # Structured diff
    action_description: str  # Human-readable description
    current_state_snapshot: Dict[str, Any]  # State before action
    approval_required_by: Optional[str]  # ISO datetime string
    
    # Optional fields
    alternatives: List[Dict[str, Any]]  # Alternative actions
    impact_analysis: Dict[str, Any]  # Impact assessment
    rollback_plan: Dict[str, Any]  # Rollback strategy
    approval_history: List[Dict[str, Any]]  # Previous approvals


# ============================================================================
# Risk Assessment
# ============================================================================

@dataclass
class RiskFactors:
    """
    Risk factors for assessment.
    
    This demonstrates risk factor structure:
    - Action type, cost magnitude, reversibility, impact scope
    """
    action_type: str  # "read" | "write" | "delete" | "system_change"
    cost_magnitude: str  # "low" | "medium" | "high" | "critical"
    reversibility: str  # "fully_reversible" | "partially_reversible" | "irreversible"
    impact_scope: str  # "single_user" | "multiple_users" | "system_wide"
    data_sensitivity: str  # "public" | "internal" | "confidential" | "critical"


class RiskAssessor:
    """
    Service for assessing risk levels.
    
    This demonstrates risk assessment patterns:
    - Calculate risk based on multiple factors
    - Escalate risk when multiple high-risk factors present
    - Return RiskLevel enum
    """
    
    def assess_risk(self, factors: RiskFactors) -> RiskLevel:
        """
        Assess risk level from factors.
        
        Args:
            factors: Risk factors
        
        Returns:
            RiskLevel
        """
        # Base risk from action type
        action_risk = self._get_action_risk(factors.action_type)
        
        # Cost risk
        cost_risk = self._get_cost_risk(factors.cost_magnitude)
        
        # Reversibility risk
        reversibility_risk = self._get_reversibility_risk(factors.reversibility)
        
        # Impact risk
        impact_risk = self._get_impact_risk(factors.impact_scope)
        
        # Data sensitivity risk
        sensitivity_risk = self._get_sensitivity_risk(factors.data_sensitivity)
        
        # Take highest risk as base
        base_risk = max(
            action_risk,
            cost_risk,
            reversibility_risk,
            impact_risk,
            sensitivity_risk
        )
        
        # Escalate if multiple high-risk factors
        high_risk_count = sum([
            1 for risk in [action_risk, cost_risk, reversibility_risk, impact_risk, sensitivity_risk]
            if risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        ])
        
        if high_risk_count >= 3 and base_risk == RiskLevel.HIGH:
            return RiskLevel.CRITICAL
        
        return base_risk
    
    def _get_action_risk(self, action_type: str) -> RiskLevel:
        """Get risk from action type."""
        risk_map = {
            "read": RiskLevel.LOW,
            "write": RiskLevel.MEDIUM,
            "delete": RiskLevel.HIGH,
            "system_change": RiskLevel.CRITICAL
        }
        return risk_map.get(action_type, RiskLevel.MEDIUM)
    
    def _get_cost_risk(self, cost_magnitude: str) -> RiskLevel:
        """Get risk from cost magnitude."""
        risk_map = {
            "low": RiskLevel.LOW,
            "medium": RiskLevel.MEDIUM,
            "high": RiskLevel.HIGH,
            "critical": RiskLevel.CRITICAL
        }
        return risk_map.get(cost_magnitude, RiskLevel.MEDIUM)
    
    def _get_reversibility_risk(self, reversibility: str) -> RiskLevel:
        """Get risk from reversibility."""
        risk_map = {
            "fully_reversible": RiskLevel.LOW,
            "partially_reversible": RiskLevel.MEDIUM,
            "irreversible": RiskLevel.HIGH
        }
        return risk_map.get(reversibility, RiskLevel.MEDIUM)
    
    def _get_impact_risk(self, impact_scope: str) -> RiskLevel:
        """Get risk from impact scope."""
        risk_map = {
            "single_user": RiskLevel.LOW,
            "multiple_users": RiskLevel.MEDIUM,
            "system_wide": RiskLevel.HIGH
        }
        return risk_map.get(impact_scope, RiskLevel.MEDIUM)
    
    def _get_sensitivity_risk(self, data_sensitivity: str) -> RiskLevel:
        """Get risk from data sensitivity."""
        risk_map = {
            "public": RiskLevel.LOW,
            "internal": RiskLevel.LOW,
            "confidential": RiskLevel.MEDIUM,
            "critical": RiskLevel.HIGH
        }
        return risk_map.get(data_sensitivity, RiskLevel.LOW)


# ============================================================================
# Cost Estimation
# ============================================================================

class CostEstimator:
    """
    Service for estimating action costs.
    
    This demonstrates cost estimation patterns:
    - Estimate LLM costs
    - Estimate tool costs
    - Estimate time costs
    - Return total estimated cost
    """
    
    def estimate_cost(
        self,
        action_type: str,
        model_name: Optional[str] = None,
        estimated_tokens: Optional[int] = None,
        tool_costs: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Estimate total cost for action.
        
        Args:
            action_type: Type of action
            model_name: LLM model name (if LLM call)
            estimated_tokens: Estimated token count (if LLM call)
            tool_costs: Dictionary of tool costs
        
        Returns:
            Estimated cost in USD
        """
        total_cost = 0.0
        
        # Estimate LLM costs
        if model_name and estimated_tokens:
            llm_cost = self._estimate_llm_cost(model_name, estimated_tokens)
            total_cost += llm_cost
        
        # Estimate tool costs
        if tool_costs:
            total_cost += sum(tool_costs.values())
        
        # Add overhead (10% buffer)
        total_cost *= 1.1
        
        return total_cost
    
    def _estimate_llm_cost(self, model_name: str, tokens: int) -> float:
        """Estimate LLM cost."""
        # Simplified pricing (in real implementation, use pricing registry)
        pricing = {
            "gpt-4": 0.03 / 1000,  # per 1K tokens
            "gpt-4-turbo": 0.01 / 1000,
            "gpt-3.5-turbo": 0.0005 / 1000,
            "claude-opus": 0.015 / 1000,
            "claude-sonnet": 0.003 / 1000,
            "claude-haiku": 0.00025 / 1000
        }
        
        price_per_1k = pricing.get(model_name, 0.01 / 1000)
        return (tokens / 1000) * price_per_1k


# ============================================================================
# Approval Context Builder
# ============================================================================

class ApprovalContextBuilder:
    """
    Builder for creating Approval Context objects.
    
    This demonstrates approval context construction:
    - Build required fields
    - Calculate risk and cost
    - Create structured proposed_diff
    - Validate completeness
    """
    
    def __init__(
        self,
        risk_assessor: RiskAssessor,
        cost_estimator: CostEstimator
    ):
        """
        Initialize builder.
        
        Args:
            risk_assessor: Risk assessor service
            cost_estimator: Cost estimator service
        """
        self.risk_assessor = risk_assessor
        self.cost_estimator = cost_estimator
    
    def build(
        self,
        action_description: str,
        proposed_diff: Dict[str, Any],
        current_state: Dict[str, Any],
        risk_factors: RiskFactors,
        model_name: Optional[str] = None,
        estimated_tokens: Optional[int] = None,
        tool_costs: Optional[Dict[str, float]] = None,
        approval_required_by: Optional[datetime] = None,
        alternatives: Optional[List[Dict[str, Any]]] = None
    ) -> ApprovalContext:
        """
        Build Approval Context.
        
        Args:
            action_description: Human-readable description
            proposed_diff: Structured diff
            current_state: Current state snapshot
            risk_factors: Risk factors for assessment
            model_name: LLM model (if applicable)
            estimated_tokens: Estimated tokens (if applicable)
            tool_costs: Tool costs (if applicable)
            approval_required_by: Approval deadline
            alternatives: Alternative actions
        
        Returns:
            ApprovalContext
        """
        # Assess risk
        risk_level = self.risk_assessor.assess_risk(risk_factors)
        
        # Estimate cost
        estimated_cost = self.cost_estimator.estimate_cost(
            action_type=risk_factors.action_type,
            model_name=model_name,
            estimated_tokens=estimated_tokens,
            tool_costs=tool_costs
        )
        
        # Build context
        context: ApprovalContext = {
            "risk_level": risk_level.value,
            "estimated_cost": estimated_cost,
            "proposed_diff": proposed_diff,
            "action_description": action_description,
            "current_state_snapshot": current_state,
            "approval_required_by": approval_required_by.isoformat() if approval_required_by else None
        }
        
        # Add optional fields
        if alternatives:
            context["alternatives"] = alternatives
        
        return context


# ============================================================================
# Worker Node Integration
# ============================================================================

def create_approval_context_for_worker_action(
    action_type: str,
    action_description: str,
    proposed_changes: Dict[str, Any],
    current_state: Dict[str, Any],
    model_name: Optional[str] = None,
    estimated_tokens: Optional[int] = None
) -> ApprovalContext:
    """
    Create Approval Context for worker action.
    
    This demonstrates approval context creation in Worker Nodes:
    - Assess risk factors
    - Estimate cost
    - Build structured diff
    - Create approval context
    
    Args:
        action_type: Type of action
        action_description: Description
        proposed_changes: Proposed changes
        current_state: Current state
        model_name: Model name (if LLM call)
        estimated_tokens: Estimated tokens (if LLM call)
    
    Returns:
        ApprovalContext
    """
    # Initialize services
    risk_assessor = RiskAssessor()
    cost_estimator = CostEstimator()
    builder = ApprovalContextBuilder(risk_assessor, cost_estimator)
    
    # Determine risk factors (in real implementation, analyze from context)
    risk_factors = RiskFactors(
        action_type=action_type,
        cost_magnitude="medium",  # Would be calculated from estimated_cost
        reversibility="partially_reversible",
        impact_scope="single_user",
        data_sensitivity="internal"
    )
    
    # Build proposed diff
    proposed_diff = {
        "action": action_type,
        "changes": proposed_changes,
        "target": current_state.get("target_resource", "unknown")
    }
    
    # Build approval context
    approval_context = builder.build(
        action_description=action_description,
        proposed_diff=proposed_diff,
        current_state=current_state,
        risk_factors=risk_factors,
        model_name=model_name,
        estimated_tokens=estimated_tokens
    )
    
    return approval_context


# ============================================================================
# Interrupt Node Integration
# ============================================================================

def interrupt_node_with_approval(
    state: Dict[str, Any],
    approval_context: ApprovalContext
) -> Dict[str, Any]:
    """
    Interrupt Node that uses Approval Context.
    
    This demonstrates interrupt node pattern:
    - Receive Approval Context from Worker
    - Send to human for review
    - Wait for approval decision
    - Update state with decision
    
    Args:
        state: GraphState
        approval_context: Approval Context
    
    Returns:
        Updated GraphState
    """
    # Store approval context in state
    state["approval_context"] = approval_context
    state["approval_status"] = "pending"
    
    # In real implementation:
    # 1. Send approval_context to human (via UI, email, etc.)
    # 2. Wait for human decision
    # 3. Receive approval/rejection
    # 4. Update state with decision
    
    # For example:
    # approval_decision = await wait_for_human_approval(approval_context)
    # state["approval_status"] = approval_decision["status"]  # "approved" | "rejected"
    # state["approval_reasoning"] = approval_decision.get("reasoning")
    
    return state


# ============================================================================
# Example: Complete Workflow
# ============================================================================

def example_worker_to_approval_workflow():
    """
    Example workflow: Worker → Approval → Execution.
    
    This demonstrates complete approval workflow:
    - Worker identifies need for approval
    - Creates Approval Context
    - Sends to Interrupt Node
    - Human reviews and approves
    - Workflow continues
    """
    # Worker Node identifies need for approval
    action_description = "Update user status to 'active' in database"
    proposed_changes = {"status": "active"}
    current_state = {
        "user_id": 123,
        "current_status": "inactive",
        "target_resource": "users"
    }
    
    # Create Approval Context
    approval_context = create_approval_context_for_worker_action(
        action_type="write",
        action_description=action_description,
        proposed_changes=proposed_changes,
        current_state=current_state
    )
    
    # Send to Interrupt Node
    state = {"user_id": 123}
    state = interrupt_node_with_approval(state, approval_context)
    
    # In real workflow:
    # - Human reviews approval_context
    # - Human approves/rejects
    # - Workflow continues based on decision
    
    return state
