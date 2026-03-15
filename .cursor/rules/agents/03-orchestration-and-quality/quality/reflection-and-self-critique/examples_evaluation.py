"""
Evaluation Examples

This file demonstrates internal eval metrics and quality scoring patterns.
Reference this example from RULE.mdc using @examples_evaluation.py syntax.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Evaluation Metrics
# ============================================================================

@dataclass
class EvaluationMetrics:
    """
    Evaluation metrics structure.
    
    This demonstrates evaluation metrics:
    - Faithfulness: Reliance on provided context
    - Answer Relevance: Relevance to user request
    - Completeness: Presence of required elements
    - Coherence: Logical structure and consistency
    """
    faithfulness: float  # 0.0-1.0
    answer_relevance: float  # 0.0-1.0
    completeness: float  # 0.0-1.0
    coherence: float  # 0.0-1.0
    overall_score: float  # 0.0-1.0
    
    def __post_init__(self):
        """Calculate overall score."""
        # Weighted average
        weights = {
            "faithfulness": 0.3,
            "answer_relevance": 0.3,
            "completeness": 0.2,
            "coherence": 0.2
        }
        
        self.overall_score = (
            self.faithfulness * weights["faithfulness"] +
            self.answer_relevance * weights["answer_relevance"] +
            self.completeness * weights["completeness"] +
            self.coherence * weights["coherence"]
        )


class MetricEvaluator:
    """
    Service for evaluating outputs on different metrics.
    
    This demonstrates metric evaluation patterns:
    - Faithfulness evaluation
    - Relevance evaluation
    - Completeness evaluation
    - Coherence evaluation
    """
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize metric evaluator.
        
        Args:
            llm_client: Optional LLM client for evaluation
        """
        self.llm_client = llm_client
    
    def evaluate_faithfulness(
        self,
        output: str,
        context: List[str]
    ) -> float:
        """
        Evaluate faithfulness (no hallucinations).
        
        Args:
            output: Output to evaluate
            context: Provided context
        
        Returns:
            Faithfulness score (0.0-1.0)
        """
        # In real implementation:
        # 1. Extract claims from output
        # 2. Verify each claim against context
        # 3. Calculate percentage of verifiable claims
        
        # Simple implementation: check if output references context
        context_mentions = sum(1 for ctx in context if ctx.lower() in output.lower())
        if len(context) > 0:
            return min(1.0, context_mentions / len(context))
        return 0.5  # Default if no context
    
    def evaluate_answer_relevance(
        self,
        output: str,
        user_request: str
    ) -> float:
        """
        Evaluate answer relevance to user request.
        
        Args:
            output: Output to evaluate
            user_request: Original user request
        
        Returns:
            Relevance score (0.0-1.0)
        """
        # In real implementation:
        # 1. Extract key topics from user request
        # 2. Check if output addresses these topics
        # 3. Calculate relevance score
        
        # Simple implementation: keyword overlap
        request_keywords = set(user_request.lower().split())
        output_keywords = set(output.lower().split())
        
        if not request_keywords:
            return 0.5
        
        overlap = len(request_keywords & output_keywords) / len(request_keywords)
        return min(1.0, overlap * 1.5)  # Scale to 0.0-1.0
    
    def evaluate_completeness(
        self,
        output: str,
        required_elements: List[str]
    ) -> float:
        """
        Evaluate completeness (all required elements present).
        
        Args:
            output: Output to evaluate
            required_elements: List of required elements
        
        Returns:
            Completeness score (0.0-1.0)
        """
        if not required_elements:
            return 1.0
        
        # Check if each required element is present
        present_count = sum(
            1 for element in required_elements
            if element.lower() in output.lower()
        )
        
        return present_count / len(required_elements)
    
    def evaluate_coherence(
        self,
        output: str
    ) -> float:
        """
        Evaluate coherence (logical structure and consistency).
        
        Args:
            output: Output to evaluate
        
        Returns:
            Coherence score (0.0-1.0)
        """
        # In real implementation:
        # 1. Check logical flow
        # 2. Check for contradictions
        # 3. Check structure consistency
        # 4. Calculate coherence score
        
        # Simple implementation: check for basic structure
        has_structure = any(marker in output for marker in [". ", "\n", "•", "-"])
        has_length = len(output.split()) > 10
        
        # Check for contradictions (simple: check for "but" and "however" patterns)
        contradiction_indicators = ["but", "however", "although", "despite"]
        has_contradictions = sum(1 for ind in contradiction_indicators if ind in output.lower()) > 2
        
        score = 0.5
        if has_structure:
            score += 0.2
        if has_length:
            score += 0.2
        if not has_contradictions:
            score += 0.1
        
        return min(1.0, score)
    
    def evaluate_all(
        self,
        output: str,
        context: List[str],
        user_request: str,
        required_elements: List[str]
    ) -> EvaluationMetrics:
        """
        Evaluate output on all metrics.
        
        Args:
            output: Output to evaluate
            context: Provided context
            user_request: Original user request
            required_elements: Required elements
        
        Returns:
            EvaluationMetrics
        """
        faithfulness = self.evaluate_faithfulness(output, context)
        answer_relevance = self.evaluate_answer_relevance(output, user_request)
        completeness = self.evaluate_completeness(output, required_elements)
        coherence = self.evaluate_coherence(output)
        
        metrics = EvaluationMetrics(
            faithfulness=faithfulness,
            answer_relevance=answer_relevance,
            completeness=completeness,
            coherence=coherence,
            overall_score=0.0  # Will be calculated in __post_init__
        )
        
        return metrics


# ============================================================================
# Quality Scorer
# ============================================================================

class QualityScorer:
    """
    Service for scoring output quality.
    
    This demonstrates quality scoring patterns:
    - Multi-dimensional scoring
    - Weighted scoring
    - Threshold-based decisions
    - Comparative scoring
    """
    
    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        threshold: float = 0.8
    ):
        """
        Initialize quality scorer.
        
        Args:
            weights: Optional custom weights for dimensions
            threshold: Quality threshold for approval
        """
        self.weights = weights or {
            "faithfulness": 0.3,
            "answer_relevance": 0.3,
            "completeness": 0.2,
            "coherence": 0.2
        }
        self.threshold = threshold
    
    def score(
        self,
        metrics: EvaluationMetrics
    ) -> Dict[str, Any]:
        """
        Score output quality.
        
        Args:
            metrics: Evaluation metrics
        
        Returns:
            Scoring result dictionary
        """
        # Calculate weighted score
        weighted_score = (
            metrics.faithfulness * self.weights["faithfulness"] +
            metrics.answer_relevance * self.weights["answer_relevance"] +
            metrics.completeness * self.weights["completeness"] +
            metrics.coherence * self.weights["coherence"]
        )
        
        # Determine status
        if weighted_score >= self.threshold:
            status = "approved"
        elif weighted_score >= self.threshold * 0.6:  # 60% of threshold
            status = "needs_revision"
        else:
            status = "rejected"
        
        return {
            "weighted_score": weighted_score,
            "overall_score": metrics.overall_score,
            "dimension_scores": {
                "faithfulness": metrics.faithfulness,
                "answer_relevance": metrics.answer_relevance,
                "completeness": metrics.completeness,
                "coherence": metrics.coherence
            },
            "status": status,
            "meets_threshold": weighted_score >= self.threshold
        }
    
    def compare_versions(
        self,
        version1_metrics: EvaluationMetrics,
        version2_metrics: EvaluationMetrics
    ) -> Dict[str, Any]:
        """
        Compare two output versions.
        
        Args:
            version1_metrics: Metrics for version 1
            version2_metrics: Metrics for version 2
        
        Returns:
            Comparison result
        """
        score1 = self.score(version1_metrics)
        score2 = self.score(version2_metrics)
        
        improvement = score2["weighted_score"] - score1["weighted_score"]
        
        return {
            "version1_score": score1["weighted_score"],
            "version2_score": score2["weighted_score"],
            "improvement": improvement,
            "is_improved": improvement > 0,
            "better_version": "version2" if improvement > 0 else "version1"
        }


# ============================================================================
# Evaluation Service
# ============================================================================

class EvaluationService:
    """
    Service for comprehensive output evaluation.
    
    This demonstrates evaluation service pattern:
    - Evaluate on all metrics
    - Score quality
    - Compare versions
    - Generate reports
    """
    
    def __init__(
        self,
        metric_evaluator: MetricEvaluator,
        quality_scorer: QualityScorer
    ):
        """
        Initialize evaluation service.
        
        Args:
            metric_evaluator: Metric evaluator instance
            quality_scorer: Quality scorer instance
        """
        self.metric_evaluator = metric_evaluator
        self.quality_scorer = quality_scorer
    
    def evaluate_output(
        self,
        output: str,
        context: List[str],
        user_request: str,
        required_elements: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate output comprehensively.
        
        Args:
            output: Output to evaluate
            context: Provided context
            user_request: Original user request
            required_elements: Required elements
        
        Returns:
            Evaluation result dictionary
        """
        # Evaluate metrics
        metrics = self.metric_evaluator.evaluate_all(
            output, context, user_request, required_elements
        )
        
        # Score quality
        score_result = self.quality_scorer.score(metrics)
        
        return {
            "metrics": metrics,
            "scoring": score_result,
            "recommendation": score_result["status"]
        }
