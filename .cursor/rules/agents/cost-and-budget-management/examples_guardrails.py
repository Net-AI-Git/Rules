"""
Guardrail Enforcement Examples

This file demonstrates threshold checking and graceful degradation patterns.
Reference this example from RULE.mdc using @examples_guardrails.py syntax.
"""

from typing import TypedDict, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass

# Note: In actual implementation, import from your actual modules
# from your_project.budget import BudgetState, CostTracker
# For this example, we reference the types from examples_budget_state.py
# In a real implementation, these would be in shared modules
from typing import TypedDict, Dict, Any, Optional

# Type alias - in real implementation, import from shared module
BudgetState = TypedDict('BudgetState', {
    'total_cost_usd': float,
    'budget_limit_usd': float,
    'budget_exceeded': bool,
    # ... other fields
}, total=False)

# CostTracker would be imported from actual implementation
# For this example, we use a type hint
CostTracker = Any


# ============================================================================
# Guardrail Enforcement
# ============================================================================

class GuardrailAction(Enum):
    """
    Actions to take when budget thresholds are reached.
    
    This demonstrates guardrail action types:
    - CONTINUE: Continue normal operation
    - WARN: Log warning but continue
    - DEGRADE: Switch to cheaper models/reduced context
    - HALT: Stop execution immediately
    """
    CONTINUE = "continue"
    WARN = "warn"
    DEGRADE = "degrade"
    HALT = "halt"


@dataclass
class GuardrailConfig:
    """
    Configuration for budget guardrails.
    
    This demonstrates guardrail configuration:
    - Multiple threshold levels
    - Actions per threshold
    - Graceful degradation options
    """
    warning_threshold: float = 0.8  # 80% of budget
    soft_limit_threshold: float = 0.9  # 90% of budget
    hard_limit_threshold: float = 1.0  # 100% of budget
    
    enable_graceful_degradation: bool = True
    fallback_model: Optional[str] = None  # e.g., "gpt-3.5-turbo" or "claude-haiku"
    reduce_context_on_degradation: bool = True
    context_reduction_factor: float = 0.5  # Reduce to 50% of original


class BudgetGuardrail:
    """
    Budget guardrail enforcement service.
    
    This demonstrates guardrail enforcement:
    - Threshold checking
    - Action determination
    - Graceful degradation
    - Hard halt on budget exceeded
    """
    
    def __init__(
        self,
        cost_tracker: CostTracker,
        config: Optional[GuardrailConfig] = None
    ):
        """
        Initialize budget guardrail.
        
        Args:
            cost_tracker: Cost tracker instance
            config: Guardrail configuration
        """
        self.cost_tracker = cost_tracker
        self.config = config or GuardrailConfig()
    
    def check_guardrail(self, state: BudgetState) -> GuardrailAction:
        """
        Check budget status and determine guardrail action.
        
        Args:
            state: Current budget state
            
        Returns:
            GuardrailAction to take
        """
        status = self.cost_tracker.check_budget_status(state)
        
        if status["is_exceeded"]:
            return GuardrailAction.HALT
        
        if status["budget_usage_percent"] >= self.config.hard_limit_threshold:
            return GuardrailAction.HALT
        
        if status["budget_usage_percent"] >= self.config.soft_limit_threshold:
            if self.config.enable_graceful_degradation:
                return GuardrailAction.DEGRADE
            return GuardrailAction.HALT
        
        if status["is_warning"]:
            return GuardrailAction.WARN
        
        return GuardrailAction.CONTINUE
    
    def should_halt(self, state: BudgetState) -> bool:
        """
        Check if execution should be halted.
        
        Args:
            state: Current budget state
            
        Returns:
            True if execution should halt
        """
        action = self.check_guardrail(state)
        return action == GuardrailAction.HALT
    
    def get_degradation_config(self, state: BudgetState) -> Optional[Dict[str, Any]]:
        """
        Get configuration for graceful degradation.
        
        Args:
            state: Current budget state
            
        Returns:
            Degradation configuration or None if not needed
        """
        action = self.check_guardrail(state)
        
        if action != GuardrailAction.DEGRADE:
            return None
        
        config = {}
        
        # Switch to cheaper model
        if self.config.fallback_model:
            config["model"] = self.config.fallback_model
        
        # Reduce context window
        if self.config.reduce_context_on_degradation:
            config["max_context_tokens"] = int(
                state.get("max_context_tokens", 8000) * 
                self.config.context_reduction_factor
            )
        
        return config
    
    def create_budget_exceeded_error(self, state: BudgetState) -> Dict[str, Any]:
        """
        Create error response for budget exceeded.
        
        Args:
            state: Current budget state
            
        Returns:
            Error response dictionary
        """
        status = self.cost_tracker.check_budget_status(state)
        
        return {
            "error": "budget_exceeded",
            "message": f"Budget limit of ${state.get('budget_limit_usd', 0):.2f} exceeded. Current cost: ${status['budget_used']:.2f}",
            "budget_limit_usd": state.get("budget_limit_usd", 0),
            "current_cost_usd": status["budget_used"],
            "budget_usage_percent": status["budget_usage_percent"],
            "suggestion": "Retry with a higher budget limit or simplify your request",
            "state_preserved": True  # Indicate state can be resumed
        }


# ============================================================================
# LangGraph Node Integration
# ============================================================================

def budget_aware_node(
    state: BudgetState,
    cost_tracker: CostTracker,
    guardrail: BudgetGuardrail,
    node_name: str,
    llm_call_func,
    *args,
    **kwargs
) -> BudgetState:
    """
    Wrapper for LLM calls that enforces budget guardrails.
    
    This demonstrates budget-aware node pattern:
    - Check budget before LLM call
    - Track costs after call
    - Enforce guardrails
    - Handle budget exceeded errors
    
    Args:
        state: Current graph state
        cost_tracker: Cost tracker instance
        guardrail: Budget guardrail instance
        node_name: Name of the node
        llm_call_func: Function that makes LLM call
        *args: Arguments for LLM call
        **kwargs: Keyword arguments for LLM call
        
    Returns:
        Updated state
        
    Raises:
        BudgetExceededError: If budget is exceeded
    """
    # Check if we should halt
    if guardrail.should_halt(state):
        error = guardrail.create_budget_exceeded_error(state)
        raise ValueError(f"Budget exceeded: {error['message']}")
    
    # Check for graceful degradation
    degradation_config = guardrail.get_degradation_config(state)
    if degradation_config:
        # Apply degradation (e.g., switch model, reduce context)
        if "model" in degradation_config:
            kwargs["model"] = degradation_config["model"]
        if "max_context_tokens" in degradation_config:
            kwargs["max_context_tokens"] = degradation_config["max_context_tokens"]
    
    # Make LLM call
    result = llm_call_func(*args, **kwargs)
    
    # Extract token usage (this would come from LLM response metadata)
    # In real implementation, this would be from the LLM SDK response
    model_name = kwargs.get("model", "unknown")
    input_tokens = result.get("usage", {}).get("prompt_tokens", 0)
    output_tokens = result.get("usage", {}).get("completion_tokens", 0)
    
    # Update budget state
    state = cost_tracker.update_budget_state(
        state=state,
        model_name=model_name,
        node_name=node_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    
    # Check again after update (in case this call exceeded budget)
    if guardrail.should_halt(state):
        error = guardrail.create_budget_exceeded_error(state)
        raise ValueError(f"Budget exceeded: {error['message']}")
    
    return state


# ============================================================================
# Conditional Routing Example
# ============================================================================

def budget_aware_router(
    state: BudgetState,
    cost_tracker: 'CostTracker',
    guardrail: 'BudgetGuardrail'
) -> str:
    """
    Conditional router that considers budget status.
    
    This demonstrates budget-aware routing:
    - Route to cheaper nodes when budget is low
    - Route to halt node when budget exceeded
    - Route normally when budget is healthy
    
    Args:
        state: Current graph state
        cost_tracker: Cost tracker instance
        guardrail: Budget guardrail instance
        
    Returns:
        Next node name
    """
    action = guardrail.check_guardrail(state)
    
    if action == GuardrailAction.HALT:
        return "halt_node"
    elif action == GuardrailAction.DEGRADE:
        return "degraded_processing_node"
    else:
        return "normal_processing_node"


# ============================================================================
# Pre-Call Budget Checking
# ============================================================================

@dataclass
class EstimatedCallCost:
    """
    Estimated cost for an upcoming LLM call.
    
    This demonstrates cost estimation:
    - Model name
    - Estimated input/output tokens
    - Estimated total cost
    """
    model_name: str
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_cost_usd: float


def check_budget_before_llm_call(
    state: BudgetState,
    cost_tracker: CostTracker,
    guardrail: BudgetGuardrail,
    estimated_call_cost: EstimatedCallCost
) -> tuple[bool, Optional[GuardrailAction], Optional[Dict[str, Any]]]:
    """
    Check if budget allows LLM call before making it.
    
    This demonstrates pre-call budget checking:
    - Calculate total cost if call is made
    - Check against budget limits
    - Return decision: proceed, degrade, or halt
    - Provide degradation config if needed
    
    Args:
        state: Current budget state
        cost_tracker: Cost tracker instance
        guardrail: Budget guardrail instance
        estimated_call_cost: Estimated cost for upcoming call
    
    Returns:
        Tuple of (can_proceed, action, degradation_config)
        - can_proceed: True if call can be made
        - action: GuardrailAction to take
        - degradation_config: Config for degradation if needed
    """
    # Get current budget status
    current_status = cost_tracker.check_budget_status(state)
    current_cost = current_status["budget_used"]
    budget_limit = state.get("budget_limit_usd", 0)
    
    # Calculate projected cost after call
    projected_cost = current_cost + estimated_call_cost.estimated_cost_usd
    projected_usage_percent = projected_cost / budget_limit if budget_limit > 0 else 0.0
    
    # Create temporary state with projected cost for guardrail check
    projected_state = state.copy()
    projected_state["total_cost_usd"] = projected_cost
    
    # Check guardrail with projected cost
    action = guardrail.check_guardrail(projected_state)
    
    # Determine if we can proceed
    can_proceed = action != GuardrailAction.HALT
    
    # Get degradation config if needed
    degradation_config = None
    if action == GuardrailAction.DEGRADE:
        degradation_config = guardrail.get_degradation_config(projected_state)
    
    return can_proceed, action, degradation_config


# ============================================================================
# Budget-Aware Worker Node Pattern
# ============================================================================

def budget_aware_worker_node(
    state: Dict[str, Any],
    cost_tracker: CostTracker,
    guardrail: BudgetGuardrail,
    node_name: str,
    worker_logic_func,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """
    Budget-aware Worker Node pattern.
    
    This demonstrates Worker Node with pre-call budget checking:
    - READ: Read BudgetState from GraphState
    - CHECK: Verify budget allows operation before LLM call
    - DO: Execute worker logic only if budget allows
    - WRITE: Update BudgetState after successful call
    
    Args:
        state: GraphState (must contain BudgetState)
        cost_tracker: Cost tracker instance
        guardrail: Budget guardrail instance
        node_name: Name of the worker node
        worker_logic_func: Function that contains worker logic with LLM calls
        *args: Arguments for worker logic
        **kwargs: Keyword arguments for worker logic
    
    Returns:
        Updated GraphState
    
    Raises:
        ValueError: If budget exceeded
    """
    # READ: Extract BudgetState from GraphState
    budget_state = state.get("budget", {})
    if not budget_state:
        # Initialize if missing
        budget_state = {
            "total_cost_usd": 0.0,
            "budget_limit_usd": kwargs.get("budget_limit_usd", 10.0),
            "budget_exceeded": False
        }
        state["budget"] = budget_state
    
    # CHECK: Estimate cost for upcoming operation
    # In real implementation, estimate based on:
    # - Model being used
    # - Input context size
    # - Expected output length
    estimated_cost = EstimatedCallCost(
        model_name=kwargs.get("model", "gpt-4"),
        estimated_input_tokens=kwargs.get("estimated_input_tokens", 1000),
        estimated_output_tokens=kwargs.get("estimated_output_tokens", 500),
        estimated_cost_usd=0.0  # Would be calculated from pricing
    )
    
    # Pre-call budget check
    can_proceed, action, degradation_config = check_budget_before_llm_call(
        state=budget_state,
        cost_tracker=cost_tracker,
        guardrail=guardrail,
        estimated_call_cost=estimated_cost
    )
    
    # HALT if budget exceeded
    if not can_proceed:
        error = guardrail.create_budget_exceeded_error(budget_state)
        state["errors"] = state.get("errors", []) + [error]
        state["budget"]["budget_exceeded"] = True
        return state
    
    # Apply degradation if needed
    if degradation_config:
        # Update kwargs with degradation config
        if "model" in degradation_config:
            kwargs["model"] = degradation_config["model"]
        if "max_context_tokens" in degradation_config:
            kwargs["max_context_tokens"] = degradation_config["max_context_tokens"]
    
    # DO: Execute worker logic
    try:
        result = worker_logic_func(*args, **kwargs)
        
        # Extract actual token usage from result
        # In real implementation, this comes from LLM response
        actual_input_tokens = result.get("usage", {}).get("prompt_tokens", estimated_cost.estimated_input_tokens)
        actual_output_tokens = result.get("usage", {}).get("completion_tokens", estimated_cost.estimated_output_tokens)
        model_name = kwargs.get("model", estimated_cost.model_name)
        
        # WRITE: Update BudgetState
        updated_budget = cost_tracker.update_budget_state(
            state=budget_state,
            model_name=model_name,
            node_name=node_name,
            input_tokens=actual_input_tokens,
            output_tokens=actual_output_tokens
        )
        
        # Update state with new budget
        state["budget"] = updated_budget
        
        # Check again after actual call (in case estimation was off)
        if guardrail.should_halt(updated_budget):
            error = guardrail.create_budget_exceeded_error(updated_budget)
            state["errors"] = state.get("errors", []) + [error]
            state["budget"]["budget_exceeded"] = True
        
        return state
        
    except Exception as e:
        # Handle errors - don't update budget on failure
        state["errors"] = state.get("errors", []) + [{"error": str(e), "node": node_name}]
        return state


# ============================================================================
# Example: Worker Node Using Budget Check
# ============================================================================

def example_worker_node_with_budget_check(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example Worker Node that uses budget checking.
    
    This demonstrates the pattern:
    - Read BudgetState
    - Check budget before LLM call
    - Execute only if budget allows
    - Update BudgetState after call
    """
    # In real implementation, these would be injected
    cost_tracker = None  # CostTracker instance
    guardrail = None  # BudgetGuardrail instance
    
    def worker_logic(prompt: str, model: str = "gpt-4"):
        """Worker logic that makes LLM call."""
        # In real implementation, make actual LLM call
        return {
            "content": "Worker output",
            "usage": {
                "prompt_tokens": 1000,
                "completion_tokens": 500
            }
        }
    
    # Use budget-aware wrapper
    return budget_aware_worker_node(
        state=state,
        cost_tracker=cost_tracker,
        guardrail=guardrail,
        node_name="example_worker",
        worker_logic_func=worker_logic,
        prompt=state.get("user_input", ""),
        model="gpt-4",
        estimated_input_tokens=1000,
        estimated_output_tokens=500
    )
