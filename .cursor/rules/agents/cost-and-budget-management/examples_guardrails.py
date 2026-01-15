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
