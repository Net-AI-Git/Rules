"""
Validation Patterns Examples

This file demonstrates input validation patterns and rules.
Reference this example from RULE.mdc using @examples_validation_patterns.py syntax.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import re
from pydantic import BaseModel, validator, Field


# ============================================================================
# Validation Rules
# ============================================================================

class ValidationLevel(Enum):
    """
    Validation levels.
    
    This demonstrates validation strictness:
    - Basic: Format and length only
    - Standard: Format, length, and content checks
    - Strict: All checks plus security validation
    """
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class ValidationResult:
    """
    Validation result structure.
    
    This demonstrates validation result:
    - Pass/fail status
    - Validation errors
    - Warnings
    """
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_value: Optional[str] = None


# ============================================================================
# Schema Validation
# ============================================================================

class UserInputSchema(BaseModel):
    """
    Pydantic schema for user input validation.
    
    This demonstrates schema validation:
    - Type checking
    - Format validation
    - Length limits
    - Pattern matching
    """
    user_message: str = Field(..., min_length=1, max_length=10000)
    context: Optional[str] = Field(None, max_length=5000)
    user_id: str = Field(..., pattern=r'^[a-zA-Z0-9_-]+$')
    
    @validator('user_message')
    def validate_message(cls, v):
        """Validate user message."""
        # Check for injection patterns
        injection_patterns = [
            r"(?i)ignore\s+previous",
            r"(?i)system\s*:",
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, v):
                raise ValueError(f"Input contains suspicious pattern: {pattern}")
        
        return v
    
    @validator('context')
    def validate_context(cls, v):
        """Validate context if provided."""
        if v and len(v) > 5000:
            raise ValueError("Context exceeds maximum length")
        return v


# ============================================================================
# Format Validation
# ============================================================================

class FormatValidator:
    """
    Service for format validation.
    
    This demonstrates format validation:
    - Text format validation
    - JSON validation
    - Encoding validation
    - Structure validation
    """
    
    @staticmethod
    def validate_text_format(text: str) -> ValidationResult:
        """
        Validate text format.
        
        Args:
            text: Text to validate
        
        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        
        # Check encoding
        try:
            text.encode('utf-8')
        except UnicodeEncodeError:
            errors.append("Text contains invalid UTF-8 characters")
        
        # Check length
        if len(text) == 0:
            errors.append("Text cannot be empty")
        elif len(text) > 10000:
            errors.append(f"Text exceeds maximum length: {len(text)} > 10000")
            warnings.append("Text will be truncated")
        
        # Check for null bytes
        if '\x00' in text:
            errors.append("Text contains null bytes")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    @staticmethod
    def validate_json_format(text: str) -> ValidationResult:
        """
        Validate JSON format.
        
        Args:
            text: JSON text to validate
        
        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        
        try:
            import json
            data = json.loads(text)
            
            # Check structure
            if not isinstance(data, (dict, list)):
                warnings.append("JSON is not an object or array")
            
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {str(e)}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


# ============================================================================
# Content Validation
# ============================================================================

class ContentValidator:
    """
    Service for content validation.
    
    This demonstrates content validation:
    - Content type validation
    - Business rule validation
    - Security validation
    """
    
    def __init__(self):
        """Initialize content validator."""
        self.injection_detector = None  # Would be InjectionDetector instance
    
    def validate_content(
        self,
        text: str,
        validation_level: ValidationLevel = ValidationLevel.STANDARD
    ) -> ValidationResult:
        """
        Validate content.
        
        Args:
            text: Text to validate
            validation_level: Validation level
        
        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        
        # Format validation
        format_result = FormatValidator.validate_text_format(text)
        errors.extend(format_result.errors)
        warnings.extend(format_result.warnings)
        
        # Content validation
        if validation_level in [ValidationLevel.STANDARD, ValidationLevel.STRICT]:
            content_errors = self._validate_content_rules(text)
            errors.extend(content_errors)
        
        # Security validation
        if validation_level == ValidationLevel.STRICT:
            security_errors = self._validate_security(text)
            errors.extend(security_errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_content_rules(self, text: str) -> List[str]:
        """
        Validate content against business rules.
        
        Args:
            text: Text to validate
        
        Returns:
            List of error messages
        """
        errors = []
        
        # Check for required content
        if len(text.strip()) == 0:
            errors.append("Content cannot be empty")
        
        # Check for reasonable content (not just whitespace)
        if not text.strip():
            errors.append("Content cannot be only whitespace")
        
        return errors
    
    def _validate_security(self, text: str) -> List[str]:
        """
        Validate security aspects.
        
        Args:
            text: Text to validate
        
        Returns:
            List of error messages
        """
        errors = []
        
        # In real implementation, use injection detector
        # if self.injection_detector:
        #     detection = self.injection_detector.detect(text)
        #     if detection.is_injection:
        #         errors.append(f"Injection attempt detected: {detection.injection_type}")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            (r"(?i)ignore\s+previous", "Instruction override attempt"),
            (r"(?i)system\s*:", "System prompt injection attempt"),
        ]
        
        for pattern, description in suspicious_patterns:
            if re.search(pattern, text):
                errors.append(description)
        
        return errors


# ============================================================================
# Validation Pipeline
# ============================================================================

class ValidationPipeline:
    """
    Pipeline for comprehensive input validation.
    
    This demonstrates validation pipeline:
    - Multiple validation layers
    - Configurable validation
    - Error aggregation
    """
    
    def __init__(self):
        """Initialize validation pipeline."""
        self.format_validator = FormatValidator()
        self.content_validator = ContentValidator()
    
    def validate(
        self,
        user_input: str,
        input_type: str = "text",
        validation_level: ValidationLevel = ValidationLevel.STANDARD
    ) -> ValidationResult:
        """
        Run full validation pipeline.
        
        Args:
            user_input: User input to validate
            input_type: Type of input (text, json, etc.)
            validation_level: Validation level
        
        Returns:
            ValidationResult
        """
        all_errors = []
        all_warnings = []
        
        # Layer 1: Format validation
        if input_type == "json":
            format_result = self.format_validator.validate_json_format(user_input)
        else:
            format_result = self.format_validator.validate_text_format(user_input)
        
        all_errors.extend(format_result.errors)
        all_warnings.extend(format_result.warnings)
        
        # Layer 2: Content validation (if format valid)
        if format_result.is_valid:
            content_result = self.content_validator.validate_content(
                user_input,
                validation_level
            )
            all_errors.extend(content_result.errors)
            all_warnings.extend(content_result.warnings)
        
        # Layer 3: Schema validation (if applicable)
        if input_type == "structured":
            schema_result = self._validate_schema(user_input)
            all_errors.extend(schema_result.errors)
            all_warnings.extend(schema_result.warnings)
        
        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings
        )
    
    def _validate_schema(self, data: Any) -> ValidationResult:
        """
        Validate against schema.
        
        Args:
            data: Data to validate
        
        Returns:
            ValidationResult
        """
        errors = []
        
        try:
            # In real implementation, validate against Pydantic schema
            # UserInputSchema(**data)
            pass
        except Exception as e:
            errors.append(f"Schema validation failed: {str(e)}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=[]
        )


# ============================================================================
# Integration Examples
# ============================================================================

def validate_user_input(
    user_input: str,
    validation_level: str = "standard"
) -> Tuple[bool, List[str]]:
    """
    Validate user input before prompt construction.
    
    This demonstrates validation integration:
    - Run validation pipeline
    - Return validation status
    - Provide error messages
    
    Args:
        user_input: User input
        validation_level: Validation level
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    pipeline = ValidationPipeline()
    level = ValidationLevel(validation_level)
    
    result = pipeline.validate(
        user_input=user_input,
        input_type="text",
        validation_level=level
    )
    
    return result.is_valid, result.errors
