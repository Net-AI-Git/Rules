"""
Multi-Agent Orchestration Pattern Example

This file demonstrates the generic Orchestrator/Worker/Synthesizer architecture pattern.
Reference this example from RULE.mdc using @examples_orchestration.py syntax.
"""

from typing import List, Dict, Any, TypedDict
from dataclasses import dataclass


# ============================================================================
# Orchestrator/Worker/Synthesizer Pattern
# ============================================================================

@dataclass
class Section:
    """
    Generic SECTION structure for task decomposition.
    
    This demonstrates the SECTION pattern:
    - Identifiers (section_id, task_id)
    - Scope (what to produce)
    - Inputs (required data)
    - Constraints (limitations, rules)
    - Expected output shape
    """
    section_id: str
    task_id: str
    scope: str
    inputs: Dict[str, Any]
    constraints: List[str]
    expected_output_shape: Dict[str, Any]


class Orchestrator:
    """
    Generic Orchestrator pattern.
    
    This demonstrates the Orchestrator role:
    - Decompose user requests into sub-tasks
    - Create SECTIONS list
    - Attach structured fields per section
    - MUST NOT execute work or produce final output
    """
    
    def decompose_request(self, user_request: str) -> List[Section]:
        """
        Decompose user request into SECTIONS.
        
        This demonstrates the pattern for task decomposition:
        - Parse user request
        - Identify sub-tasks
        - Create SECTION for each sub-task
        - Define scope, inputs, constraints, and output shape
        
        Args:
            user_request: User's request to decompose
            
        Returns:
            List of SECTIONS representing sub-tasks
        """
        sections = []
        
        # Example: Create sections based on request analysis
        # In real implementation, this would use LLM or rule-based logic
        section = Section(
            section_id="section_1",
            task_id="task_1",
            scope="Process first part of request",
            inputs={"request": user_request},
            constraints=["Follow specified format"],
            expected_output_shape={"type": "dict", "fields": ["result"]}
        )
        sections.append(section)
        
        return sections


class Worker:
    """
    Generic Worker pattern.
    
    This demonstrates the Worker role:
    - Read assigned SECTION
    - Execute specialized work
    - Write to designated output key
    - MUST NOT modify SECTIONS list or write to another worker's SECTION
    """
    
    def __init__(self, worker_id: str):
        """
        Initialize worker.
        
        Args:
            worker_id: Unique identifier for this worker
        """
        self.worker_id = worker_id
    
    def execute_section(self, section: Section) -> Dict[str, Any]:
        """
        Execute work for assigned SECTION.
        
        This demonstrates the pattern for worker execution:
        - Read SECTION as single source of truth
        - Execute specialized work based on SECTION scope
        - Return result in expected output shape
        
        Args:
            section: Assigned SECTION to execute
            
        Returns:
            Result in expected output shape
        """
        # Execute work based on section scope
        result = {
            "section_id": section.section_id,
            "worker_id": self.worker_id,
            "result": "Processed section"
        }
        
        return result


class Synthesizer:
    """
    Generic Synthesizer pattern.
    
    This demonstrates the Synthesizer role:
    - Read collected worker outputs
    - Merge into FINAL_OUTPUT
    - Resolve conflicts
    - MUST NOT create new tasks or call workers again
    """
    
    def synthesize(self, worker_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Unify worker outputs into final output.
        
        This demonstrates the pattern for synthesis:
        - Collect all worker outputs
        - Merge into coherent final output
        - Resolve any conflicts between outputs
        
        Args:
            worker_outputs: List of outputs from all workers
            
        Returns:
            Unified final output
        """
        final_output = {
            "status": "completed",
            "sections_processed": len(worker_outputs),
            "results": worker_outputs
        }
        
        return final_output
