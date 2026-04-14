"""
SECTIONS Pattern Implementation Example

This file demonstrates the generic SECTIONS pattern structure and assignment.
Reference this example from RULE.mdc using @examples_sections.py syntax.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


# ============================================================================
# SECTIONS Pattern
# ============================================================================

@dataclass
class Section:
    """
    Generic SECTION structure - the mandatory unit of work.
    
    This demonstrates the SECTION pattern:
    - SECTION is a task contract defining what one worker must produce
    - Each SECTION owned by exactly one worker
    - SECTION must not be shared for writing
    """
    section_id: str
    task_id: str
    scope: str
    inputs: Dict[str, Any]
    constraints: List[str]
    expected_output_shape: Dict[str, Any]


class SectionManager:
    """
    Generic SECTION management pattern.
    
    This demonstrates the pattern for SECTION assignment:
    - Create SECTIONS from task decomposition
    - Assign each SECTION to one worker
    - Ensure SECTION isolation (no shared writing)
    """
    
    def create_sections(
        self,
        task_id: str,
        sub_tasks: List[Dict[str, Any]]
    ) -> List[Section]:
        """
        Create SECTIONS from sub-tasks.
        
        This demonstrates the pattern for SECTION creation:
        - Each sub-task becomes a SECTION
        - SECTION contains all necessary information for worker
        - SECTION defines expected output shape
        
        Args:
            task_id: Parent task identifier
            sub_tasks: List of sub-tasks to convert to SECTIONS
            
        Returns:
            List of SECTIONS
        """
        sections = []
        
        for idx, sub_task in enumerate(sub_tasks):
            section = Section(
                section_id=f"{task_id}_section_{idx}",
                task_id=task_id,
                scope=sub_task.get("scope", ""),
                inputs=sub_task.get("inputs", {}),
                constraints=sub_task.get("constraints", []),
                expected_output_shape=sub_task.get("output_shape", {})
            )
            sections.append(section)
        
        return sections
    
    def assign_to_worker(
        self,
        section: Section,
        worker_id: str
    ) -> Dict[str, Any]:
        """
        Assign SECTION to worker.
        
        This demonstrates the pattern for SECTION assignment:
        - Each SECTION sent to one worker as worker_state.section
        - Worker treats SECTION as single source of truth
        - SECTION ownership is exclusive
        
        Args:
            section: SECTION to assign
            worker_id: Worker identifier
            
        Returns:
            Worker state with assigned SECTION
        """
        return {
            "worker_id": worker_id,
            "section": section,
            "status": "assigned"
        }
