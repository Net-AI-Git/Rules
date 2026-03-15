"""
Context Compression Examples

This file demonstrates summarization implementations and trimming logic.
Reference this example from RULE.mdc using @examples_compression.py syntax.
"""

from typing import List, Dict, Any, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


# ============================================================================
# Compression Types
# ============================================================================

class CompressionType(Enum):
    """
    Types of context compression.
    
    This demonstrates compression strategies:
    - Extractive: Extract key sentences
    - Abstractive: Generate new summary
    - Hierarchical: Multi-level summaries
    """
    EXTRACTIVE = "extractive"
    ABSTRACTIVE = "abstractive"
    HIERARCHICAL = "hierarchical"


@dataclass
class Message:
    """
    Conversation message structure.
    
    This demonstrates message format:
    - Role (user/assistant/system)
    - Content
    - Metadata (timestamp, tokens, importance)
    """
    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: datetime
    token_count: int = 0
    importance_score: float = 0.5
    metadata: Dict[str, Any] = None


@dataclass
class CompressionConfig:
    """
    Configuration for context compression.
    
    This demonstrates compression configuration:
    - Target token count
    - Compression type
    - Retention criteria
    - Quality thresholds
    """
    target_tokens: int
    compression_type: CompressionType
    preserve_recent_messages: int = 5  # Keep last N messages
    min_importance_score: float = 0.3
    max_summary_length: int = 500


# ============================================================================
# Token Counting
# ============================================================================

class TokenCounter:
    """
    Token counting utility.
    
    This demonstrates token counting:
    - Model-specific tokenizers
    - Accurate token estimation
    - Batch counting
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        """
        Initialize token counter.
        
        Args:
            model_name: Name of the model
        """
        self.model_name = model_name
        # In real implementation, load appropriate tokenizer
        # e.g., tiktoken for OpenAI models
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count
            
        Returns:
            Number of tokens
        """
        # In real implementation:
        # if "gpt" in self.model_name.lower():
        #     import tiktoken
        #     encoding = tiktoken.encoding_for_model(self.model_name)
        #     return len(encoding.encode(text))
        # else:
        #     # Use model-specific tokenizer
        
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
    
    def count_messages(self, messages: List[Message]) -> int:
        """
        Count total tokens in messages.
        
        Args:
            messages: List of messages
            
        Returns:
            Total token count
        """
        return sum(msg.token_count for msg in messages)


# ============================================================================
# Compression Triggers
# ============================================================================

class CompressionTrigger:
    """
    Service for detecting when compression is needed.
    
    This demonstrates compression trigger patterns:
    - Token threshold detection
    - Automatic vs manual triggers
    - Model-specific limits
    """
    
    def __init__(
        self,
        token_counter: TokenCounter,
        warning_threshold: float = 0.8,
        compression_threshold: float = 0.85,
        critical_threshold: float = 0.95
    ):
        """
        Initialize compression trigger.
        
        Args:
            token_counter: Token counter instance
            warning_threshold: Warning threshold (0.0-1.0)
            compression_threshold: Compression threshold (0.0-1.0)
            critical_threshold: Critical threshold (0.0-1.0)
        """
        self.token_counter = token_counter
        self.warning_threshold = warning_threshold
        self.compression_threshold = compression_threshold
        self.critical_threshold = critical_threshold
    
    def check_compression_needed(
        self,
        messages: List[Message],
        model_context_limit: int
    ) -> Dict[str, Any]:
        """
        Check if compression is needed.
        
        Args:
            messages: List of messages
            model_context_limit: Model's context limit
            
        Returns:
            Dictionary with compression status
        """
        total_tokens = self.token_counter.count_messages(messages)
        usage_ratio = total_tokens / model_context_limit if model_context_limit > 0 else 0
        
        status = {
            "total_tokens": total_tokens,
            "context_limit": model_context_limit,
            "usage_ratio": usage_ratio,
            "needs_compression": False,
            "compression_urgency": "none"
        }
        
        if usage_ratio >= self.critical_threshold:
            status["needs_compression"] = True
            status["compression_urgency"] = "critical"
        elif usage_ratio >= self.compression_threshold:
            status["needs_compression"] = True
            status["compression_urgency"] = "high"
        elif usage_ratio >= self.warning_threshold:
            status["compression_urgency"] = "warning"
        
        return status


# ============================================================================
# Extractive Summarization
# ============================================================================

class ExtractiveSummarizer:
    """
    Extractive summarization implementation.
    
    This demonstrates extractive summarization:
    - Extract key sentences without modification
    - Preserve exact wording
    - Fast, no LLM call needed
    """
    
    def summarize(
        self,
        messages: List[Message],
        target_tokens: int,
        preserve_recent: int = 5
    ) -> List[Message]:
        """
        Summarize messages using extractive method.
        
        Args:
            messages: List of messages to summarize
            target_tokens: Target token count
            preserve_recent: Number of recent messages to preserve
            
        Returns:
            Compressed list of messages
        """
        # Preserve recent messages
        recent_messages = messages[-preserve_recent:] if len(messages) > preserve_recent else messages
        old_messages = messages[:-preserve_recent] if len(messages) > preserve_recent else []
        
        if not old_messages:
            return messages
        
        # Extract important sentences from old messages
        compressed_old = []
        current_tokens = sum(msg.token_count for msg in recent_messages)
        
        for message in reversed(old_messages):
            # Extract key sentences (simplified - in real implementation, use NLP)
            key_sentences = self._extract_key_sentences(message.content)
            
            # Create compressed message
            compressed_content = " ".join(key_sentences)
            compressed_tokens = len(compressed_content) // 4  # Rough estimate
            
            if current_tokens + compressed_tokens <= target_tokens:
                compressed_message = Message(
                    role=message.role,
                    content=f"[Compressed] {compressed_content}",
                    timestamp=message.timestamp,
                    token_count=compressed_tokens,
                    importance_score=message.importance_score,
                    metadata={**message.metadata or {}, "compressed": True, "original_tokens": message.token_count}
                )
                compressed_old.insert(0, compressed_message)
                current_tokens += compressed_tokens
            else:
                break
        
        return compressed_old + recent_messages
    
    def _extract_key_sentences(self, text: str) -> List[str]:
        """
        Extract key sentences from text.
        
        Args:
            text: Text to extract from
            
        Returns:
            List of key sentences
        """
        # In real implementation, use NLP techniques:
        # - Sentence tokenization
        # - Importance scoring (TF-IDF, position, length)
        # - Select top sentences
        
        # Simple implementation: split by sentences and take first/last
        sentences = text.split(". ")
        if len(sentences) <= 3:
            return sentences
        # Take first, middle, and last sentences
        return [sentences[0], sentences[len(sentences)//2], sentences[-1]]


# ============================================================================
# Abstractive Summarization
# ============================================================================

class AbstractiveSummarizer:
    """
    Abstractive summarization implementation.
    
    This demonstrates abstractive summarization:
    - Generate new summary text
    - Use LLM for summarization
    - Preserve meaning, not exact wording
    """
    
    def __init__(self, llm_client: Any = None):
        """
        Initialize abstractive summarizer.
        
        Args:
            llm_client: LLM client for summarization
        """
        self.llm_client = llm_client
    
    def summarize(
        self,
        messages: List[Message],
        target_tokens: int,
        preserve_recent: int = 5
    ) -> List[Message]:
        """
        Summarize messages using abstractive method.
        
        Args:
            messages: List of messages to summarize
            target_tokens: Target token count
            preserve_recent: Number of recent messages to preserve
            
        Returns:
            Compressed list of messages
        """
        # Preserve recent messages
        recent_messages = messages[-preserve_recent:] if len(messages) > preserve_recent else messages
        old_messages = messages[:-preserve_recent] if len(messages) > preserve_recent else []
        
        if not old_messages:
            return messages
        
        # Generate summary of old messages
        old_content = "\n".join([f"{msg.role}: {msg.content}" for msg in old_messages])
        
        # In real implementation, use LLM to generate summary:
        # summary = self.llm_client.generate(
        #     prompt=f"Summarize the following conversation history, preserving key decisions, user preferences, and important context:\n\n{old_content}",
        #     max_tokens=target_tokens - sum(msg.token_count for msg in recent_messages)
        # )
        
        # For example, create a summary message
        summary_content = f"[Summary of {len(old_messages)} previous messages] Key points and decisions from earlier conversation."
        summary_tokens = len(summary_content) // 4
        
        summary_message = Message(
            role="system",
            content=summary_content,
            timestamp=old_messages[0].timestamp,
            token_count=summary_tokens,
            importance_score=0.7,
            metadata={"compressed": True, "original_count": len(old_messages), "method": "abstractive"}
        )
        
        return [summary_message] + recent_messages


# ============================================================================
# Compression Service
# ============================================================================

class ContextCompressionService:
    """
    Service for compressing conversation context.
    
    This demonstrates compression service pattern:
    - Detect compression needs
    - Apply appropriate compression strategy
    - Validate results
    """
    
    def __init__(
        self,
        token_counter: TokenCounter,
        compression_type: CompressionType = CompressionType.ABSTRACTIVE
    ):
        """
        Initialize compression service.
        
        Args:
            token_counter: Token counter instance
            compression_type: Default compression type
        """
        self.token_counter = token_counter
        self.compression_type = compression_type
        self.extractive_summarizer = ExtractiveSummarizer()
        self.abstractive_summarizer = AbstractiveSummarizer()
    
    def compress_context(
        self,
        messages: List[Message],
        model_context_limit: int,
        config: Optional[CompressionConfig] = None
    ) -> List[Message]:
        """
        Compress conversation context.
        
        Args:
            messages: List of messages
            model_context_limit: Model's context limit
            config: Compression configuration
            
        Returns:
            Compressed list of messages
        """
        # Check if compression needed
        trigger = CompressionTrigger(self.token_counter)
        status = trigger.check_compression_needed(messages, model_context_limit)
        
        if not status["needs_compression"]:
            return messages
        
        # Determine target tokens
        target_tokens = int(model_context_limit * 0.75)  # Target 75% of limit
        if config:
            target_tokens = config.target_tokens
        
        # Choose compression type
        compression_type = config.compression_type if config else self.compression_type
        
        # Apply compression
        if compression_type == CompressionType.EXTRACTIVE:
            compressed = self.extractive_summarizer.summarize(
                messages,
                target_tokens,
                preserve_recent=config.preserve_recent_messages if config else 5
            )
        elif compression_type == CompressionType.ABSTRACTIVE:
            compressed = self.abstractive_summarizer.summarize(
                messages,
                target_tokens,
                preserve_recent=config.preserve_recent_messages if config else 5
            )
        else:
            # Hierarchical - combine both methods
            compressed = self._hierarchical_compress(messages, target_tokens, config)
        
        # Validate compression
        final_tokens = self.token_counter.count_messages(compressed)
        if final_tokens > model_context_limit * 0.9:
            # Still too large, apply more aggressive compression
            compressed = self._aggressive_compress(compressed, model_context_limit)
        
        return compressed
    
    def _hierarchical_compress(
        self,
        messages: List[Message],
        target_tokens: int,
        config: Optional[CompressionConfig]
    ) -> List[Message]:
        """Apply hierarchical compression (combines extractive and abstractive)."""
        # In real implementation:
        # 1. Use abstractive for very old messages
        # 2. Use extractive for moderately old messages
        # 3. Keep recent messages intact
        
        preserve_recent = config.preserve_recent_messages if config else 5
        recent = messages[-preserve_recent:]
        old = messages[:-preserve_recent] if len(messages) > preserve_recent else []
        
        if not old:
            return messages
        
        # Abstractive summary for old messages
        compressed_old = self.abstractive_summarizer.summarize(old, target_tokens // 2, preserve_recent=0)
        
        return compressed_old + recent
    
    def _aggressive_compress(
        self,
        messages: List[Message],
        model_context_limit: int
    ) -> List[Message]:
        """Apply aggressive compression (FIFO trimming)."""
        # Keep only most recent messages that fit
        compressed = []
        current_tokens = 0
        
        for message in reversed(messages):
            if current_tokens + message.token_count <= model_context_limit * 0.8:
                compressed.insert(0, message)
                current_tokens += message.token_count
            else:
                break
        
        return compressed
