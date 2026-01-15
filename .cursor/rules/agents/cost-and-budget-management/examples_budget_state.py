"""
Budget State and Cost Tracking Examples

This file demonstrates BudgetState TypedDict definition and cost tracking implementation.
Reference this example from RULE.mdc using @examples_budget_state.py syntax.
"""

from typing import TypedDict, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field


# ============================================================================
# BudgetState TypedDict
# ============================================================================

class BudgetState(TypedDict, total=False):
    """
    Budget state structure for tracking token costs in real-time.
    
    This demonstrates the BudgetState pattern:
    - Cumulative token and cost tracking
    - Per-model cost breakdown
    - Per-node cost attribution
    - Session metadata
    """
    # Cumulative tracking
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    total_cost_usd: float
    
    # Per-model tracking
    model_costs: Dict[str, float]  # model_name -> cost
    model_tokens: Dict[str, int]    # model_name -> token_count
    
    # Per-node tracking
    node_costs: Dict[str, float]    # node_name -> cost
    node_tokens: Dict[str, int]     # node_name -> token_count
    
    # Session metadata
    session_start_time: datetime
    last_update_time: datetime
    budget_limit_usd: float
    budget_warning_threshold: float  # e.g., 0.8 for 80%
    budget_exceeded: bool


# ============================================================================
# Model Pricing Configuration
# ============================================================================

@dataclass
class ModelPricing:
    """
    Model pricing configuration for cost calculation.
    
    This demonstrates model-specific pricing:
    - Input and output token pricing (per 1K tokens)
    - Different pricing for different models
    - Support for multiple providers
    """
    model_name: str
    input_price_per_1k: float  # USD per 1K input tokens
    output_price_per_1k: float  # USD per 1K output tokens
    provider: str  # e.g., "openai", "anthropic"


class PricingRegistry:
    """
    Registry for model pricing configurations.
    
    This demonstrates centralized pricing management:
    - Model pricing lookup
    - Default pricing for unknown models
    - Pricing updates
    """
    
    def __init__(self):
        """Initialize with default pricing for common models."""
        self._pricing: Dict[str, ModelPricing] = {
            "gpt-4": ModelPricing(
                model_name="gpt-4",
                input_price_per_1k=0.03,
                output_price_per_1k=0.06,
                provider="openai"
            ),
            "gpt-4-turbo": ModelPricing(
                model_name="gpt-4-turbo",
                input_price_per_1k=0.01,
                output_price_per_1k=0.03,
                provider="openai"
            ),
            "gpt-3.5-turbo": ModelPricing(
                model_name="gpt-3.5-turbo",
                input_price_per_1k=0.0005,
                output_price_per_1k=0.0015,
                provider="openai"
            ),
            "claude-opus": ModelPricing(
                model_name="claude-opus",
                input_price_per_1k=0.015,
                output_price_per_1k=0.075,
                provider="anthropic"
            ),
            "claude-sonnet": ModelPricing(
                model_name="claude-sonnet",
                input_price_per_1k=0.003,
                output_price_per_1k=0.015,
                provider="anthropic"
            ),
            "claude-haiku": ModelPricing(
                model_name="claude-haiku",
                input_price_per_1k=0.00025,
                output_price_per_1k=0.00125,
                provider="anthropic"
            ),
        }
        self._default_pricing = ModelPricing(
            model_name="unknown",
            input_price_per_1k=0.01,  # Conservative default
            output_price_per_1k=0.03,
            provider="unknown"
        )
    
    def get_pricing(self, model_name: str) -> ModelPricing:
        """
        Get pricing for a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            ModelPricing configuration for the model
        """
        return self._pricing.get(model_name, self._default_pricing)
    
    def register_pricing(self, pricing: ModelPricing) -> None:
        """
        Register or update pricing for a model.
        
        Args:
            pricing: ModelPricing configuration
        """
        self._pricing[pricing.model_name] = pricing


# ============================================================================
# Cost Tracker
# ============================================================================

class CostTracker:
    """
    Cost tracking service for agent workflows.
    
    This demonstrates cost tracking implementation:
    - Real-time cost calculation
    - BudgetState updates
    - Per-model and per-node tracking
    - Budget limit checking
    """
    
    def __init__(
        self,
        pricing_registry: PricingRegistry,
        budget_limit_usd: float = 10.0,
        warning_threshold: float = 0.8
    ):
        """
        Initialize cost tracker.
        
        Args:
            pricing_registry: Registry for model pricing
            budget_limit_usd: Budget limit in USD
            warning_threshold: Warning threshold (0.0-1.0)
        """
        self.pricing_registry = pricing_registry
        self.budget_limit_usd = budget_limit_usd
        self.warning_threshold = warning_threshold
    
    def calculate_cost(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Calculate cost for an LLM call.
        
        Args:
            model_name: Name of the model used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in USD
        """
        pricing = self.pricing_registry.get_pricing(model_name)
        
        input_cost = (input_tokens / 1000) * pricing.input_price_per_1k
        output_cost = (output_tokens / 1000) * pricing.output_price_per_1k
        
        return input_cost + output_cost
    
    def update_budget_state(
        self,
        state: BudgetState,
        model_name: str,
        node_name: str,
        input_tokens: int,
        output_tokens: int
    ) -> BudgetState:
        """
        Update budget state with new LLM call costs.
        
        Args:
            state: Current budget state
            model_name: Name of the model used
            node_name: Name of the node making the call
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Updated budget state
        """
        # Calculate cost
        cost = self.calculate_cost(model_name, input_tokens, output_tokens)
        total_tokens = input_tokens + output_tokens
        
        # Initialize state if needed
        if "total_input_tokens" not in state:
            state["total_input_tokens"] = 0
            state["total_output_tokens"] = 0
            state["total_tokens"] = 0
            state["total_cost_usd"] = 0.0
            state["model_costs"] = {}
            state["model_tokens"] = {}
            state["node_costs"] = {}
            state["node_tokens"] = {}
            state["budget_limit_usd"] = self.budget_limit_usd
            state["budget_warning_threshold"] = self.warning_threshold
            state["budget_exceeded"] = False
        
        # Update cumulative totals
        state["total_input_tokens"] += input_tokens
        state["total_output_tokens"] += output_tokens
        state["total_tokens"] += total_tokens
        state["total_cost_usd"] += cost
        
        # Update per-model tracking
        state["model_costs"][model_name] = state["model_costs"].get(model_name, 0.0) + cost
        state["model_tokens"][model_name] = state["model_tokens"].get(model_name, 0) + total_tokens
        
        # Update per-node tracking
        state["node_costs"][node_name] = state["node_costs"].get(node_name, 0.0) + cost
        state["node_tokens"][node_name] = state["node_tokens"].get(node_name, 0) + total_tokens
        
        # Update timestamps
        state["last_update_time"] = datetime.now()
        if "session_start_time" not in state:
            state["session_start_time"] = datetime.now()
        
        # Check budget limits
        budget_usage = state["total_cost_usd"] / state["budget_limit_usd"]
        if budget_usage >= 1.0:
            state["budget_exceeded"] = True
        
        return state
    
    def check_budget_status(self, state: BudgetState) -> Dict[str, any]:
        """
        Check current budget status.
        
        Args:
            state: Current budget state
            
        Returns:
            Dictionary with budget status information
        """
        if "total_cost_usd" not in state:
            return {
                "budget_used": 0.0,
                "budget_remaining": state.get("budget_limit_usd", 0.0),
                "budget_usage_percent": 0.0,
                "is_warning": False,
                "is_exceeded": False
            }
        
        budget_used = state["total_cost_usd"]
        budget_limit = state.get("budget_limit_usd", self.budget_limit_usd)
        budget_remaining = max(0.0, budget_limit - budget_used)
        budget_usage_percent = budget_used / budget_limit if budget_limit > 0 else 0.0
        
        warning_threshold = state.get("budget_warning_threshold", self.warning_threshold)
        is_warning = budget_usage_percent >= warning_threshold
        is_exceeded = state.get("budget_exceeded", False) or budget_usage_percent >= 1.0
        
        return {
            "budget_used": budget_used,
            "budget_remaining": budget_remaining,
            "budget_usage_percent": budget_usage_percent,
            "is_warning": is_warning,
            "is_exceeded": is_exceeded
        }
