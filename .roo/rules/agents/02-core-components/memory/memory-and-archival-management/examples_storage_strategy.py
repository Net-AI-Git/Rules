"""
Storage Strategy Examples

This file demonstrates storage decision logic and Vector DB vs PostgreSQL patterns.
Reference this example from RULE.mdc using @examples_storage_strategy.py syntax.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Storage Types
# ============================================================================

class StorageType(Enum):
    """
    Storage types for different memory data.
    
    This demonstrates storage type classification:
    - Vector DB for semantic search
    - PostgreSQL for structured data
    - Hybrid for combined approach
    """
    VECTOR_DB = "vector_db"
    POSTGRESQL = "postgresql"
    HYBRID = "hybrid"


class MemoryDataType(Enum):
    """
    Types of memory data.
    
    This demonstrates memory data classification:
    - Structured data for PostgreSQL
    - Unstructured data for Vector DB
    - Hybrid data for both
    """
    STRUCTURED_PROFILE = "structured_profile"
    UNSTRUCTURED_INSIGHT = "unstructured_insight"
    SEMANTIC_MEMORY = "semantic_memory"
    RELATIONAL_DATA = "relational_data"


# ============================================================================
# Storage Decision Logic
# ============================================================================

@dataclass
class StorageDecision:
    """
    Storage decision result.
    
    This demonstrates storage decision structure:
    - Storage type recommendation
    - Reasoning
    - Alternative options
    """
    storage_type: StorageType
    reasoning: str
    alternative: Optional[StorageType] = None
    use_hybrid: bool = False


class StorageStrategyDecider:
    """
    Service for deciding storage strategy.
    
    This demonstrates storage decision patterns:
    - Analyze data type and query patterns
    - Recommend appropriate storage
    - Consider hybrid approaches
    """
    
    def decide_storage(
        self,
        data_type: MemoryDataType,
        query_pattern: str,
        update_frequency: str = "medium",
        data_structure: str = "unstructured"
    ) -> StorageDecision:
        """
        Decide storage strategy based on criteria.
        
        Args:
            data_type: Type of memory data
            query_pattern: How data will be queried
            update_frequency: How often data is updated
            data_structure: Structure of data (structured/unstructured)
        
        Returns:
            StorageDecision
        """
        # Vector DB for semantic search
        if query_pattern in ["semantic", "similarity", "meaning", "relevance"]:
            return StorageDecision(
                storage_type=StorageType.VECTOR_DB,
                reasoning="Semantic search requires vector similarity, best handled by Vector DB",
                alternative=StorageType.HYBRID if data_structure == "structured" else None
            )
        
        # PostgreSQL for exact queries
        if query_pattern in ["exact", "filter", "sql", "relational"]:
            return StorageDecision(
                storage_type=StorageType.POSTGRESQL,
                reasoning="Exact queries and filtering require SQL capabilities",
                alternative=StorageType.HYBRID if data_type == MemoryDataType.SEMANTIC_MEMORY else None
            )
        
        # Structured data → PostgreSQL
        if data_structure == "structured" or data_type == MemoryDataType.STRUCTURED_PROFILE:
            return StorageDecision(
                storage_type=StorageType.POSTGRESQL,
                reasoning="Structured data with relationships best stored in PostgreSQL",
                use_hybrid=True  # Can also store embeddings in Vector DB for search
            )
        
        # Unstructured insights → Vector DB
        if data_type == MemoryDataType.UNSTRUCTURED_INSIGHT or data_type == MemoryDataType.SEMANTIC_MEMORY:
            return StorageDecision(
                storage_type=StorageType.VECTOR_DB,
                reasoning="Unstructured semantic memories require vector search",
                use_hybrid=True  # Can store metadata in PostgreSQL
            )
        
        # Default: Hybrid for flexibility
        return StorageDecision(
            storage_type=StorageType.HYBRID,
            reasoning="Hybrid approach provides flexibility for both structured and semantic queries",
            use_hybrid=True
        )
    
    def should_use_hybrid(
        self,
        data_type: MemoryDataType,
        query_complexity: str = "medium"
    ) -> bool:
        """
        Determine if hybrid storage is recommended.
        
        Args:
            data_type: Type of memory data
            query_complexity: Complexity of queries
        
        Returns:
            True if hybrid storage recommended
        """
        # Always use hybrid for complex systems
        if query_complexity == "high":
            return True
        
        # Use hybrid when data has both structured and semantic aspects
        if data_type in [MemoryDataType.SEMANTIC_MEMORY, MemoryDataType.RELATIONAL_DATA]:
            return True
        
        return False


# ============================================================================
# Hybrid Storage Implementation
# ============================================================================

class HybridStorageManager:
    """
    Manager for hybrid storage (Vector DB + PostgreSQL).
    
    This demonstrates hybrid storage patterns:
    - Store structured data in PostgreSQL
    - Store embeddings in Vector DB
    - Cross-reference between systems
    - Unified retrieval interface
    """
    
    def __init__(self, vector_db_client: Any, postgres_client: Any):
        """
        Initialize hybrid storage manager.
        
        Args:
            vector_db_client: Vector DB client
            postgres_client: PostgreSQL client
        """
        self.vector_db = vector_db_client
        self.postgres = postgres_client
    
    def store_user_profile(
        self,
        user_id: str,
        profile_data: Dict[str, Any],
        semantic_memories: List[str]
    ) -> Dict[str, Any]:
        """
        Store user profile using hybrid storage.
        
        Args:
            user_id: User ID
            profile_data: Structured profile data
            semantic_memories: List of semantic memory texts
        
        Returns:
            Storage result with IDs
        """
        # Store structured profile in PostgreSQL
        profile_id = self.postgres.insert_user_profile(user_id, profile_data)
        
        # Store semantic memories in Vector DB
        memory_ids = []
        for memory_text in semantic_memories:
            # Generate embedding (in real implementation)
            embedding = self._generate_embedding(memory_text)
            
            # Store in Vector DB with reference to profile
            memory_id = self.vector_db.store_memory(
                user_id=user_id,
                content=memory_text,
                embedding=embedding,
                metadata={"profile_id": profile_id}
            )
            memory_ids.append(memory_id)
        
        # Update PostgreSQL with Vector DB references
        self.postgres.update_profile_vector_refs(profile_id, memory_ids)
        
        return {
            "profile_id": profile_id,
            "memory_ids": memory_ids,
            "storage_type": "hybrid"
        }
    
    def retrieve_user_context(
        self,
        user_id: str,
        query: str,
        include_profile: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieve user context using hybrid storage.
        
        Args:
            user_id: User ID
            query: Query for semantic search
            include_profile: Whether to include structured profile
        
        Returns:
            Combined context from both storages
        """
        context = {}
        
        # Get structured profile from PostgreSQL
        if include_profile:
            profile = self.postgres.get_user_profile(user_id)
            context["profile"] = profile
        
        # Get semantic memories from Vector DB
        query_embedding = self._generate_embedding(query)
        memories = self.vector_db.search_memories(
            user_id=user_id,
            query_embedding=query_embedding,
            top_k=10
        )
        context["memories"] = memories
        
        return context
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        # In real implementation, use embedding model
        # return embedding_model.encode(text).tolist()
        return []


# ============================================================================
# Storage Decision Examples
# ============================================================================

def decide_storage_for_memory(
    memory_content: str,
    memory_type: str,
    query_needs: str
) -> StorageDecision:
    """
    Example function for deciding storage for a memory.
    
    This demonstrates decision logic:
    - Analyze memory content and type
    - Consider query needs
    - Return storage decision
    
    Args:
        memory_content: Memory content
        memory_type: Type of memory
        query_needs: Query requirements
    
    Returns:
        StorageDecision
    """
    decider = StorageStrategyDecider()
    
    # Map memory type to MemoryDataType
    if memory_type == "user_preference" or memory_type == "setting":
        data_type = MemoryDataType.STRUCTURED_PROFILE
    elif memory_type == "insight" or memory_type == "fact":
        data_type = MemoryDataType.UNSTRUCTURED_INSIGHT
    else:
        data_type = MemoryDataType.SEMANTIC_MEMORY
    
    # Determine query pattern
    if "similar" in query_needs or "relevant" in query_needs:
        query_pattern = "semantic"
    elif "exact" in query_needs or "filter" in query_needs:
        query_pattern = "exact"
    else:
        query_pattern = "semantic"  # Default to semantic
    
    # Make decision
    decision = decider.decide_storage(
        data_type=data_type,
        query_pattern=query_pattern,
        data_structure="structured" if data_type == MemoryDataType.STRUCTURED_PROFILE else "unstructured"
    )
    
    return decision
