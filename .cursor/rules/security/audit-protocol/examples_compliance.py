"""
Compliance Validation Pattern Example

This file demonstrates the generic compliance validation pattern structure.
Reference this example from RULE.mdc using @examples_compliance.py syntax.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# Compliance Validation Pattern
# ============================================================================

class ComplianceType(str, Enum):
    """Types of compliance checks."""
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOC2 = "soc2"


@dataclass
class ComplianceCheck:
    """
    Generic compliance check structure.
    
    This demonstrates the pattern for validating compliance requirements:
    - Check type (GDPR, HIPAA, SOC2)
    - Validation rules
    - Check results
    - Remediation actions
    """
    check_type: ComplianceType
    rule_name: str
    passed: bool
    details: Dict[str, Any]
    remediation: List[str] | None = None


class ComplianceValidator:
    """
    Generic compliance validator pattern.
    
    This demonstrates the structure for automated compliance validation:
    - Real-time validation checks
    - Periodic audit checks
    - Compliance reporting
    """
    
    def __init__(self, audit_logger: Any):
        """
        Initialize compliance validator.
        
        Args:
            audit_logger: Audit logger for compliance event logging
        """
        self.audit_logger = audit_logger
        self.checks: List[ComplianceCheck] = []
    
    def validate_input_compliance(
        self,
        data: Dict[str, Any],
        compliance_type: ComplianceType
    ) -> ComplianceCheck:
        """
        Validate input data against compliance requirements.
        
        This demonstrates the pattern for real-time compliance validation:
        - PII detection and masking
        - Data classification
        - Input sanitization
        
        Args:
            data: Input data to validate
            compliance_type: Type of compliance to check
            
        Returns:
            ComplianceCheck: Result of the compliance check
        """
        check = ComplianceCheck(
            check_type=compliance_type,
            rule_name="input_validation",
            passed=True,
            details={}
        )
        
        if compliance_type == ComplianceType.GDPR:
            check = self._validate_gdpr_input(data)
        elif compliance_type == ComplianceType.HIPAA:
            check = self._validate_hipaa_input(data)
        
        self.checks.append(check)
        self._log_compliance_check(check)
        
        return check
    
    def _validate_gdpr_input(self, data: Dict[str, Any]) -> ComplianceCheck:
        """
        Validate GDPR compliance for input data.
        
        Returns:
            ComplianceCheck: GDPR validation result
        """
        details = {
            "pii_detected": False,
            "pii_masked": False,
            "data_classified": True
        }
        
        return ComplianceCheck(
            check_type=ComplianceType.GDPR,
            rule_name="gdpr_input_validation",
            passed=True,
            details=details
        )
    
    def _validate_hipaa_input(self, data: Dict[str, Any]) -> ComplianceCheck:
        """
        Validate HIPAA compliance for input data.
        
        Returns:
            ComplianceCheck: HIPAA validation result
        """
        details = {
            "phi_detected": False,
            "access_authorized": True
        }
        
        return ComplianceCheck(
            check_type=ComplianceType.HIPAA,
            rule_name="hipaa_input_validation",
            passed=True,
            details=details
        )
    
    def _log_compliance_check(self, check: ComplianceCheck) -> None:
        """
        Log compliance check result to audit trail.
        
        Args:
            check: Compliance check result
        """
        self.audit_logger.log_event(
            event_type="compliance_check",
            actor_id="system",
            actor_type="system",
            resource="compliance_validation",
            action=check.rule_name,
            result="success" if check.passed else "failure",
            correlation_id="compliance_check",
            metadata={
                "compliance_type": check.check_type.value,
                "details": check.details
            }
        )
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """
        Generate compliance report from all checks.
        
        Returns:
            Dict containing compliance report data
        """
        return {
            "total_checks": len(self.checks),
            "passed": sum(1 for c in self.checks if c.passed),
            "failed": sum(1 for c in self.checks if not c.passed),
            "checks": [asdict(check) for check in self.checks]
        }
