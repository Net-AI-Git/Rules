"""
Model Tiers Examples

This file demonstrates model tier definitions and cost-performance optimization.
Reference this example from RULE.mdc using @examples_model_tiers.py syntax.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Model Tiers
# ============================================================================

class ModelTier(Enum):
    """
    Model tier classification.
    
    This demonstrates tier structure:
    - Tier 1: Small, fast, cheap
    - Tier 2: Medium, balanced
    - Tier 3: Large, powerful, expensive
    """
    TIER1 = "tier1"  # Small/Fast/Cheap
    TIER2 = "tier2"  # Medium
    TIER3 = "tier3"  # Large/Powerful


@dataclass
class ModelSpec:
    """
    Model specification.
    
    This demonstrates model specification:
    - Model name
    - Tier classification
    - Pricing (input/output)
    - Capabilities
    - Performance characteristics
    """
    name: str
    tier: ModelTier
    provider: str
    input_price_per_1k: float  # USD per 1K input tokens
    output_price_per_1k: float  # USD per 1K output tokens
    capabilities: List[str]
    avg_latency_seconds: float
    context_window: int
    max_output_tokens: Optional[int] = None


# ============================================================================
# Model Registry
# ============================================================================

class ModelRegistry:
    """
    Registry of available models with tier classification.
    
    This demonstrates model registry pattern:
    - Model specifications
    - Tier organization
    - Capability mapping
    - Cost tracking
    """
    
    def __init__(self):
        """Initialize model registry with common models."""
        self.models: Dict[str, ModelSpec] = {}
        self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize default model specifications."""
        # Tier 1: Small/Fast/Cheap
        self.register_model(ModelSpec(
            name="claude-haiku",
            tier=ModelTier.TIER1,
            provider="anthropic",
            input_price_per_1k=0.00025,
            output_price_per_1k=0.00125,
            capabilities=["classification", "extraction", "simple_reasoning"],
            avg_latency_seconds=1.0,
            context_window=200000
        ))
        
        self.register_model(ModelSpec(
            name="gpt-3.5-turbo",
            tier=ModelTier.TIER1,
            provider="openai",
            input_price_per_1k=0.0005,
            output_price_per_1k=0.0015,
            capabilities=["classification", "extraction", "simple_reasoning"],
            avg_latency_seconds=1.5,
            context_window=16385
        ))
        
        # Tier 2: Medium
        self.register_model(ModelSpec(
            name="claude-sonnet",
            tier=ModelTier.TIER2,
            provider="anthropic",
            input_price_per_1k=0.003,
            output_price_per_1k=0.015,
            capabilities=["reasoning", "analysis", "generation", "synthesis"],
            avg_latency_seconds=2.5,
            context_window=200000
        ))
        
        self.register_model(ModelSpec(
            name="gpt-4-turbo",
            tier=ModelTier.TIER2,
            provider="openai",
            input_price_per_1k=0.01,
            output_price_per_1k=0.03,
            capabilities=["reasoning", "analysis", "generation", "code"],
            avg_latency_seconds=3.0,
            context_window=128000
        ))
        
        # Tier 3: Large/Powerful
        self.register_model(ModelSpec(
            name="claude-opus",
            tier=ModelTier.TIER3,
            provider="anthropic",
            input_price_per_1k=0.015,
            output_price_per_1k=0.075,
            capabilities=["deep_reasoning", "complex_synthesis", "creative_generation"],
            avg_latency_seconds=5.0,
            context_window=200000
        ))
        
        self.register_model(ModelSpec(
            name="gpt-4",
            tier=ModelTier.TIER3,
            provider="openai",
            input_price_per_1k=0.03,
            output_price_per_1k=0.06,
            capabilities=["deep_reasoning", "complex_synthesis", "creative_generation"],
            avg_latency_seconds=4.0,
            context_window=8192
        ))
    
    def register_model(self, spec: ModelSpec):
        """
        Register a model specification.
        
        Args:
            spec: Model specification
        """
        self.models[spec.name] = spec
    
    def get_model(self, name: str) -> Optional[ModelSpec]:
        """
        Get model specification by name.
        
        Args:
            name: Model name
        
        Returns:
            ModelSpec or None
        """
        return self.models.get(name)
    
    def get_models_by_tier(self, tier: ModelTier) -> List[ModelSpec]:
        """
        Get all models in a tier.
        
        Args:
            tier: Model tier
        
        Returns:
            List of ModelSpec
        """
        return [spec for spec in self.models.values() if spec.tier == tier]
    
    def get_models_by_capability(self, capability: str) -> List[ModelSpec]:
        """
        Get models with a specific capability.
        
        Args:
            capability: Required capability
        
        Returns:
            List of ModelSpec
        """
        return [
            spec for spec in self.models.values()
            if capability in spec.capabilities
        ]
    
    def get_tier_mapping(self) -> Dict[str, List[str]]:
        """
        Get mapping of tier names to model names.
        
        Returns:
            Dictionary mapping tier names to model name lists
        """
        mapping = {
            "tier1": [],
            "tier2": [],
            "tier3": []
        }
        
        for spec in self.models.values():
            tier_key = f"tier{spec.tier.value[-1]}"  # Extract number from enum
            mapping[tier_key].append(spec.name)
        
        return mapping


# ============================================================================
# Cost-Performance Optimizer
# ============================================================================

class CostPerformanceOptimizer:
    """
    Service for optimizing cost-performance trade-offs.
    
    This demonstrates cost optimization patterns:
    - Calculate cost for different models
    - Compare performance vs cost
    - Select optimal model
    """
    
    def __init__(self, model_registry: ModelRegistry):
        """
        Initialize optimizer.
        
        Args:
            model_registry: Model registry instance
        """
        self.registry = model_registry
    
    def estimate_cost(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Estimate cost for a model call.
        
        Args:
            model_name: Model name
            input_tokens: Input token count
            output_tokens: Output token count
        
        Returns:
            Estimated cost in USD
        """
        spec = self.registry.get_model(model_name)
        if not spec:
            return 0.0
        
        input_cost = (input_tokens / 1000) * spec.input_price_per_1k
        output_cost = (output_tokens / 1000) * spec.output_price_per_1k
        
        return input_cost + output_cost
    
    def find_optimal_model(
        self,
        required_capabilities: List[str],
        estimated_input_tokens: int,
        estimated_output_tokens: int,
        max_cost: Optional[float] = None,
        max_latency: Optional[float] = None
    ) -> Optional[str]:
        """
        Find optimal model for requirements.
        
        Args:
            required_capabilities: Required capabilities
            estimated_input_tokens: Estimated input tokens
            estimated_output_tokens: Estimated output tokens
            max_cost: Optional maximum cost constraint
            max_latency: Optional maximum latency constraint
        
        Returns:
            Optimal model name or None
        """
        # Find models with required capabilities
        candidates = []
        for capability in required_capabilities:
            capable_models = self.registry.get_models_by_capability(capability)
            candidates.extend(capable_models)
        
        # Remove duplicates
        candidates = list(set(candidates))
        
        if not candidates:
            return None
        
        # Filter by constraints
        if max_cost:
            candidates = [
                spec for spec in candidates
                if self.estimate_cost(spec.name, estimated_input_tokens, estimated_output_tokens) <= max_cost
            ]
        
        if max_latency:
            candidates = [
                spec for spec in candidates
                if spec.avg_latency_seconds <= max_latency
            ]
        
        if not candidates:
            return None
        
        # Select cheapest model that meets requirements
        # In real implementation, consider quality scores too
        optimal = min(
            candidates,
            key=lambda spec: self.estimate_cost(spec.name, estimated_input_tokens, estimated_output_tokens)
        )
        
        return optimal.name
    
    def compare_models(
        self,
        model_names: List[str],
        input_tokens: int,
        output_tokens: int
    ) -> List[Dict[str, Any]]:
        """
        Compare multiple models.
        
        Args:
            model_names: List of model names to compare
            input_tokens: Input token count
            output_tokens: Output token count
        
        Returns:
            List of comparison dictionaries
        """
        comparisons = []
        
        for model_name in model_names:
            spec = self.registry.get_model(model_name)
            if not spec:
                continue
            
            cost = self.estimate_cost(model_name, input_tokens, output_tokens)
            
            comparisons.append({
                "model": model_name,
                "tier": spec.tier.value,
                "cost": cost,
                "latency": spec.avg_latency_seconds,
                "capabilities": spec.capabilities
            })
        
        return comparisons
