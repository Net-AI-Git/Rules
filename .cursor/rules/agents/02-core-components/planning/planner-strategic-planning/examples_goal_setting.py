"""
Goal Setting Examples

This file demonstrates goal and sub-goal definition patterns, goal hierarchy, and success criteria.
Reference this example from RULE.mdc using @examples_goal_setting.py syntax.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


# ============================================================================
# Goal Definition Patterns
# ============================================================================

@dataclass
class Goal:
    """
    Goal structure with hierarchy and constraints.
    
    This demonstrates:
    - Main goals (high-level objectives)
    - Sub-goals (actionable sub-objectives)
    - Goal hierarchy (structured relationships)
    - Goal constraints (limitations, deadlines, resources)
    """
    goal_id: str
    main_goal: str
    sub_goals: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    deadline: Optional[str] = None
    priority: str = "medium"  # low, medium, high


@dataclass
class GoalHierarchy:
    """
    Goal hierarchy structure.
    
    This demonstrates:
    - Parent-child relationships between goals
    - Goal dependencies
    - Goal sequencing
    """
    root_goal: Goal
    child_goals: List[Goal] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)


class GoalSettingService:
    """
    Service for setting goals and sub-goals.
    
    This demonstrates goal setting patterns:
    - Parse user request to extract goals
    - Break down main goals into sub-goals
    - Set success criteria
    - Define goal constraints
    """
    
    def extract_goals(self, user_request: str) -> List[Goal]:
        """
        Extract goals from user request.
        
        This demonstrates:
        - Parsing user request
        - Identifying main objectives
        - Creating goal structures
        
        Args:
            user_request: User's request text
            
        Returns:
            List of goals extracted from request
        """
        # Implementation would use LLM to extract goals
        # This is a simplified example
        goal = Goal(
            goal_id="goal_1",
            main_goal="Complete user request",
            sub_goals=["Understand requirements", "Plan actions", "Execute plan"],
            success_criteria=["All requirements met", "User satisfied"],
            constraints=["Time limit: 1 hour"],
            dependencies=[],
            priority="high"
        )
        return [goal]
    
    def create_sub_goals(self, main_goal: Goal) -> List[Goal]:
        """
        Break down main goal into sub-goals.
        
        This demonstrates:
        - Goal decomposition
        - Sub-goal creation
        - Maintaining goal hierarchy
        
        Args:
            main_goal: Main goal to decompose
            
        Returns:
            List of sub-goals
        """
        sub_goals = []
        for i, sub_goal_text in enumerate(main_goal.sub_goals):
            sub_goal = Goal(
                goal_id=f"{main_goal.goal_id}_sub_{i+1}",
                main_goal=sub_goal_text,
                sub_goals=[],
                success_criteria=[f"Sub-goal {sub_goal_text} completed"],
                constraints=main_goal.constraints,
                dependencies=[main_goal.goal_id] if i > 0 else [],
                priority=main_goal.priority
            )
            sub_goals.append(sub_goal)
        return sub_goals
    
    def set_success_criteria(self, goal: Goal) -> Goal:
        """
        Set success criteria for a goal.
        
        This demonstrates:
        - Defining measurable success criteria
        - Ensuring criteria are achievable
        - Aligning criteria with goal objectives
        
        Args:
            goal: Goal to set criteria for
            
        Returns:
            Goal with success criteria set
        """
        if not goal.success_criteria:
            goal.success_criteria = [
                f"Goal {goal.main_goal} completed",
                "All sub-goals achieved",
                "Quality standards met"
            ]
        return goal
    
    def build_goal_hierarchy(self, goals: List[Goal]) -> GoalHierarchy:
        """
        Build goal hierarchy from list of goals.
        
        This demonstrates:
        - Creating goal hierarchy
        - Establishing parent-child relationships
        - Managing goal dependencies
        
        Args:
            goals: List of goals to organize
            
        Returns:
            Goal hierarchy structure
        """
        if not goals:
            raise ValueError("Cannot build hierarchy from empty goal list")
        
        root_goal = goals[0]
        child_goals = goals[1:] if len(goals) > 1 else []
        
        dependencies = {}
        for goal in goals:
            if goal.dependencies:
                dependencies[goal.goal_id] = goal.dependencies
        
        return GoalHierarchy(
            root_goal=root_goal,
            child_goals=child_goals,
            dependencies=dependencies
        )
