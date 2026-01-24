"""
Memory Node Implementation Example

This file demonstrates the Memory Node implementation following READ→DO→WRITE→CONTROL pattern.
Reference this example from RULE.mdc using @examples_memory_node.py syntax.
"""

from typing import TypedDict, List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Memory Node State Types
# ============================================================================

@dataclass
class Experience:
    """Experience structure for storing actions, context, and results."""
    experience_id: str
    actions: List[Dict[str, Any]]
    context: Dict[str, Any]
    results: Dict[str, Any]
    success: bool
    feedback: Optional[str] = None


@dataclass
class Memory:
    """Memory structure for historical context."""
    memory_id: str
    content: str
    relevance_score: float
    timestamp: str
    source: str
    metadata: Dict[str, Any]


@dataclass
class Feedback:
    """Feedback structure for Planner."""
    feedback_id: str
    insights: List[str]
    patterns: List[str]
    recommendations: List[str]
    confidence: float


class MemoryOperation(str, Enum):
    """Memory operation types."""
    LOAD = "load"
    STORE = "store"
    FEEDBACK = "feedback"


class MemoryNodeState(TypedDict):
    """State structure for Memory Node."""
    user_request: Optional[str]
    context: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]
    memories: Optional[List[Memory]]
    feedback: Optional[Feedback]
    experiences: Optional[List[Experience]]


# ============================================================================
# Memory Node Implementation
# ============================================================================

class MemoryNode:
    """
    Memory Node implementation following READ→DO→WRITE→CONTROL pattern.
    
    This demonstrates:
    - READ: Read state, context, and retrieve memories from storage
    - DO: Process memories, extract insights, provide feedback
    - WRITE: Write memories, feedback, or context to state
    - CONTROL: Route to next node based on operation type
    """
    
    def __init__(self, storage_service: Any):
        """
        Initialize Memory Node.
        
        Args:
            storage_service: Memory storage service (from memory-and-archival-management)
        """
        self.storage_service = storage_service
    
    def memory_node(self, state: MemoryNodeState, operation: MemoryOperation) -> MemoryNodeState:
        """
        Memory Node following READ→DO→WRITE→CONTROL pattern.
        
        Args:
            state: Current state
            operation: Operation type (load, store, feedback)
            
        Returns:
            Updated state with memories, feedback, or experiences
        """
        if operation == MemoryOperation.LOAD:
            return self._load_memories(state)
        elif operation == MemoryOperation.STORE:
            return self._store_experiences(state)
        elif operation == MemoryOperation.FEEDBACK:
            return self._provide_feedback(state)
        else:
            return state
    
    def _load_memories(self, state: MemoryNodeState) -> MemoryNodeState:
        """
        Load relevant memories operation.
        
        READ: Read user context and conversation state
        DO: Retrieve relevant memories from storage service
        WRITE: Write memories to state
        CONTROL: Route to next node
        """
        # READ: Read context
        context = state.get("context", {})
        user_request = state.get("user_request", "")
        
        # DO: Retrieve memories from storage
        memories = self.storage_service.retrieve_memories(
            query=user_request,
            context=context,
            top_k=5
        )
        
        # WRITE: Write memories to state
        state["memories"] = memories
        
        # CONTROL: State updated, routing handled by graph
        return state
    
    def _store_experiences(self, state: MemoryNodeState) -> MemoryNodeState:
        """
        Store experiences operation.
        
        READ: Read actions, context, and results from state
        DO: Extract experience, format, and store via storage service
        WRITE: Write memory IDs and confirmation to state
        CONTROL: Route to next node
        """
        # READ: Read experiences
        experiences = state.get("experiences", [])
        context = state.get("context", {})
        
        # DO: Store experiences
        memory_ids = []
        for experience in experiences:
            memory_id = self.storage_service.store_experience(
                experience=experience,
                context=context
            )
            memory_ids.append(memory_id)
        
        # WRITE: Write memory IDs
        state["memory_ids"] = memory_ids
        
        # CONTROL: State updated, routing handled by graph
        return state
    
    def _provide_feedback(self, state: MemoryNodeState) -> MemoryNodeState:
        """
        Provide feedback to Planner operation.
        
        READ: Read stored experiences and patterns
        DO: Analyze experiences, extract insights, generate feedback
        WRITE: Write feedback to state for Planner
        CONTROL: Route feedback to Planner node
        """
        # READ: Read memories and experiences
        memories = state.get("memories", [])
        experiences = state.get("experiences", [])
        
        # DO: Generate feedback
        insights = self._extract_insights(experiences)
        patterns = self._identify_patterns(experiences)
        recommendations = self._generate_recommendations(insights, patterns)
        
        feedback = Feedback(
            feedback_id="feedback_1",
            insights=insights,
            patterns=patterns,
            recommendations=recommendations,
            confidence=0.85
        )
        
        # WRITE: Write feedback to state
        state["feedback"] = feedback
        
        # CONTROL: State updated, routing handled by graph
        return state
    
    def _extract_insights(self, experiences: List[Experience]) -> List[str]:
        """Extract insights from experiences."""
        insights = []
        for exp in experiences:
            if exp.success:
                insights.append(f"Success pattern: {exp.actions}")
            else:
                insights.append(f"Failure pattern: {exp.actions}")
        return insights
    
    def _identify_patterns(self, experiences: List[Experience]) -> List[str]:
        """Identify patterns from experiences."""
        # Implementation would analyze experiences for patterns
        return ["Pattern 1", "Pattern 2"]
    
    def _generate_recommendations(self, insights: List[str], patterns: List[str]) -> List[str]:
        """Generate recommendations based on insights and patterns."""
        # Implementation would generate recommendations
        return ["Recommendation 1", "Recommendation 2"]
