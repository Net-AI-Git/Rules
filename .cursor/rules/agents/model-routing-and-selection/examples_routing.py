"""
Model Routing Examples

This file demonstrates task complexity assessment and model selection logic.
Reference this example from RULE.mdc using @examples_routing.py syntax.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Task Complexity
# ============================================================================

class TaskComplexity(Enum):
    """
    Task complexity levels.
    
    This demonstrates complexity classification:
    - Simple: Classification, extraction
    - Medium: Reasoning, analysis
    - Complex: Deep reasoning, synthesis
    """
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class TaskType(Enum):
    """
    Task types for classification.
    
    This demonstrates task categorization:
    - Classification tasks
    - Extraction tasks
    - Reasoning tasks
    - Synthesis tasks
    """
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    REASONING = "reasoning"
    SYNTHESIS = "synthesis"
    GENERATION = "generation"


@dataclass
class TaskAssessment:
    """
    Task complexity assessment result.
    
    This demonstrates task assessment:
    - Task type
    - Complexity level
    - Required capabilities
    - Estimated tokens
    """
    task_type: TaskType
    complexity: TaskComplexity
    required_capabilities: List[str]
    estimated_tokens: int
    requires_deep_reasoning: bool = False
    requires_creativity: bool = False


# ============================================================================
# Task Complexity Assessor
# ============================================================================

class TaskComplexityAssessor:
    """
    Service for assessing task complexity.
    
    This demonstrates complexity assessment patterns:
    - Analyze task description
    - Classify task type
    - Determine complexity level
    - Identify required capabilities
    """
    
    def assess_task(
        self,
        task_description: str,
        input_data: Optional[Dict[str, Any]] = None
    ) -> TaskAssessment:
        """
        Assess task complexity.
        
        Args:
            task_description: Description of the task
            input_data: Optional input data for assessment
            
        Returns:
            TaskAssessment result
        """
        # Classify task type
        task_type = self._classify_task_type(task_description)
        
        # Determine complexity
        complexity = self._determine_complexity(task_description, task_type, input_data)
        
        # Identify required capabilities
        capabilities = self._identify_capabilities(task_type, complexity)
        
        # Estimate tokens
        estimated_tokens = self._estimate_tokens(task_description, input_data)
        
        return TaskAssessment(
            task_type=task_type,
            complexity=complexity,
            required_capabilities=capabilities,
            estimated_tokens=estimated_tokens,
            requires_deep_reasoning=self._requires_deep_reasoning(task_description),
            requires_creativity=self._requires_creativity(task_description)
        )
    
    def _classify_task_type(self, description: str) -> TaskType:
        """
        Classify task type from description.
        
        Args:
            description: Task description
            
        Returns:
            TaskType
        """
        desc_lower = description.lower()
        
        # Classification keywords
        if any(kw in desc_lower for kw in ["classify", "categorize", "sentiment", "intent"]):
            return TaskType.CLASSIFICATION
        
        # Extraction keywords
        if any(kw in desc_lower for kw in ["extract", "find", "identify", "ner", "entity"]):
            return TaskType.EXTRACTION
        
        # Reasoning keywords
        if any(kw in desc_lower for kw in ["reason", "analyze", "solve", "determine", "decide"]):
            return TaskType.REASONING
        
        # Synthesis keywords
        if any(kw in desc_lower for kw in ["synthesize", "combine", "merge", "summarize"]):
            return TaskType.SYNTHESIS
        
        # Generation keywords
        if any(kw in desc_lower for kw in ["generate", "create", "write", "compose"]):
            return TaskType.GENERATION
        
        # Default to reasoning
        return TaskType.REASONING
    
    def _determine_complexity(
        self,
        description: str,
        task_type: TaskType,
        input_data: Optional[Dict[str, Any]]
    ) -> TaskComplexity:
        """
        Determine task complexity.
        
        Args:
            description: Task description
            task_type: Task type
            input_data: Optional input data
        
        Returns:
            TaskComplexity
        """
        # Simple tasks
        if task_type == TaskType.CLASSIFICATION:
            # Binary or multi-class classification is simple
            if "binary" in description.lower() or "yes/no" in description.lower():
                return TaskComplexity.SIMPLE
            return TaskComplexity.SIMPLE
        
        if task_type == TaskType.EXTRACTION:
            # Simple extraction (dates, numbers) is simple
            if any(kw in description.lower() for kw in ["date", "number", "keyword"]):
                return TaskComplexity.SIMPLE
            # NER is usually simple to medium
            return TaskComplexity.MEDIUM
        
        # Medium tasks
        if task_type == TaskType.REASONING:
            # Multi-step reasoning is medium
            if "multi-step" in description.lower() or "step by step" in description.lower():
                return TaskComplexity.MEDIUM
            # Deep reasoning is complex
            if "deep" in description.lower() or "complex" in description.lower():
                return TaskComplexity.COMPLEX
            return TaskComplexity.MEDIUM
        
        # Complex tasks
        if task_type == TaskType.SYNTHESIS:
            # Multi-source synthesis is complex
            if "multiple" in description.lower() or "several" in description.lower():
                return TaskComplexity.COMPLEX
            return TaskComplexity.MEDIUM
        
        if task_type == TaskType.GENERATION:
            # Creative generation is complex
            if "creative" in description.lower() or "original" in description.lower():
                return TaskComplexity.COMPLEX
            return TaskComplexity.MEDIUM
        
        return TaskComplexity.MEDIUM
    
    def _identify_capabilities(
        self,
        task_type: TaskType,
        complexity: TaskComplexity
    ) -> List[str]:
        """
        Identify required model capabilities.
        
        Args:
            task_type: Task type
            complexity: Complexity level
        
        Returns:
            List of required capabilities
        """
        capabilities = []
        
        if task_type == TaskType.CLASSIFICATION:
            capabilities.append("classification")
        elif task_type == TaskType.EXTRACTION:
            capabilities.append("extraction")
            if complexity == TaskComplexity.COMPLEX:
                capabilities.append("context_understanding")
        elif task_type == TaskType.REASONING:
            capabilities.append("reasoning")
            if complexity == TaskComplexity.COMPLEX:
                capabilities.append("deep_reasoning")
        elif task_type == TaskType.SYNTHESIS:
            capabilities.append("synthesis")
            if complexity == TaskComplexity.COMPLEX:
                capabilities.append("multi_source")
        elif task_type == TaskType.GENERATION:
            capabilities.append("generation")
            if complexity == TaskComplexity.COMPLEX:
                capabilities.append("creativity")
        
        return capabilities
    
    def _estimate_tokens(
        self,
        description: str,
        input_data: Optional[Dict[str, Any]]
    ) -> int:
        """
        Estimate token count for task.
        
        Args:
            description: Task description
            input_data: Optional input data
        
        Returns:
            Estimated token count
        """
        # Base tokens from description
        base_tokens = len(description.split()) * 1.3  # Rough estimate
        
        # Add input data tokens
        if input_data:
            input_str = str(input_data)
            base_tokens += len(input_str.split()) * 1.3
        
        return int(base_tokens)
    
    def _requires_deep_reasoning(self, description: str) -> bool:
        """Check if task requires deep reasoning."""
        keywords = ["deep", "complex", "sophisticated", "advanced", "multi-step"]
        return any(kw in description.lower() for kw in keywords)
    
    def _requires_creativity(self, description: str) -> bool:
        """Check if task requires creativity."""
        keywords = ["creative", "original", "novel", "innovative", "artistic"]
        return any(kw in description.lower() for kw in keywords)


# ============================================================================
# Model Router
# ============================================================================

class ModelRouter:
    """
    Service for routing tasks to appropriate models.
    
    This demonstrates model routing patterns:
    - Assess task complexity
    - Select model tier
    - Consider cost constraints
    - Handle fallbacks
    """
    
    def __init__(self, model_tiers: Dict[str, List[str]]):
        """
        Initialize model router.
        
        Args:
            model_tiers: Dictionary mapping tier names to model lists
        """
        self.model_tiers = model_tiers
        self.assessor = TaskComplexityAssessor()
    
    def route_task(
        self,
        task_description: str,
        input_data: Optional[Dict[str, Any]] = None,
        budget_constraint: Optional[float] = None,
        latency_requirement: Optional[float] = None
    ) -> str:
        """
        Route task to appropriate model.
        
        Args:
            task_description: Task description
            input_data: Optional input data
            budget_constraint: Optional budget constraint
            latency_requirement: Optional latency requirement (seconds)
        
        Returns:
            Model name to use
        """
        # Assess task
        assessment = self.assessor.assess_task(task_description, input_data)
        
        # Select model tier based on complexity
        if assessment.complexity == TaskComplexity.SIMPLE:
            tier = "tier1"  # Small/fast/cheap
        elif assessment.complexity == TaskComplexity.MEDIUM:
            tier = "tier2"  # Medium
        else:
            tier = "tier3"  # Large/powerful
        
        # Get available models in tier
        available_models = self.model_tiers.get(tier, [])
        
        if not available_models:
            # Fallback to next tier
            if tier == "tier3":
                tier = "tier2"
            elif tier == "tier2":
                tier = "tier1"
            available_models = self.model_tiers.get(tier, [])
        
        # Select specific model (first available)
        # In real implementation, consider:
        # - Model availability
        # - Cost constraints
        # - Latency requirements
        selected_model = available_models[0] if available_models else "gpt-3.5-turbo"
        
        # Apply constraints
        if budget_constraint:
            selected_model = self._apply_budget_constraint(
                selected_model, tier, budget_constraint
            )
        
        if latency_requirement:
            selected_model = self._apply_latency_constraint(
                selected_model, tier, latency_requirement
            )
        
        return selected_model
    
    def _apply_budget_constraint(
        self,
        current_model: str,
        tier: str,
        budget: float
    ) -> str:
        """
        Apply budget constraint to model selection.
        
        Args:
            current_model: Currently selected model
            tier: Model tier
            budget: Budget constraint
        
        Returns:
            Model name (possibly downgraded)
        """
        # In real implementation:
        # - Check estimated cost for current model
        # - If exceeds budget, downgrade to cheaper tier
        # - Return appropriate model
        
        # Simple implementation: if tier3 and low budget, downgrade
        if tier == "tier3" and budget < 1.0:
            return self.model_tiers.get("tier2", ["gpt-4-turbo"])[0]
        
        return current_model
    
    def _apply_latency_constraint(
        self,
        current_model: str,
        tier: str,
        max_latency: float
    ) -> str:
        """
        Apply latency constraint to model selection.
        
        Args:
            current_model: Currently selected model
            tier: Model tier
            max_latency: Maximum allowed latency (seconds)
        
        Returns:
            Model name (possibly faster)
        """
        # In real implementation:
        # - Check estimated latency for current model
        # - If exceeds limit, use faster model
        # - Return appropriate model
        
        # Simple implementation: if tier3 and strict latency, downgrade
        if tier == "tier3" and max_latency < 5.0:
            return self.model_tiers.get("tier2", ["gpt-4-turbo"])[0]
        
        return current_model


# ============================================================================
# SECTION-Based Routing
# ============================================================================

def route_section_to_model(
    section: Dict[str, Any],
    model_router: ModelRouter,
    budget_state: Optional[Dict[str, Any]] = None
) -> str:
    """
    Route a SECTION to appropriate model.
    
    This demonstrates SECTION-based routing:
    - Assess SECTION complexity
    - Route to appropriate model
    - Consider budget constraints
    
    Args:
        section: SECTION dictionary
        model_router: Model router instance
        budget_state: Optional budget state
        
    Returns:
        Model name to use
    """
    # Extract task description from SECTION
    task_description = section.get("scope", "") + " " + section.get("task_description", "")
    
    # Get budget constraint if available
    budget_constraint = None
    if budget_state:
        remaining_budget = budget_state.get("budget_remaining", None)
        if remaining_budget:
            budget_constraint = remaining_budget
    
    # Route task
    model = model_router.route_task(
        task_description=task_description,
        input_data=section.get("inputs"),
        budget_constraint=budget_constraint
    )
    
    return model
