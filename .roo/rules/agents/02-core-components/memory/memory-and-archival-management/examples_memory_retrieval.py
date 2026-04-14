"""
Memory Retrieval Examples

This file demonstrates semantic search and relevance-based retrieval patterns.
Reference this example from RULE.mdc using @examples_memory_retrieval.py syntax.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from examples_memory_storage import UserMemory, MemoryType, MemoryStorageService


# ============================================================================
# Retrieval Strategies
# ============================================================================

class RetrievalStrategy(Enum):
    """
    Memory retrieval strategies.
    
    This demonstrates different retrieval approaches:
    - Semantic search for relevance
    - Hybrid search (semantic + keyword)
    - Time-based filtering
    - Type-based filtering
    """
    SEMANTIC = "semantic"
    HYBRID = "hybrid"
    KEYWORD = "keyword"
    TIME_BASED = "time_based"


@dataclass
class RetrievalConfig:
    """
    Configuration for memory retrieval.
    
    This demonstrates retrieval configuration:
    - Number of results
    - Relevance thresholds
    - Filtering options
    - Token budget constraints
    """
    top_k: int = 10
    min_confidence: float = 0.5
    min_relevance_score: float = 0.7
    memory_types: Optional[List[MemoryType]] = None
    max_tokens: Optional[int] = None  # Token budget for loaded memories
    include_metadata: bool = True


class MemoryRetrievalService:
    """
    Service for retrieving relevant memories.
    
    This demonstrates memory retrieval patterns:
    - Semantic search
    - Relevance filtering
    - Token-aware loading
    - Context formatting
    """
    
    def __init__(self, storage_service: MemoryStorageService):
        """
        Initialize retrieval service.
        
        Args:
            storage_service: Memory storage service
        """
        self.storage_service = storage_service
    
    def retrieve_for_conversation_start(
        self,
        user_id: str,
        tenant_id: Optional[str] = None,
        config: Optional[RetrievalConfig] = None
    ) -> Dict[str, Any]:
        """
        Retrieve memories at conversation start.
        
        This demonstrates loading user profile at conversation start:
        - Load user profile
        - Load recent high-confidence memories
        - Format for context window
        
        Args:
            user_id: User ID
            tenant_id: Optional tenant ID
            config: Retrieval configuration
            
        Returns:
            Dictionary with loaded memories formatted for context
        """
        config = config or RetrievalConfig()
        
        # Load user profile
        profile = self.storage_service.vector_db.get_user_profile(user_id, tenant_id)
        
        # Load recent high-confidence memories
        recent_memories = self.storage_service.retrieve_relevant_memories(
            user_id=user_id,
            query="user preferences and recent context",
            top_k=config.top_k,
            min_confidence=config.min_confidence,
            tenant_id=tenant_id
        )
        
        # Format for context
        context = self._format_memories_for_context(
            profile=profile,
            memories=recent_memories,
            max_tokens=config.max_tokens
        )
        
        return context
    
    def retrieve_on_demand(
        self,
        user_id: str,
        query: str,
        tenant_id: Optional[str] = None,
        config: Optional[RetrievalConfig] = None
    ) -> List[UserMemory]:
        """
        Retrieve memories on-demand during conversation.
        
        This demonstrates on-demand retrieval:
        - Query current conversation context
        - Find relevant memories
        - Return filtered results
        
        Args:
            user_id: User ID
            query: Query text (from current conversation)
            tenant_id: Optional tenant ID
            config: Retrieval configuration
            
        Returns:
            List of relevant memories
        """
        config = config or RetrievalConfig()
        
        memories = self.storage_service.retrieve_relevant_memories(
            user_id=user_id,
            query=query,
            top_k=config.top_k,
            memory_type=None,  # Search all types
            min_confidence=config.min_confidence,
            tenant_id=tenant_id
        )
        
        # Filter by relevance score if available
        if config.min_relevance_score:
            memories = [
                m for m in memories
                if m.metadata.get("relevance_score", 1.0) >= config.min_relevance_score
            ]
        
        return memories
    
    def retrieve_by_type(
        self,
        user_id: str,
        memory_type: MemoryType,
        query: Optional[str] = None,
        tenant_id: Optional[str] = None,
        config: Optional[RetrievalConfig] = None
    ) -> List[UserMemory]:
        """
        Retrieve memories filtered by type.
        
        This demonstrates type-based retrieval:
        - Filter by memory type
        - Optional query for semantic search
        - Return type-specific memories
        
        Args:
            user_id: User ID
            memory_type: Type of memory to retrieve
            query: Optional query for semantic search
            tenant_id: Optional tenant ID
            config: Retrieval configuration
            
        Returns:
            List of memories of specified type
        """
        config = config or RetrievalConfig()
        
        query = query or f"{memory_type.value} information"
        
        memories = self.storage_service.retrieve_relevant_memories(
            user_id=user_id,
            query=query,
            top_k=config.top_k,
            memory_type=memory_type,
            min_confidence=config.min_confidence,
            tenant_id=tenant_id
        )
        
        return memories
    
    def _format_memories_for_context(
        self,
        profile: Optional[Any],
        memories: List[UserMemory],
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Format memories for inclusion in context window.
        
        This demonstrates context formatting:
        - Summarize user profile
        - Format key memories
        - Respect token budget
        - Structure for LLM consumption
        
        Args:
            profile: User profile
            memories: List of memories
            max_tokens: Optional token budget
            
        Returns:
            Formatted context dictionary
        """
        context = {
            "user_profile_summary": self._summarize_profile(profile) if profile else None,
            "relevant_memories": [],
            "memory_count": len(memories)
        }
        
        # Format memories
        for memory in memories:
            memory_context = {
                "type": memory.memory_type.value,
                "content": memory.content,
                "confidence": memory.confidence_score,
                "source": memory.source
            }
            context["relevant_memories"].append(memory_context)
        
        # Apply token budget if specified
        if max_tokens:
            context = self._apply_token_budget(context, max_tokens)
        
        return context
    
    def _summarize_profile(self, profile: Any) -> Dict[str, Any]:
        """
        Summarize user profile for context.
        
        Args:
            profile: User profile
            
        Returns:
            Summarized profile dictionary
        """
        # In real implementation, create concise summary
        return {
            "preferences": profile.preferences if hasattr(profile, 'preferences') else {},
            "expertise": profile.expertise_domains if hasattr(profile, 'expertise_domains') else [],
            "communication_style": profile.communication_style if hasattr(profile, 'communication_style') else {}
        }
    
    def _apply_token_budget(
        self,
        context: Dict[str, Any],
        max_tokens: int
    ) -> Dict[str, Any]:
        """
        Apply token budget to context.
        
        Args:
            context: Context dictionary
            max_tokens: Maximum tokens allowed
            
        Returns:
            Context with token budget applied
        """
        # In real implementation:
        # 1. Estimate tokens for each memory
        # 2. Prioritize high-confidence, recent memories
        # 3. Summarize or truncate to fit budget
        # 4. Return filtered context
        
        # Simple implementation: limit number of memories
        if len(context["relevant_memories"]) > max_tokens // 50:  # Rough estimate
            context["relevant_memories"] = context["relevant_memories"][:max_tokens // 50]
        
        return context


# ============================================================================
# Hybrid Search Implementation
# ============================================================================

class HybridMemorySearch:
    """
    Hybrid search combining semantic and keyword search.
    
    This demonstrates hybrid search pattern:
    - Semantic search for relevance
    - Keyword search for exact matches
    - Combine and rerank results
    """
    
    def __init__(self, storage_service: MemoryStorageService):
        """
        Initialize hybrid search.
        
        Args:
            storage_service: Memory storage service
        """
        self.storage_service = storage_service
    
    def search(
        self,
        user_id: str,
        query: str,
        keywords: Optional[List[str]] = None,
        top_k: int = 10,
        tenant_id: Optional[str] = None
    ) -> List[UserMemory]:
        """
        Perform hybrid search.
        
        Args:
            user_id: User ID
            query: Semantic query
            keywords: Optional keywords for exact matching
            top_k: Number of results
            tenant_id: Optional tenant ID
            
        Returns:
            Combined and reranked results
        """
        # Semantic search
        semantic_results = self.storage_service.retrieve_relevant_memories(
            user_id=user_id,
            query=query,
            top_k=top_k * 2,  # Get more for reranking
            tenant_id=tenant_id
        )
        
        # Keyword search (if keywords provided)
        keyword_results = []
        if keywords:
            # In real implementation, perform keyword search
            # keyword_results = self._keyword_search(user_id, keywords, tenant_id)
            pass
        
        # Combine and rerank
        combined = self._combine_and_rerank(semantic_results, keyword_results, top_k)
        
        return combined
    
    def _combine_and_rerank(
        self,
        semantic_results: List[UserMemory],
        keyword_results: List[UserMemory],
        top_k: int
    ) -> List[UserMemory]:
        """
        Combine and rerank search results.
        
        Args:
            semantic_results: Results from semantic search
            keyword_results: Results from keyword search
            top_k: Number of final results
            
        Returns:
            Reranked results
        """
        # In real implementation:
        # 1. Combine results (deduplicate by memory_id)
        # 2. Score each result (semantic score + keyword match bonus)
        # 3. Sort by combined score
        # 4. Return top_k
        
        # Simple implementation: prioritize keyword matches, then semantic
        all_results = {}
        
        # Add keyword results with bonus
        for memory in keyword_results:
            all_results[memory.memory_id] = (memory, 2.0)  # Higher score for keyword match
        
        # Add semantic results
        for memory in semantic_results:
            if memory.memory_id not in all_results:
                all_results[memory.memory_id] = (memory, 1.0)
        
        # Sort by score and return top_k
        sorted_results = sorted(
            all_results.values(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [memory for memory, _ in sorted_results[:top_k]]
