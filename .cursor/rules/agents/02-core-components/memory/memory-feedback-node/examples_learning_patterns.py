"""
Learning Patterns Examples

This file demonstrates pattern learning and adaptation patterns, pattern recognition, and adaptive behavior.
Reference this example from RULE.mdc using @examples_learning_patterns.py syntax.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict


# ============================================================================
# Learning Pattern Structures
# ============================================================================

@dataclass
class Experience:
    """Experience structure for learning."""
    experience_id: str
    actions: List[Dict[str, Any]]
    context: Dict[str, Any]
    results: Dict[str, Any]
    success: bool
    timestamp: datetime


@dataclass
class LearnedPattern:
    """Pattern learned from experiences."""
    pattern_id: str
    pattern_type: str  # success, failure, sequence, context
    description: str
    frequency: int
    success_rate: float
    confidence: float
    last_seen: datetime
    related_experiences: List[str]


@dataclass
class Adaptation:
    """Adaptation based on learned patterns."""
    adaptation_id: str
    pattern_id: str
    adaptation_type: str  # strategy_change, parameter_adjustment, rule_update
    description: str
    expected_improvement: float
    confidence: float


# ============================================================================
# Learning Service
# ============================================================================

class LearningService:
    """
    Service for learning from patterns and experiences.
    
    This demonstrates:
    - Pattern recognition
    - Learning from successes and failures
    - Adaptive behavior
    - Pattern-based recommendations
    """
    
    def __init__(self):
        """Initialize learning service."""
        self.learned_patterns: Dict[str, LearnedPattern] = {}
        self.experience_history: List[Experience] = []
    
    def learn_from_experience(self, experience: Experience) -> List[LearnedPattern]:
        """
        Learn patterns from a new experience.
        
        This demonstrates:
        - Experience analysis
        - Pattern extraction
        - Pattern updating
        - Learning adaptation
        
        Args:
            experience: New experience to learn from
            
        Returns:
            List of updated or new patterns
        """
        self.experience_history.append(experience)
        
        # Extract patterns from experience
        patterns = self._extract_patterns(experience)
        
        # Update learned patterns
        updated_patterns = []
        for pattern in patterns:
            updated_pattern = self._update_pattern(pattern)
            self.learned_patterns[updated_pattern.pattern_id] = updated_pattern
            updated_patterns.append(updated_pattern)
        
        return updated_patterns
    
    def _extract_patterns(self, experience: Experience) -> List[LearnedPattern]:
        """
        Extract patterns from experience.
        
        This demonstrates:
        - Pattern identification
        - Pattern categorization
        - Pattern description generation
        
        Args:
            experience: Experience to analyze
            
        Returns:
            List of extracted patterns
        """
        patterns = []
        
        # Success/failure pattern
        pattern_type = "success" if experience.success else "failure"
        pattern = LearnedPattern(
            pattern_id=f"pattern_{pattern_type}_{experience.experience_id}",
            pattern_type=pattern_type,
            description=f"{pattern_type.capitalize()} pattern from {len(experience.actions)} actions",
            frequency=1,
            success_rate=1.0 if experience.success else 0.0,
            confidence=0.5,  # Low confidence for single occurrence
            last_seen=experience.timestamp,
            related_experiences=[experience.experience_id]
        )
        patterns.append(pattern)
        
        # Action sequence pattern
        if len(experience.actions) > 1:
            sequence_pattern = LearnedPattern(
                pattern_id=f"pattern_sequence_{experience.experience_id}",
                pattern_type="sequence",
                description=f"Action sequence: {[a.get('type') for a in experience.actions]}",
                frequency=1,
                success_rate=1.0 if experience.success else 0.0,
                confidence=0.5,
                last_seen=experience.timestamp,
                related_experiences=[experience.experience_id]
            )
            patterns.append(sequence_pattern)
        
        return patterns
    
    def _update_pattern(self, new_pattern: LearnedPattern) -> LearnedPattern:
        """
        Update existing pattern or create new one.
        
        This demonstrates:
        - Pattern merging
        - Frequency tracking
        - Success rate calculation
        - Confidence updating
        
        Args:
            new_pattern: New pattern to merge or create
            
        Returns:
            Updated pattern
        """
        existing = self.learned_patterns.get(new_pattern.pattern_id)
        
        if existing:
            # Merge with existing pattern
            merged_frequency = existing.frequency + new_pattern.frequency
            merged_experiences = existing.related_experiences + new_pattern.related_experiences
            
            # Recalculate success rate
            successful = sum(1 for exp_id in merged_experiences 
                           if any(e.experience_id == exp_id and e.success 
                                 for e in self.experience_history))
            success_rate = successful / len(merged_experiences) if merged_experiences else 0.0
            
            # Increase confidence with more occurrences
            confidence = min(0.5 + (merged_frequency * 0.1), 1.0)
            
            updated = LearnedPattern(
                pattern_id=existing.pattern_id,
                pattern_type=existing.pattern_type,
                description=existing.description,
                frequency=merged_frequency,
                success_rate=success_rate,
                confidence=confidence,
                last_seen=new_pattern.last_seen,
                related_experiences=merged_experiences
            )
            return updated
        else:
            # New pattern
            return new_pattern
    
    def get_recommendations(self, context: Dict[str, Any]) -> List[str]:
        """
        Get recommendations based on learned patterns.
        
        This demonstrates:
        - Pattern-based recommendations
        - Context-aware suggestions
        - Adaptive recommendations
        
        Args:
            context: Current context for recommendations
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Find relevant patterns
        relevant_patterns = self._find_relevant_patterns(context)
        
        # Generate recommendations from patterns
        for pattern in relevant_patterns:
            if pattern.success_rate > 0.8 and pattern.confidence > 0.7:
                recommendations.append(
                    f"Use {pattern.description} (high success rate: {pattern.success_rate:.2f})"
                )
            elif pattern.success_rate < 0.3 and pattern.confidence > 0.7:
                recommendations.append(
                    f"Avoid {pattern.description} (low success rate: {pattern.success_rate:.2f})"
                )
        
        return recommendations
    
    def _find_relevant_patterns(self, context: Dict[str, Any]) -> List[LearnedPattern]:
        """
        Find patterns relevant to current context.
        
        Args:
            context: Current context
            
        Returns:
            List of relevant patterns
        """
        # Simple relevance matching - in production would use semantic similarity
        relevant = []
        for pattern in self.learned_patterns.values():
            # Check if pattern matches context
            if self._pattern_matches_context(pattern, context):
                relevant.append(pattern)
        
        # Sort by confidence and recency
        relevant.sort(key=lambda p: (p.confidence, p.last_seen), reverse=True)
        
        return relevant[:5]  # Return top 5
    
    def _pattern_matches_context(self, pattern: LearnedPattern, context: Dict[str, Any]) -> bool:
        """
        Check if pattern matches context.
        
        Args:
            pattern: Pattern to check
            context: Current context
            
        Returns:
            True if pattern matches context
        """
        # Simplified matching - in production would use semantic similarity
        return True  # For now, return all patterns
    
    def adapt_behavior(self, pattern: LearnedPattern) -> Optional[Adaptation]:
        """
        Generate adaptation based on learned pattern.
        
        This demonstrates:
        - Adaptive behavior generation
        - Strategy adjustments
        - Parameter optimization
        
        Args:
            pattern: Pattern to adapt from
            
        Returns:
            Adaptation recommendation or None
        """
        if pattern.success_rate > 0.9 and pattern.confidence > 0.8:
            # High success pattern - reinforce
            adaptation = Adaptation(
                adaptation_id=f"adapt_{pattern.pattern_id}",
                pattern_id=pattern.pattern_id,
                adaptation_type="strategy_change",
                description=f"Reinforce successful pattern: {pattern.description}",
                expected_improvement=0.1,
                confidence=0.8
            )
            return adaptation
        elif pattern.success_rate < 0.2 and pattern.confidence > 0.8:
            # Low success pattern - avoid
            adaptation = Adaptation(
                adaptation_id=f"adapt_{pattern.pattern_id}",
                pattern_id=pattern.pattern_id,
                adaptation_type="strategy_change",
                description=f"Avoid failing pattern: {pattern.description}",
                expected_improvement=0.2,
                confidence=0.8
            )
            return adaptation
        
        return None
