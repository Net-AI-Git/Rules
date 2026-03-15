"""
Retention Criteria Examples

This file demonstrates retention criteria and importance scoring patterns.
Reference this example from RULE.mdc using @examples_retention.py syntax.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

from examples_compression import Message


# ============================================================================
# Importance Scoring
# ============================================================================

class MessageType(Enum):
    """
    Message types for importance scoring.
    
    This demonstrates message categorization:
    - User requests are most important
    - System instructions are critical
    - Tool results vary by relevance
    """
    USER_REQUEST = "user_request"
    SYSTEM_INSTRUCTION = "system_instruction"
    AGENT_RESPONSE = "agent_response"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    PREFERENCE = "preference"


@dataclass
class ImportanceScore:
    """
    Importance score for a message.
    
    This demonstrates importance scoring:
    - Base score by message type
    - Recency multiplier
    - Relevance score
    - Final combined score
    """
    base_score: float  # 0.0-1.0 based on message type
    recency_multiplier: float  # 0.0-1.0 based on age
    relevance_score: float  # 0.0-1.0 based on relevance to current task
    final_score: float  # Combined score
    
    def __post_init__(self):
        """Calculate final score after initialization."""
        self.final_score = self.base_score * self.recency_multiplier * (0.7 + 0.3 * self.relevance_score)


class ImportanceScorer:
    """
    Service for scoring message importance.
    
    This demonstrates importance scoring patterns:
    - Type-based scoring
    - Recency weighting
    - Relevance calculation
    - Combined scoring
    """
    
    def __init__(self):
        """Initialize importance scorer."""
        # Base scores by message type
        self.type_scores = {
            MessageType.USER_REQUEST: 1.0,
            MessageType.SYSTEM_INSTRUCTION: 0.95,
            MessageType.PREFERENCE: 0.9,
            MessageType.ERROR: 0.85,
            MessageType.AGENT_RESPONSE: 0.6,
            MessageType.TOOL_RESULT: 0.5
        }
    
    def score_message(
        self,
        message: Message,
        current_time: datetime,
        current_task: Optional[str] = None
    ) -> ImportanceScore:
        """
        Score message importance.
        
        Args:
            message: Message to score
            current_time: Current timestamp
            current_task: Optional current task for relevance
        
        Returns:
            ImportanceScore
        """
        # Determine message type
        msg_type = self._classify_message(message)
        base_score = self.type_scores.get(msg_type, 0.5)
        
        # Calculate recency multiplier
        recency_multiplier = self._calculate_recency(message.timestamp, current_time)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance(message, current_task)
        
        score = ImportanceScore(
            base_score=base_score,
            recency_multiplier=recency_multiplier,
            relevance_score=relevance_score,
            final_score=0.0  # Will be calculated in __post_init__
        )
        
        return score
    
    def _classify_message(self, message: Message) -> MessageType:
        """
        Classify message type.
        
        Args:
            message: Message to classify
            
        Returns:
            MessageType
        """
        role = message.role.lower()
        content = message.content.lower()
        
        if role == "user":
            return MessageType.USER_REQUEST
        elif role == "system":
            return MessageType.SYSTEM_INSTRUCTION
        elif "preference" in content or "i prefer" in content or "i like" in content:
            return MessageType.PREFERENCE
        elif "error" in content or "failed" in content:
            return MessageType.ERROR
        elif role == "tool":
            return MessageType.TOOL_RESULT
        else:
            return MessageType.AGENT_RESPONSE
    
    def _calculate_recency(self, message_time: datetime, current_time: datetime) -> float:
        """
        Calculate recency multiplier.
        
        Args:
            message_time: Message timestamp
            current_time: Current timestamp
            
        Returns:
            Recency multiplier (0.0-1.0)
        """
        age_seconds = (current_time - message_time).total_seconds()
        
        # Recent messages (last 10% of conversation) get full weight
        # Older messages get progressively lower weight
        if age_seconds < 300:  # Last 5 minutes
            return 1.0
        elif age_seconds < 1800:  # Last 30 minutes
            return 0.9
        elif age_seconds < 3600:  # Last hour
            return 0.7
        elif age_seconds < 7200:  # Last 2 hours
            return 0.5
        else:
            return 0.3
    
    def _calculate_relevance(self, message: Message, current_task: Optional[str]) -> float:
        """
        Calculate relevance to current task.
        
        Args:
            message: Message to evaluate
            current_task: Current task description
            
        Returns:
            Relevance score (0.0-1.0)
        """
        if not current_task:
            return 0.7  # Default relevance
        
        # In real implementation, use semantic similarity or keyword matching
        # For now, simple keyword matching
        task_keywords = set(current_task.lower().split())
        message_keywords = set(message.content.lower().split())
        
        if not task_keywords:
            return 0.7
        
        overlap = len(task_keywords & message_keywords) / len(task_keywords)
        return min(1.0, overlap * 2)  # Scale to 0.0-1.0


# ============================================================================
# Retention Criteria
# ============================================================================

class RetentionCriteria:
    """
    Service for determining what to keep, summarize, or discard.
    
    This demonstrates retention criteria patterns:
    - Mandatory retention
    - High priority retention
    - Summarization candidates
    - Safe to discard
    """
    
    def __init__(self, importance_scorer: ImportanceScorer):
        """
        Initialize retention criteria.
        
        Args:
            importance_scorer: Importance scorer instance
        """
        self.importance_scorer = importance_scorer
    
    def classify_messages(
        self,
        messages: List[Message],
        current_time: datetime,
        current_task: Optional[str] = None
    ) -> Dict[str, List[Message]]:
        """
        Classify messages into retention categories.
        
        Args:
            messages: List of messages
            current_time: Current timestamp
            current_task: Optional current task
        
        Returns:
            Dictionary with categorized messages
        """
        classified = {
            "keep": [],
            "summarize": [],
            "discard": []
        }
        
        for message in messages:
            score = self.importance_scorer.score_message(message, current_time, current_task)
            category = self._categorize_by_score(score, message)
            classified[category].append(message)
        
        return classified
    
    def _categorize_by_score(self, score: ImportanceScore, message: Message) -> str:
        """
        Categorize message based on importance score.
        
        Args:
            score: Importance score
            message: Message to categorize
            
        Returns:
            Category: "keep", "summarize", or "discard"
        """
        # Mandatory keep: high importance, recent, or critical type
        if score.final_score >= 0.8:
            return "keep"
        if message.role == "system" or message.role == "user":
            return "keep"
        if "error" in message.content.lower() or "critical" in message.content.lower():
            return "keep"
        
        # Summarize: medium importance
        if score.final_score >= 0.4:
            return "summarize"
        
        # Discard: low importance
        return "discard"
    
    def get_retention_plan(
        self,
        messages: List[Message],
        target_tokens: int,
        current_time: datetime,
        current_task: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create retention plan for messages.
        
        Args:
            messages: List of messages
            target_tokens: Target token count
            current_time: Current timestamp
            current_task: Optional current task
        
        Returns:
            Retention plan with actions for each message
        """
        classified = self.classify_messages(messages, current_time, current_task)
        
        plan = {
            "keep": classified["keep"],
            "summarize": classified["summarize"],
            "discard": classified["discard"],
            "target_tokens": target_tokens,
            "estimated_tokens_after": self._estimate_tokens(classified)
        }
        
        return plan
    
    def _estimate_tokens(self, classified: Dict[str, List[Message]]) -> int:
        """
        Estimate tokens after retention plan.
        
        Args:
            classified: Classified messages
        
        Returns:
            Estimated token count
        """
        # Keep all "keep" messages
        keep_tokens = sum(msg.token_count for msg in classified["keep"])
        
        # Summarize "summarize" messages (estimate 30% of original)
        summarize_tokens = int(sum(msg.token_count for msg in classified["summarize"]) * 0.3)
        
        # Discard "discard" messages (0 tokens)
        
        return keep_tokens + summarize_tokens


# ============================================================================
# Retention Service
# ============================================================================

class RetentionService:
    """
    Service for applying retention criteria.
    
    This demonstrates retention service pattern:
    - Score all messages
    - Classify by retention criteria
    - Apply retention plan
    - Validate results
    """
    
    def __init__(self, importance_scorer: ImportanceScorer):
        """
        Initialize retention service.
        
        Args:
            importance_scorer: Importance scorer instance
        """
        self.importance_scorer = importance_scorer
        self.retention_criteria = RetentionCriteria(importance_scorer)
    
    def apply_retention(
        self,
        messages: List[Message],
        target_tokens: int,
        current_time: datetime,
        current_task: Optional[str] = None
    ) -> List[Message]:
        """
        Apply retention criteria to messages.
        
        Args:
            messages: List of messages
            target_tokens: Target token count
            current_time: Current timestamp
            current_task: Optional current task
        
        Returns:
            Retained messages (kept + summarized)
        """
        # Get retention plan
        plan = self.retention_criteria.get_retention_plan(
            messages, target_tokens, current_time, current_task
        )
        
        # Keep all "keep" messages
        retained = plan["keep"].copy()
        
        # Summarize "summarize" messages
        if plan["summarize"]:
            summarized = self._summarize_messages(plan["summarize"])
            retained.extend(summarized)
        
        # Discard "discard" messages (not added to retained)
        
        # Sort by timestamp to maintain order
        retained.sort(key=lambda m: m.timestamp)
        
        return retained
    
    def _summarize_messages(self, messages: List[Message]) -> List[Message]:
        """
        Summarize a group of messages.
        
        Args:
            messages: Messages to summarize
        
        Returns:
            List of summarized messages (usually one)
        """
        if not messages:
            return []
        
        # Combine messages into summary
        combined_content = "\n".join([f"{msg.role}: {msg.content[:100]}..." for msg in messages])
        summary_content = f"[Summary of {len(messages)} messages] {combined_content[:500]}"
        
        # Create summary message
        summary_message = Message(
            role="system",
            content=summary_content,
            timestamp=messages[0].timestamp,
            token_count=len(summary_content) // 4,
            importance_score=0.6,
            metadata={"summarized_count": len(messages), "original_messages": [m.content[:50] for m in messages]}
        )
        
        return [summary_message]
