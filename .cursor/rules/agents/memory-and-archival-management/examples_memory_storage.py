"""
Memory Storage Examples

This file demonstrates Vector DB integration and user profile storage patterns.
Reference this example from RULE.mdc using @examples_memory_storage.py syntax.
"""

from typing import List, Dict, Any, Optional, TypedDict
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# Memory Types and Schemas
# ============================================================================

class MemoryType(Enum):
    """
    Types of long-term memories.
    
    This demonstrates memory categorization:
    - User profile information
    - Contextual insights
    - Behavioral patterns
    """
    USER_PROFILE = "user_profile"
    CONTEXTUAL_INSIGHT = "contextual_insight"
    BEHAVIORAL_PATTERN = "behavioral_pattern"


@dataclass
class UserMemory:
    """
    Structure for storing user memories in Vector DB.
    
    This demonstrates memory storage format:
    - Structured data for user profiles
    - Embeddings for semantic search
    - Metadata for filtering and versioning
    """
    memory_id: str
    user_id: str
    tenant_id: Optional[str]
    memory_type: MemoryType
    content: str  # The actual memory content
    embedding: Optional[List[float]]  # Vector embedding for semantic search
    metadata: Dict[str, Any]  # Additional metadata
    created_at: datetime
    updated_at: datetime
    confidence_score: float  # 0.0-1.0, how confident we are in this memory
    source: str  # Which conversation/agent created this memory
    version: int  # Version number for tracking changes


@dataclass
class UserProfile:
    """
    User profile structure aggregating user memories.
    
    This demonstrates user profile structure:
    - Preferences and settings
    - Domain expertise
    - Communication style
    - Historical patterns
    """
    user_id: str
    tenant_id: Optional[str]
    preferences: Dict[str, Any]
    expertise_domains: List[str]
    communication_style: Dict[str, Any]
    interaction_patterns: Dict[str, Any]
    last_updated: datetime
    memory_count: int


# ============================================================================
# Vector DB Interface
# ============================================================================

class VectorDBInterface:
    """
    Interface for Vector DB operations.
    
    This demonstrates Vector DB integration pattern:
    - Store embeddings and metadata
    - Semantic search capabilities
    - Multi-tenant isolation
    - Versioning support
    """
    
    def __init__(self, connection_string: str, tenant_id: Optional[str] = None):
        """
        Initialize Vector DB connection.
        
        Args:
            connection_string: Connection string for Vector DB
            tenant_id: Optional tenant ID for isolation
        """
        self.connection_string = connection_string
        self.tenant_id = tenant_id
        # In real implementation, initialize actual Vector DB client
        # e.g., Pinecone, Weaviate, Qdrant, ChromaDB
    
    def store_memory(self, memory: UserMemory) -> str:
        """
        Store a user memory in Vector DB.
        
        Args:
            memory: UserMemory to store
            
        Returns:
            Memory ID
        """
        # In real implementation:
        # 1. Generate embedding if not provided
        # 2. Store in Vector DB with metadata
        # 3. Return memory ID
        
        # Example structure for Pinecone:
        # vector = memory.embedding or self._generate_embedding(memory.content)
        # metadata = {
        #     "user_id": memory.user_id,
        #     "tenant_id": memory.tenant_id,
        #     "memory_type": memory.memory_type.value,
        #     "content": memory.content,
        #     "created_at": memory.created_at.isoformat(),
        #     "confidence_score": memory.confidence_score,
        #     "source": memory.source,
        #     "version": memory.version
        # }
        # index.upsert(vectors=[(memory.memory_id, vector, metadata)])
        
        return memory.memory_id
    
    def search_memories(
        self,
        user_id: str,
        query_embedding: List[float],
        top_k: int = 10,
        memory_type: Optional[MemoryType] = None,
        min_confidence: float = 0.5,
        tenant_id: Optional[str] = None
    ) -> List[UserMemory]:
        """
        Search memories using semantic similarity.
        
        Args:
            user_id: User ID to search memories for
            query_embedding: Query vector embedding
            top_k: Number of results to return
            memory_type: Optional filter by memory type
            min_confidence: Minimum confidence score
            tenant_id: Optional tenant ID for isolation
            
        Returns:
            List of relevant UserMemory objects
        """
        # In real implementation:
        # 1. Build filter for user_id, tenant_id, memory_type
        # 2. Perform vector similarity search
        # 3. Filter by confidence score
        # 4. Return top_k results
        
        # Example structure for Pinecone:
        # filter_dict = {"user_id": user_id}
        # if tenant_id:
        #     filter_dict["tenant_id"] = tenant_id
        # if memory_type:
        #     filter_dict["memory_type"] = memory_type.value
        # 
        # results = index.query(
        #     vector=query_embedding,
        #     top_k=top_k,
        #     filter=filter_dict,
        #     include_metadata=True
        # )
        # 
        # memories = []
        # for result in results.matches:
        #     if result.metadata.get("confidence_score", 0) >= min_confidence:
        #         memory = self._result_to_memory(result)
        #         memories.append(memory)
        # 
        # return memories
        
        return []
    
    def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of memory to update
            updates: Dictionary of fields to update
            
        Returns:
            True if update successful
        """
        # In real implementation:
        # 1. Fetch existing memory
        # 2. Apply updates
        # 3. Increment version
        # 4. Update in Vector DB
        
        return True
    
    def delete_memory(self, memory_id: str, user_id: str) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of memory to delete
            user_id: User ID for authorization
            
        Returns:
            True if deletion successful
        """
        # In real implementation:
        # 1. Verify user_id matches memory owner
        # 2. Delete from Vector DB
        # 3. Log deletion for audit
        
        return True
    
    def get_user_profile(self, user_id: str, tenant_id: Optional[str] = None) -> Optional[UserProfile]:
        """
        Get aggregated user profile.
        
        Args:
            user_id: User ID
            tenant_id: Optional tenant ID
            
        Returns:
            UserProfile or None if not found
        """
        # In real implementation:
        # 1. Retrieve all memories for user
        # 2. Aggregate into profile structure
        # 3. Return UserProfile
        
        return None


# ============================================================================
# Memory Storage Service
# ============================================================================

class MemoryStorageService:
    """
    Service for managing long-term memory storage.
    
    This demonstrates memory storage service pattern:
    - Store user memories
    - Retrieve relevant memories
    - Update and delete memories
    - Manage user profiles
    """
    
    def __init__(self, vector_db: VectorDBInterface, embedding_model: Any = None):
        """
        Initialize memory storage service.
        
        Args:
            vector_db: Vector DB interface
            embedding_model: Model for generating embeddings
        """
        self.vector_db = vector_db
        self.embedding_model = embedding_model
    
    def store_user_memory(
        self,
        user_id: str,
        content: str,
        memory_type: MemoryType,
        metadata: Dict[str, Any],
        confidence_score: float = 1.0,
        source: str = "agent",
        tenant_id: Optional[str] = None
    ) -> str:
        """
        Store a new user memory.
        
        Args:
            user_id: User ID
            content: Memory content
            memory_type: Type of memory
            metadata: Additional metadata
            confidence_score: Confidence in this memory
            source: Source of memory
            tenant_id: Optional tenant ID
            
        Returns:
            Memory ID
        """
        # Generate embedding
        embedding = self._generate_embedding(content) if self.embedding_model else None
        
        # Create memory object
        memory = UserMemory(
            memory_id=f"{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            tenant_id=tenant_id,
            memory_type=memory_type,
            content=content,
            embedding=embedding,
            metadata=metadata,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            confidence_score=confidence_score,
            source=source,
            version=1
        )
        
        # Store in Vector DB
        memory_id = self.vector_db.store_memory(memory)
        
        return memory_id
    
    def retrieve_relevant_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 10,
        memory_type: Optional[MemoryType] = None,
        min_confidence: float = 0.5,
        tenant_id: Optional[str] = None
    ) -> List[UserMemory]:
        """
        Retrieve relevant memories for a query.
        
        Args:
            user_id: User ID
            query: Query text
            top_k: Number of results
            memory_type: Optional filter by type
            min_confidence: Minimum confidence score
            tenant_id: Optional tenant ID
            
        Returns:
            List of relevant memories
        """
        # Generate query embedding
        query_embedding = self._generate_embedding(query) if self.embedding_model else []
        
        # Search Vector DB
        memories = self.vector_db.search_memories(
            user_id=user_id,
            query_embedding=query_embedding,
            top_k=top_k,
            memory_type=memory_type,
            min_confidence=min_confidence,
            tenant_id=tenant_id
        )
        
        return memories
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # In real implementation, use embedding model:
        # return self.embedding_model.encode(text).tolist()
        return []
