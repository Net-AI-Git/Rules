"""
Input Sanitization Examples

This file demonstrates sanitization patterns and implementation.
Reference this example from RULE.mdc using @examples_input_sanitization.py syntax.
"""

from typing import List, Dict, Any, Optional
import re
import html
import json


# ============================================================================
# Sanitization Techniques
# ============================================================================

class InputSanitizer:
    """
    Service for sanitizing user input.
    
    This demonstrates sanitization patterns:
    - Escaping special characters
    - Filtering injection patterns
    - Encoding user input
    - Validation
    """
    
    def __init__(self):
        """Initialize sanitizer."""
        self.injection_patterns = self._load_injection_patterns()
    
    def sanitize(self, user_input: str, sanitization_level: str = "standard") -> str:
        """
        Sanitize user input.
        
        Args:
            user_input: User input to sanitize
            sanitization_level: Level of sanitization (basic, standard, strict)
        
        Returns:
            Sanitized input
        """
        if sanitization_level == "basic":
            return self._basic_sanitize(user_input)
        elif sanitization_level == "standard":
            return self._standard_sanitize(user_input)
        else:  # strict
            return self._strict_sanitize(user_input)
    
    def _basic_sanitize(self, user_input: str) -> str:
        """
        Basic sanitization (escaping only).
        
        Args:
            user_input: Input to sanitize
        
        Returns:
            Sanitized input
        """
        # Escape XML/HTML characters
        sanitized = html.escape(user_input)
        
        # Escape prompt delimiters
        sanitized = sanitized.replace("###", "\\#\\#\\#")
        sanitized = sanitized.replace("---", "\\-\\-\\-")
        
        return sanitized
    
    def _standard_sanitize(self, user_input: str) -> str:
        """
        Standard sanitization (escaping + filtering).
        
        Args:
            user_input: Input to sanitize
        
        Returns:
            Sanitized input
        """
        # Apply basic sanitization
        sanitized = self._basic_sanitize(user_input)
        
        # Filter injection patterns
        sanitized = self._filter_injection_patterns(sanitized)
        
        # Normalize whitespace
        sanitized = self._normalize_whitespace(sanitized)
        
        return sanitized
    
    def _strict_sanitize(self, user_input: str) -> str:
        """
        Strict sanitization (all techniques).
        
        Args:
            user_input: Input to sanitize
        
        Returns:
            Sanitized input
        """
        # Apply standard sanitization
        sanitized = self._standard_sanitize(user_input)
        
        # Remove control characters
        sanitized = self._remove_control_characters(sanitized)
        
        # Additional filtering
        sanitized = self._aggressive_filtering(sanitized)
        
        return sanitized
    
    def _filter_injection_patterns(self, text: str) -> str:
        """
        Filter known injection patterns.
        
        Args:
            text: Text to filter
        
        Returns:
            Filtered text
        """
        filtered = text
        
        # Filter common injection phrases
        injection_phrases = [
            r"(?i)ignore\s+previous\s+instructions",
            r"(?i)forget\s+everything\s+above",
            r"(?i)you\s+are\s+now",
            r"(?i)system\s*:",
            r"(?i)begin\s+new\s+prompt",
            r"(?i)###\s*instructions?\s*:",
        ]
        
        for pattern in injection_phrases:
            filtered = re.sub(pattern, "[FILTERED]", filtered)
        
        return filtered
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace.
        
        Args:
            text: Text to normalize
        
        Returns:
            Normalized text
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Normalize newlines
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # Limit consecutive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _remove_control_characters(self, text: str) -> str:
        """
        Remove control characters.
        
        Args:
            text: Text to clean
        
        Returns:
            Cleaned text
        """
        # Remove control characters except newline and tab
        cleaned = ''.join(
            char for char in text
            if ord(char) >= 32 or char in ['\n', '\t']
        )
        
        return cleaned
    
    def _aggressive_filtering(self, text: str) -> str:
        """
        Aggressive filtering for strict mode.
        
        Args:
            text: Text to filter
        
        Returns:
            Filtered text
        """
        # Remove XML/HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '[CODE_BLOCK_REMOVED]', text)
        
        # Remove markdown headers
        text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
        
        return text
    
    def _load_injection_patterns(self) -> List[str]:
        """
        Load injection patterns.
        
        Returns:
            List of injection patterns
        """
        return [
            r"(?i)ignore\s+previous",
            r"(?i)forget\s+everything",
            r"(?i)you\s+are\s+now",
            r"(?i)system\s*:",
            r"(?i)instructions?\s*:",
            r"(?i)begin\s+new",
            r"(?i)override",
            r"(?i)bypass",
        ]


# ============================================================================
# Escaping Strategies
# ============================================================================

class PromptEscaper:
    """
    Service for escaping user input in prompts.
    
    This demonstrates escaping patterns:
    - XML/HTML escaping
    - Prompt delimiter escaping
    - Control character handling
    """
    
    @staticmethod
    def escape_xml(text: str) -> str:
        """
        Escape XML/HTML characters.
        
        Args:
            text: Text to escape
        
        Returns:
            Escaped text
        """
        return html.escape(text)
    
    @staticmethod
    def escape_prompt_delimiters(text: str) -> str:
        """
        Escape prompt delimiters.
        
        Args:
            text: Text to escape
        
        Returns:
            Escaped text
        """
        # Escape common delimiters
        text = text.replace("###", "\\#\\#\\#")
        text = text.replace("---", "\\-\\-\\-")
        text = text.replace("===", "\\=\\=\\=")
        
        # Escape XML tags
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        
        return text
    
    @staticmethod
    def escape_control_characters(text: str) -> str:
        """
        Escape control characters.
        
        Args:
            text: Text to escape
        
        Returns:
            Escaped text
        """
        # Replace control characters with escape sequences
        control_char_map = {
            '\x00': '\\0',
            '\x01': '\\x01',
            '\x02': '\\x02',
            # ... more control characters
        }
        
        for char, replacement in control_char_map.items():
            text = text.replace(char, replacement)
        
        return text


# ============================================================================
# Encoding Strategies
# ============================================================================

class InputEncoder:
    """
    Service for encoding user input.
    
    This demonstrates encoding patterns:
    - Safe encoding for prompt insertion
    - Base64 encoding detection
    - Unicode normalization
    """
    
    @staticmethod
    def encode_for_prompt(text: str) -> str:
        """
        Encode text for safe prompt insertion.
        
        Args:
            text: Text to encode
        
        Returns:
            Encoded text
        """
        # JSON encode for safe insertion
        return json.dumps(text)
    
    @staticmethod
    def detect_encoded_content(text: str) -> bool:
        """
        Detect if text contains encoded content.
        
        Args:
            text: Text to check
        
        Returns:
            True if encoded content detected
        """
        # Check for base64 patterns
        base64_pattern = r'^[A-Za-z0-9+/]{20,}={0,2}$'
        if re.match(base64_pattern, text.strip()):
            return True
        
        # Check for URL encoding
        if '%' in text and re.search(r'%[0-9A-Fa-f]{2}', text):
            return True
        
        return False
    
    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize Unicode characters.
        
        Args:
            text: Text to normalize
        
        Returns:
            Normalized text
        """
        import unicodedata
        # Normalize to NFC form
        normalized = unicodedata.normalize('NFC', text)
        return normalized


# ============================================================================
# Sanitization Pipeline
# ============================================================================

class SanitizationPipeline:
    """
    Pipeline for comprehensive input sanitization.
    
    This demonstrates sanitization pipeline:
    - Multiple sanitization steps
    - Configurable pipeline
    - Error handling
    """
    
    def __init__(self):
        """Initialize sanitization pipeline."""
        self.sanitizer = InputSanitizer()
        self.escaper = PromptEscaper()
        self.encoder = InputEncoder()
    
    def sanitize_input(
        self,
        user_input: str,
        level: str = "standard"
    ) -> Dict[str, Any]:
        """
        Run full sanitization pipeline.
        
        Args:
            user_input: User input
            level: Sanitization level
        
        Returns:
            Dictionary with sanitized input and metadata
        """
        original = user_input
        
        # Step 1: Detect encoded content
        is_encoded = self.encoder.detect_encoded_content(user_input)
        if is_encoded:
            # Log suspicious content
            pass
        
        # Step 2: Normalize Unicode
        normalized = self.encoder.normalize_unicode(user_input)
        
        # Step 3: Sanitize
        sanitized = self.sanitizer.sanitize(normalized, level)
        
        # Step 4: Escape
        escaped = self.escaper.escape_prompt_delimiters(sanitized)
        
        # Step 5: Final validation
        final = self._final_validation(escaped)
        
        return {
            "original": original,
            "sanitized": final,
            "was_modified": original != final,
            "modifications": self._get_modifications(original, final),
            "is_encoded": is_encoded
        }
    
    def _final_validation(self, text: str) -> str:
        """
        Final validation step.
        
        Args:
            text: Text to validate
        
        Returns:
            Validated text
        """
        # Check length
        if len(text) > 10000:  # Max length
            text = text[:10000] + "...[TRUNCATED]"
        
        # Final pattern check
        text = self.sanitizer._filter_injection_patterns(text)
        
        return text
    
    def _get_modifications(self, original: str, sanitized: str) -> List[str]:
        """
        Get list of modifications made.
        
        Args:
            original: Original text
            sanitized: Sanitized text
        
        Returns:
            List of modification descriptions
        """
        modifications = []
        
        if original != sanitized:
            modifications.append("Input was sanitized")
        
        if len(original) != len(sanitized):
            modifications.append(f"Length changed: {len(original)} -> {len(sanitized)}")
        
        return modifications
