"""
Feedback Loop Examples

This file demonstrates feedback patterns to Planner, feedback generation, and feedback loop implementation.
Reference this example from RULE.mdc using @examples_feedback_loop.py syntax.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# Feedback Structures
# ============================================================================

@dataclass
class Experience:
    """Experience structure."""
    experience_id: str
    actions: List[Dict[str, Any]]
    context: Dict[str, Any]
    results: Dict[str, Any]
    success: bool
    timestamp: datetime
    feedback: Optional[str] = None


@dataclass
class Insight:
    """Insight extracted from experiences."""
    insight_id: str
    description: str
    confidence: float
    source_experiences: List[str]
    category: str  # success, failure, pattern, recommendation


@dataclass
class Pattern:
    """Pattern identified from experiences."""
    pattern_id: str
    description: str
    frequency: int
    success_rate: float
    related_experiences: List[str]


@dataclass
class Feedback:
    """Feedback structure for Planner."""
    feedback_id: str
    insights: List[Insight]
    patterns: List[Pattern]
    recommendations: List[str]
    confidence: float
    timestamp: datetime


# ============================================================================
# Feedback Loop Service
# ============================================================================

class FeedbackLoopService:
    """
    Service for generating feedback to Planner.
    
    This demonstrates:
    - Feedback generation from experiences
    - Pattern identification
    - Insight extraction
    - Recommendation generation
    """
    
    def generate_feedback(self, experiences: List[Experience]) -> Feedback:
        """
        Generate feedback from experiences.
        
        This demonstrates:
        - Analyzing stored experiences
        - Extracting insights
        - Identifying patterns
        - Generating recommendations
        
        Args:
            experiences: List of experiences to analyze
            
        Returns:
            Feedback for Planner
        """
        insights = self._extract_insights(experiences)
        patterns = self._identify_patterns(experiences)
        recommendations = self._generate_recommendations(insights, patterns)
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(insights, patterns, len(experiences))
        
        feedback = Feedback(
            feedback_id=f"feedback_{datetime.now().isoformat()}",
            insights=insights,
            patterns=patterns,
            recommendations=recommendations,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        return feedback
    
    def _extract_insights(self, experiences: List[Experience]) -> List[Insight]:
        """
        Extract insights from experiences.
        
        This demonstrates:
        - Success pattern identification
        - Failure pattern identification
        - Learning from outcomes
        
        Args:
            experiences: Experiences to analyze
            
        Returns:
            List of insights
        """
        insights = []
        
        # Analyze successful experiences
        successful = [e for e in experiences if e.success]
        if successful:
            insight = Insight(
                insight_id="insight_success",
                description=f"Found {len(successful)} successful experiences",
                confidence=0.9,
                source_experiences=[e.experience_id for e in successful],
                category="success"
            )
            insights.append(insight)
        
        # Analyze failed experiences
        failed = [e for e in experiences if not e.success]
        if failed:
            insight = Insight(
                insight_id="insight_failure",
                description=f"Found {len(failed)} failed experiences",
                confidence=0.9,
                source_experiences=[e.experience_id for e in failed],
                category="failure"
            )
            insights.append(insight)
        
        return insights
    
    def _identify_patterns(self, experiences: List[Experience]) -> List[Pattern]:
        """
        Identify patterns from experiences.
        
        This demonstrates:
        - Pattern recognition
        - Frequency analysis
        - Success rate calculation
        
        Args:
            experiences: Experiences to analyze
            
        Returns:
            List of patterns
        """
        patterns = []
        
        # Group experiences by action type
        action_groups: Dict[str, List[Experience]] = {}
        for exp in experiences:
            for action in exp.actions:
                action_type = action.get("type", "unknown")
                if action_type not in action_groups:
                    action_groups[action_type] = []
                action_groups[action_type].append(exp)
        
        # Create patterns from groups
        for action_type, group_experiences in action_groups.items():
            if len(group_experiences) >= 2:  # Pattern requires at least 2 occurrences
                successful = sum(1 for e in group_experiences if e.success)
                success_rate = successful / len(group_experiences)
                
                pattern = Pattern(
                    pattern_id=f"pattern_{action_type}",
                    description=f"Pattern for {action_type} actions",
                    frequency=len(group_experiences),
                    success_rate=success_rate,
                    related_experiences=[e.experience_id for e in group_experiences]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _generate_recommendations(self, insights: List[Insight], patterns: List[Pattern]) -> List[str]:
        """
        Generate recommendations based on insights and patterns.
        
        This demonstrates:
        - Recommendation generation
        - Actionable suggestions
        - Evidence-based recommendations
        
        Args:
            insights: Extracted insights
            patterns: Identified patterns
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Recommendations from patterns
        for pattern in patterns:
            if pattern.success_rate > 0.8:
                recommendations.append(f"Continue using {pattern.description} (high success rate)")
            elif pattern.success_rate < 0.3:
                recommendations.append(f"Avoid {pattern.description} (low success rate)")
        
        # Recommendations from insights
        for insight in insights:
            if insight.category == "failure":
                recommendations.append(f"Learn from failure: {insight.description}")
            elif insight.category == "success":
                recommendations.append(f"Replicate success: {insight.description}")
        
        return recommendations
    
    def _calculate_confidence(self, insights: List[Insight], patterns: List[Pattern], 
                             experience_count: int) -> float:
        """
        Calculate overall feedback confidence.
        
        Args:
            insights: Extracted insights
            patterns: Identified patterns
            experience_count: Number of experiences analyzed
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # More experiences = higher confidence
        experience_factor = min(experience_count / 10.0, 1.0)
        
        # More insights and patterns = higher confidence
        analysis_factor = min((len(insights) + len(patterns)) / 5.0, 1.0)
        
        # Average confidence from insights
        insight_confidence = sum(i.confidence for i in insights) / len(insights) if insights else 0.5
        
        # Combined confidence
        confidence = (experience_factor * 0.4 + analysis_factor * 0.3 + insight_confidence * 0.3)
        
        return min(confidence, 1.0)
