"""
Risk Assessment Examples

This file demonstrates risk/cost/benefit evaluation patterns, trade-off analysis, and risk mitigation strategies.
Reference this example from RULE.mdc using @examples_risk_assessment.py syntax.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Risk Assessment Types
# ============================================================================

class RiskLevel(str, Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskAssessment:
    """Risk assessment structure."""
    risk_id: str
    description: str
    risk_level: RiskLevel
    probability: float  # 0.0 to 1.0
    impact: str  # low, medium, high
    mitigation_strategy: Optional[str] = None


@dataclass
class CostEstimate:
    """Cost estimate structure."""
    tokens: int
    api_calls: int
    time_seconds: int
    resource_usage: Dict[str, Any] = None


@dataclass
class BenefitEvaluation:
    """Benefit evaluation structure."""
    benefit_id: str
    value_score: float  # 0.0 to 1.0
    impact: str  # low, medium, high
    priority: int  # 1-10, higher is more important
    success_probability: float  # 0.0 to 1.0


@dataclass
class ActionEvaluation:
    """Complete action evaluation with risk, cost, and benefit."""
    action_id: str
    risk_assessment: RiskAssessment
    cost_estimate: CostEstimate
    benefit_evaluation: BenefitEvaluation
    recommendation: bool
    trade_off_score: float  # Combined score for decision making


# ============================================================================
# Risk Assessment Service
# ============================================================================

class RiskAssessmentService:
    """
    Service for risk, cost, and benefit evaluation.
    
    This demonstrates:
    - Risk assessment patterns
    - Cost analysis
    - Benefit evaluation
    - Trade-off analysis
    """
    
    def assess_risk(self, action: Dict[str, Any], context: Dict[str, Any]) -> RiskAssessment:
        """
        Assess risk for an action.
        
        This demonstrates:
        - Identifying potential failures
        - Assessing side effects
        - Evaluating security concerns
        - Determining risk level
        
        Args:
            action: Action to assess
            context: Current context and environment
            
        Returns:
            Risk assessment for the action
        """
        # Implementation would analyze action and context
        # This is a simplified example
        risk = RiskAssessment(
            risk_id=f"risk_{action.get('id', 'unknown')}",
            description="Potential failure in action execution",
            risk_level=RiskLevel.MEDIUM,
            probability=0.3,
            impact="medium",
            mitigation_strategy="Retry with exponential backoff"
        )
        return risk
    
    def estimate_cost(self, action: Dict[str, Any], context: Dict[str, Any]) -> CostEstimate:
        """
        Estimate cost for an action.
        
        This demonstrates:
        - Estimating token usage
        - Counting API calls
        - Calculating time requirements
        - Assessing resource usage
        
        Args:
            action: Action to estimate
            context: Current context
            
        Returns:
            Cost estimate for the action
        """
        cost = CostEstimate(
            tokens=1000,
            api_calls=2,
            time_seconds=30,
            resource_usage={"memory_mb": 100, "cpu_percent": 20}
        )
        return cost
    
    def evaluate_benefit(self, action: Dict[str, Any], goals: List[str]) -> BenefitEvaluation:
        """
        Evaluate benefit of an action.
        
        This demonstrates:
        - Assessing value and impact
        - Calculating success probability
        - Determining priority
        - Measuring expected value
        
        Args:
            action: Action to evaluate
            goals: Goals this action supports
            
        Returns:
            Benefit evaluation for the action
        """
        benefit = BenefitEvaluation(
            benefit_id=f"benefit_{action.get('id', 'unknown')}",
            value_score=0.8,
            impact="high",
            priority=8,
            success_probability=0.85
        )
        return benefit
    
    def evaluate_action(self, action: Dict[str, Any], context: Dict[str, Any], 
                       goals: List[str]) -> ActionEvaluation:
        """
        Complete action evaluation with risk, cost, and benefit.
        
        This demonstrates:
        - Comprehensive action evaluation
        - Trade-off analysis
        - Recommendation generation
        
        Args:
            action: Action to evaluate
            context: Current context
            goals: Goals this action supports
            
        Returns:
            Complete action evaluation
        """
        risk = self.assess_risk(action, context)
        cost = self.estimate_cost(action, context)
        benefit = self.evaluate_benefit(action, goals)
        
        # Calculate trade-off score
        # Higher benefit, lower risk, lower cost = higher score
        trade_off_score = (
            benefit.value_score * 0.5 +
            (1.0 - risk.probability) * 0.3 +
            (1.0 - min(cost.tokens / 10000, 1.0)) * 0.2
        )
        
        recommendation = trade_off_score > 0.6
        
        return ActionEvaluation(
            action_id=action.get("id", "unknown"),
            risk_assessment=risk,
            cost_estimate=cost,
            benefit_evaluation=benefit,
            recommendation=recommendation,
            trade_off_score=trade_off_score
        )
    
    def create_mitigation_strategy(self, risk: RiskAssessment) -> str:
        """
        Create risk mitigation strategy.
        
        This demonstrates:
        - Risk mitigation planning
        - Strategy development
        - Contingency planning
        
        Args:
            risk: Risk to mitigate
            
        Returns:
            Mitigation strategy
        """
        strategies = {
            RiskLevel.LOW: "Monitor and log",
            RiskLevel.MEDIUM: "Retry with exponential backoff",
            RiskLevel.HIGH: "Implement circuit breaker and fallback",
            RiskLevel.CRITICAL: "Require human approval before execution"
        }
        return strategies.get(risk.risk_level, "Standard error handling")
