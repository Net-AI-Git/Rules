"""
Injection Detection Examples

This file demonstrates detection methods and patterns.
Reference this example from RULE.mdc using @examples_injection_detection.py syntax.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


# ============================================================================
# Detection Results
# ============================================================================

class InjectionType(Enum):
    """
    Types of injection attempts.
    
    This demonstrates injection classification:
    - Instruction override
    - System prompt injection
    - Delimiter injection
    - Encoding-based injection
    """
    INSTRUCTION_OVERRIDE = "instruction_override"
    SYSTEM_PROMPT = "system_prompt"
    DELIMITER_INJECTION = "delimiter_injection"
    ENCODED_INJECTION = "encoded_injection"
    UNKNOWN = "unknown"


@dataclass
class InjectionDetection:
    """
    Injection detection result.
    
    This demonstrates detection result:
    - Detection status
    - Injection type
    - Confidence score
    - Detected patterns
    """
    is_injection: bool
    injection_type: Optional[InjectionType]
    confidence: float  # 0.0-1.0
    detected_patterns: List[str]
    suspicious_segments: List[str]


# ============================================================================
# Pattern-Based Detection
# ============================================================================

class PatternBasedDetector:
    """
    Pattern-based injection detector.
    
    This demonstrates pattern detection:
    - Regex pattern matching
    - Keyword detection
    - Pattern scoring
    """
    
    def __init__(self):
        """Initialize pattern detector."""
        self.patterns = self._load_patterns()
    
    def detect(self, text: str) -> InjectionDetection:
        """
        Detect injection patterns.
        
        Args:
            text: Text to analyze
        
        Returns:
            InjectionDetection result
        """
        detected_patterns = []
        suspicious_segments = []
        confidence = 0.0
        
        # Check each pattern category
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    detected_patterns.append(pattern_type)
                    suspicious_segments.append(match.group(0))
                    confidence += 0.2  # Increase confidence per match
        
        # Normalize confidence
        confidence = min(1.0, confidence)
        
        # Determine injection type
        injection_type = self._classify_injection(detected_patterns)
        
        is_injection = confidence >= 0.5
        
        return InjectionDetection(
            is_injection=is_injection,
            injection_type=injection_type,
            confidence=confidence,
            detected_patterns=detected_patterns,
            suspicious_segments=suspicious_segments
        )
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """
        Load injection patterns.
        
        Returns:
            Dictionary of pattern categories and patterns
        """
        return {
            "instruction_override": [
                r"(?i)ignore\s+previous\s+instructions?",
                r"(?i)forget\s+everything\s+(above|before)",
                r"(?i)disregard\s+previous",
                r"(?i)override\s+previous",
            ],
            "system_prompt": [
                r"(?i)you\s+are\s+now\s+(a|an)\s+",
                r"(?i)system\s*:\s*",
                r"(?i)assistant\s*:\s*",
                r"(?i)act\s+as\s+if",
            ],
            "delimiter_injection": [
                r"###\s*instructions?\s*:",
                r"---\s*instructions?\s*:",
                r"<instructions?>",
                r"</?system>",
                r"```\s*instructions?",
            ],
            "encoded_injection": [
                r"[A-Za-z0-9+/]{50,}={0,2}",  # Base64-like
                r"%[0-9A-Fa-f]{2}",  # URL encoding
            ]
        }
    
    def _classify_injection(self, patterns: List[str]) -> Optional[InjectionType]:
        """
        Classify injection type from patterns.
        
        Args:
            patterns: Detected patterns
        
        Returns:
            InjectionType or None
        """
        if not patterns:
            return None
        
        # Count pattern types
        type_counts = {}
        for pattern in patterns:
            type_counts[pattern] = type_counts.get(pattern, 0) + 1
        
        # Determine most common type
        if "instruction_override" in type_counts:
            return InjectionType.INSTRUCTION_OVERRIDE
        elif "system_prompt" in type_counts:
            return InjectionType.SYSTEM_PROMPT
        elif "delimiter_injection" in type_counts:
            return InjectionType.DELIMITER_INJECTION
        elif "encoded_injection" in type_counts:
            return InjectionType.ENCODED_INJECTION
        
        return InjectionType.UNKNOWN


# ============================================================================
# Heuristic Detection
# ============================================================================

class HeuristicDetector:
    """
    Heuristic-based injection detector.
    
    This demonstrates heuristic detection:
    - Suspicious language patterns
    - Instruction-like language
    - Context analysis
    """
    
    def __init__(self):
        """Initialize heuristic detector."""
        self.instruction_keywords = [
            "ignore", "forget", "override", "disregard",
            "system", "assistant", "instructions", "prompt",
            "you are", "act as", "pretend", "simulate"
        ]
    
    def detect(self, text: str) -> InjectionDetection:
        """
        Detect injection using heuristics.
        
        Args:
            text: Text to analyze
        
        Returns:
            InjectionDetection result
        """
        text_lower = text.lower()
        suspicious_segments = []
        confidence = 0.0
        
        # Check for instruction keywords
        keyword_count = 0
        for keyword in self.instruction_keywords:
            if keyword in text_lower:
                keyword_count += 1
                # Find context around keyword
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                for match in pattern.finditer(text):
                    start = max(0, match.start() - 20)
                    end = min(len(text), match.end() + 20)
                    suspicious_segments.append(text[start:end])
        
        # Calculate confidence based on keyword density
        if keyword_count >= 3:
            confidence = 0.8
        elif keyword_count >= 2:
            confidence = 0.6
        elif keyword_count >= 1:
            confidence = 0.4
        
        # Check for imperative language
        imperative_patterns = [
            r"you\s+must\s+",
            r"you\s+should\s+",
            r"you\s+will\s+",
            r"do\s+not\s+",
        ]
        
        for pattern in imperative_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                confidence += 0.2
                break
        
        confidence = min(1.0, confidence)
        
        return InjectionDetection(
            is_injection=confidence >= 0.5,
            injection_type=InjectionType.UNKNOWN,
            confidence=confidence,
            detected_patterns=["heuristic_analysis"],
            suspicious_segments=suspicious_segments
        )


# ============================================================================
# Combined Detection
# ============================================================================

class InjectionDetector:
    """
    Combined injection detector.
    
    This demonstrates combined detection:
    - Pattern-based detection
    - Heuristic analysis
    - ML-based detection (if available)
    - Combined scoring
    """
    
    def __init__(self):
        """Initialize combined detector."""
        self.pattern_detector = PatternBasedDetector()
        self.heuristic_detector = HeuristicDetector()
    
    def detect(self, text: str) -> InjectionDetection:
        """
        Detect injection using all methods.
        
        Args:
            text: Text to analyze
        
        Returns:
            Combined InjectionDetection result
        """
        # Run pattern detection
        pattern_result = self.pattern_detector.detect(text)
        
        # Run heuristic detection
        heuristic_result = self.heuristic_detector.detect(text)
        
        # Combine results
        combined_confidence = max(
            pattern_result.confidence,
            heuristic_result.confidence
        )
        
        # If both detect, increase confidence
        if pattern_result.is_injection and heuristic_result.is_injection:
            combined_confidence = min(1.0, combined_confidence + 0.2)
        
        # Combine detected patterns
        all_patterns = list(set(
            pattern_result.detected_patterns +
            heuristic_result.detected_patterns
        ))
        
        # Combine suspicious segments
        all_segments = list(set(
            pattern_result.suspicious_segments +
            heuristic_result.suspicious_segments
        ))
        
        # Use pattern type if available, otherwise heuristic
        injection_type = pattern_result.injection_type or heuristic_result.injection_type
        
        return InjectionDetection(
            is_injection=combined_confidence >= 0.5,
            injection_type=injection_type,
            confidence=combined_confidence,
            detected_patterns=all_patterns,
            suspicious_segments=all_segments
        )
    
    def should_block(self, text: str, threshold: float = 0.7) -> Tuple[bool, InjectionDetection]:
        """
        Determine if input should be blocked.
        
        Args:
            text: Text to check
            threshold: Confidence threshold for blocking
        
        Returns:
            Tuple of (should_block, detection_result)
        """
        detection = self.detect(text)
        should_block = detection.is_injection and detection.confidence >= threshold
        
        return should_block, detection
