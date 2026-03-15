"""
Action Translation Examples

This file demonstrates plan-to-action translation patterns, action structure, and action validation.
Reference this example from RULE.mdc using @examples_action_translation.py syntax.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Action Translation Types
# ============================================================================

class ActionType(str, Enum):
    """Action type enumeration."""
    API_CALL = "api_call"
    TOOL_INVOCATION = "tool_invocation"
    FILE_OPERATION = "file_operation"
    DATABASE_OPERATION = "database_operation"
    SYSTEM_COMMAND = "system_command"
    WORKER_TASK = "worker_task"


@dataclass
class StrategicPlan:
    """Strategic plan from Planner."""
    plan_id: str
    goals: List[str]
    action_sequence: List[str]
    dependencies: Dict[str, List[str]]
    risk_assessments: List[Dict[str, Any]]
    resource_requirements: Dict[str, Any]


@dataclass
class ConcreteAction:
    """Concrete action ready for execution."""
    action_id: str
    action_type: ActionType
    parameters: Dict[str, Any]
    dependencies: List[str]
    retry_config: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None
    validation_rules: Optional[List[str]] = None


# ============================================================================
# Action Translation Service
# ============================================================================

class ActionTranslationService:
    """
    Service for translating strategic plans to concrete actions.
    
    This demonstrates:
    - Plan-to-action translation
    - Action structure creation
    - Action validation
    - Parameter extraction
    """
    
    def translate_plan(self, plan: StrategicPlan, context: Dict[str, Any]) -> List[ConcreteAction]:
        """
        Translate strategic plan to concrete actions.
        
        This demonstrates:
        - Parsing plan structure
        - Converting plan elements to actions
        - Extracting parameters
        - Mapping dependencies
        
        Args:
            plan: Strategic plan from Planner
            context: Execution context
            
        Returns:
            List of concrete actions
        """
        actions = []
        
        for i, action_name in enumerate(plan.action_sequence):
            # Determine action type from plan
            action_type = self._determine_action_type(action_name, plan, context)
            
            # Extract parameters
            parameters = self._extract_parameters(action_name, plan, context)
            
            # Get dependencies
            dependencies = plan.dependencies.get(action_name, [])
            
            # Get retry config from risk assessment
            retry_config = self._get_retry_config(action_name, plan)
            
            # Create concrete action
            action = ConcreteAction(
                action_id=f"action_{i+1}_{action_name}",
                action_type=action_type,
                parameters=parameters,
                dependencies=dependencies,
                retry_config=retry_config,
                timeout=self._get_timeout(action_type),
                validation_rules=self._get_validation_rules(action_type)
            )
            
            actions.append(action)
        
        return actions
    
    def _determine_action_type(self, action_name: str, plan: StrategicPlan, 
                              context: Dict[str, Any]) -> ActionType:
        """
        Determine action type from action name and context.
        
        Args:
            action_name: Name of the action
            plan: Strategic plan
            context: Execution context
            
        Returns:
            Action type
        """
        # Simplified logic - in production would use more sophisticated determination
        if "api" in action_name.lower():
            return ActionType.API_CALL
        elif "tool" in action_name.lower():
            return ActionType.TOOL_INVOCATION
        elif "file" in action_name.lower():
            return ActionType.FILE_OPERATION
        elif "db" in action_name.lower() or "database" in action_name.lower():
            return ActionType.DATABASE_OPERATION
        elif "worker" in action_name.lower():
            return ActionType.WORKER_TASK
        else:
            return ActionType.API_CALL  # Default
    
    def _extract_parameters(self, action_name: str, plan: StrategicPlan, 
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract parameters for action.
        
        Args:
            action_name: Name of the action
            plan: Strategic plan
            context: Execution context
            
        Returns:
            Action parameters
        """
        # Extract from plan and context
        parameters = {
            "action_name": action_name,
            "goals": plan.goals,
            "context": context,
            "resource_requirements": plan.resource_requirements
        }
        
        return parameters
    
    def _get_retry_config(self, action_name: str, plan: StrategicPlan) -> Optional[Dict[str, Any]]:
        """
        Get retry configuration from risk assessment.
        
        Args:
            action_name: Name of the action
            plan: Strategic plan
            
        Returns:
            Retry configuration or None
        """
        # Find risk assessment for this action
        for risk in plan.risk_assessments:
            if risk.get("action_id") == action_name:
                risk_level = risk.get("risk_level", "medium")
                
                # Configure retry based on risk
                if risk_level == "high":
                    return {"max_attempts": 3, "backoff": "exponential", "base_delay": 2}
                elif risk_level == "medium":
                    return {"max_attempts": 2, "backoff": "linear", "base_delay": 1}
                else:
                    return {"max_attempts": 1}
        
        return None
    
    def _get_timeout(self, action_type: ActionType) -> Optional[int]:
        """
        Get timeout for action type.
        
        Args:
            action_type: Type of action
            
        Returns:
            Timeout in seconds or None
        """
        timeouts = {
            ActionType.API_CALL: 30,
            ActionType.TOOL_INVOCATION: 60,
            ActionType.FILE_OPERATION: 10,
            ActionType.DATABASE_OPERATION: 20,
            ActionType.SYSTEM_COMMAND: 120,
            ActionType.WORKER_TASK: 300
        }
        return timeouts.get(action_type)
    
    def _get_validation_rules(self, action_type: ActionType) -> List[str]:
        """
        Get validation rules for action type.
        
        Args:
            action_type: Type of action
            
        Returns:
            List of validation rules
        """
        rules = {
            ActionType.API_CALL: ["validate_url", "validate_parameters", "check_authentication"],
            ActionType.TOOL_INVOCATION: ["validate_tool_exists", "validate_parameters"],
            ActionType.FILE_OPERATION: ["validate_path", "check_permissions"],
            ActionType.DATABASE_OPERATION: ["validate_query", "check_connection"],
            ActionType.SYSTEM_COMMAND: ["validate_command", "check_permissions"],
            ActionType.WORKER_TASK: ["validate_section", "check_worker_availability"]
        }
        return rules.get(action_type, [])
    
    def validate_action(self, action: ConcreteAction) -> Tuple[bool, List[str]]:
        """
        Validate action before execution.
        
        This demonstrates:
        - Action validation
        - Parameter checking
        - Dependency verification
        
        Args:
            action: Action to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate action ID
        if not action.action_id:
            errors.append("Action ID is required")
        
        # Validate action type
        if not action.action_type:
            errors.append("Action type is required")
        
        # Validate parameters
        if not action.parameters:
            errors.append("Action parameters are required")
        
        # Validate based on validation rules
        if action.validation_rules:
            for rule in action.validation_rules:
                # Simplified - in production would actually validate
                pass
        
        return len(errors) == 0, errors
