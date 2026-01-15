"""
Memory Update Examples

This file demonstrates update strategies, incremental updates, and event-driven patterns.
Reference this example from RULE.mdc using @examples_memory_updates.py syntax.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from examples_memory_storage import (
    UserMemory, MemoryType, MemoryStorageService, VectorDBInterface
)


# ============================================================================
# Update Strategies
# ============================================================================

class UpdateStrategy(Enum):
    """
    Memory update strategies.
    
    This demonstrates different update approaches:
    - Post-session: Update after conversation ends
    - Incremental: Update during conversation
    - Event-driven: Update on specific events
    """
    POST_SESSION = "post_session"
    INCREMENTAL = "incremental"
    EVENT_DRIVEN = "event_driven"


@dataclass
class MemoryExtraction:
    """
    Extracted memory from conversation.
    
    This demonstrates memory extraction structure:
    - Content to store
    - Memory type
    - Confidence score
    - Metadata
    """
    content: str
    memory_type: MemoryType
    confidence_score: float
    metadata: Dict[str, Any]
    source: str


class MemoryExtractionService:
    """
    Service for extracting memories from conversations.
    
    This demonstrates memory extraction patterns:
    - Extract user preferences
    - Extract contextual insights
    - Extract behavioral patterns
    - Validate and score extractions
    """
    
    def __init__(self, storage_service: MemoryStorageService):
        """
        Initialize extraction service.
        
        Args:
            storage_service: Memory storage service
        """
        self.storage_service = storage_service
    
    def extract_from_conversation(
        self,
        user_id: str,
        conversation_messages: List[Dict[str, Any]],
        tenant_id: Optional[str] = None
    ) -> List[MemoryExtraction]:
        """
        Extract memories from conversation messages.
        
        This demonstrates post-session extraction:
        - Analyze conversation messages
        - Extract key insights
        - Score and validate extractions
        - Return list of memories to store
        
        Args:
            user_id: User ID
            conversation_messages: List of conversation messages
            tenant_id: Optional tenant ID
            
        Returns:
            List of extracted memories
        """
        extractions = []
        
        # In real implementation, use LLM or rule-based extraction:
        # 1. Analyze conversation for user preferences
        # 2. Identify important facts and insights
        # 3. Detect behavioral patterns
        # 4. Score confidence for each extraction
        
        # Example: Extract user preferences
        preferences = self._extract_preferences(conversation_messages)
        for pref in preferences:
            extractions.append(MemoryExtraction(
                content=pref["content"],
                memory_type=MemoryType.USER_PROFILE,
                confidence_score=pref.get("confidence", 0.8),
                metadata=pref.get("metadata", {}),
                source="conversation_analysis"
            ))
        
        # Example: Extract contextual insights
        insights = self._extract_insights(conversation_messages)
        for insight in insights:
            extractions.append(MemoryExtraction(
                content=insight["content"],
                memory_type=MemoryType.CONTEXTUAL_INSIGHT,
                confidence_score=insight.get("confidence", 0.7),
                metadata=insight.get("metadata", {}),
                source="conversation_analysis"
            ))
        
        return extractions
    
    def extract_incremental(
        self,
        user_id: str,
        message: Dict[str, Any],
        tenant_id: Optional[str] = None
    ) -> Optional[MemoryExtraction]:
        """
        Extract memory incrementally from single message.
        
        This demonstrates incremental extraction:
        - Analyze single message
        - Extract if significant insight detected
        - Return single extraction or None
        
        Args:
            user_id: User ID
            message: Single conversation message
            tenant_id: Optional tenant ID
            
        Returns:
            Memory extraction or None
        """
        # In real implementation:
        # 1. Check if message contains significant information
        # 2. Extract if confidence is high
        # 3. Return extraction or None
        
        # Example: Check for explicit preference statement
        if self._is_explicit_preference(message):
            return MemoryExtraction(
                content=self._extract_preference_content(message),
                memory_type=MemoryType.USER_PROFILE,
                confidence_score=0.9,  # High confidence for explicit statements
                metadata={"extraction_method": "explicit_preference"},
                source="incremental_analysis"
            )
        
        return None
    
    def _extract_preferences(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract user preferences from messages."""
        # In real implementation, use LLM or NLP to extract preferences
        return []
    
    def _extract_insights(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract contextual insights from messages."""
        # In real implementation, use LLM or NLP to extract insights
        return []
    
    def _is_explicit_preference(self, message: Dict[str, Any]) -> bool:
        """Check if message contains explicit preference."""
        # In real implementation, use pattern matching or LLM
        text = message.get("content", "").lower()
        preference_indicators = ["i prefer", "i like", "i want", "i need", "my preference"]
        return any(indicator in text for indicator in preference_indicators)
    
    def _extract_preference_content(self, message: Dict[str, Any]) -> str:
        """Extract preference content from message."""
        # In real implementation, use NLP to extract structured preference
        return message.get("content", "")


# ============================================================================
# Update Service
# ============================================================================

class MemoryUpdateService:
    """
    Service for updating long-term memory.
    
    This demonstrates memory update patterns:
    - Post-session updates
    - Incremental updates
    - Event-driven updates
    - Batch operations
    """
    
    def __init__(
        self,
        storage_service: MemoryStorageService,
        extraction_service: MemoryExtractionService
    ):
        """
        Initialize update service.
        
        Args:
            storage_service: Memory storage service
            extraction_service: Memory extraction service
        """
        self.storage_service = storage_service
        self.extraction_service = extraction_service
    
    def update_post_session(
        self,
        user_id: str,
        conversation_messages: List[Dict[str, Any]],
        tenant_id: Optional[str] = None
    ) -> List[str]:
        """
        Update memory after conversation session ends.
        
        This demonstrates post-session update:
        - Extract memories from conversation
        - Store in Vector DB
        - Update user profile
        - Return memory IDs
        
        Args:
            user_id: User ID
            conversation_messages: Conversation messages
            tenant_id: Optional tenant ID
            
        Returns:
            List of stored memory IDs
        """
        # Extract memories
        extractions = self.extraction_service.extract_from_conversation(
            user_id=user_id,
            conversation_messages=conversation_messages,
            tenant_id=tenant_id
        )
        
        # Store memories
        memory_ids = []
        for extraction in extractions:
            memory_id = self.storage_service.store_user_memory(
                user_id=user_id,
                content=extraction.content,
                memory_type=extraction.memory_type,
                metadata=extraction.metadata,
                confidence_score=extraction.confidence_score,
                source=extraction.source,
                tenant_id=tenant_id
            )
            memory_ids.append(memory_id)
        
        return memory_ids
    
    def update_incremental(
        self,
        user_id: str,
        message: Dict[str, Any],
        tenant_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Update memory incrementally during conversation.
        
        This demonstrates incremental update:
        - Extract from single message
        - Store immediately if significant
        - Return memory ID or None
        
        Args:
            user_id: User ID
            message: Single message
            tenant_id: Optional tenant ID
            
        Returns:
            Memory ID or None
        """
        # Extract memory
        extraction = self.extraction_service.extract_incremental(
            user_id=user_id,
            message=message,
            tenant_id=tenant_id
        )
        
        if not extraction:
            return None
        
        # Store immediately
        memory_id = self.storage_service.store_user_memory(
            user_id=user_id,
            content=extraction.content,
            memory_type=extraction.memory_type,
            metadata=extraction.metadata,
            confidence_score=extraction.confidence_score,
            source=extraction.source,
            tenant_id=tenant_id
        )
        
        return memory_id
    
    def update_on_event(
        self,
        user_id: str,
        event_type: str,
        event_data: Dict[str, Any],
        tenant_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Update memory on specific event.
        
        This demonstrates event-driven update:
        - Handle specific events (e.g., user confirms preference)
        - Extract memory from event
        - Store with high confidence
        - Return memory ID
        
        Args:
            user_id: User ID
            event_type: Type of event
            event_data: Event data
            tenant_id: Optional tenant ID
            
        Returns:
            Memory ID or None
        """
        # Handle specific events
        if event_type == "preference_confirmed":
            content = f"User confirmed preference: {event_data.get('preference', '')}"
            memory_id = self.storage_service.store_user_memory(
                user_id=user_id,
                content=content,
                memory_type=MemoryType.USER_PROFILE,
                metadata={"event_type": event_type, **event_data},
                confidence_score=0.95,  # High confidence for explicit confirmation
                source="user_event",
                tenant_id=tenant_id
            )
            return memory_id
        
        return None
    
    def batch_update(
        self,
        user_id: str,
        extractions: List[MemoryExtraction],
        tenant_id: Optional[str] = None
    ) -> List[str]:
        """
        Batch update multiple memories.
        
        This demonstrates batch update pattern:
        - Store multiple memories efficiently
        - Return all memory IDs
        - Handle errors gracefully
        
        Args:
            user_id: User ID
            extractions: List of memory extractions
            tenant_id: Optional tenant ID
            
        Returns:
            List of stored memory IDs
        """
        memory_ids = []
        
        for extraction in extractions:
            try:
                memory_id = self.storage_service.store_user_memory(
                    user_id=user_id,
                    content=extraction.content,
                    memory_type=extraction.memory_type,
                    metadata=extraction.metadata,
                    confidence_score=extraction.confidence_score,
                    source=extraction.source,
                    tenant_id=tenant_id
                )
                memory_ids.append(memory_id)
            except Exception as e:
                # Log error but continue with other memories
                # In real implementation, use proper logging
                pass
        
        return memory_ids
