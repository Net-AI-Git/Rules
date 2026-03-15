"""
Reviewer Node Examples

This file demonstrates Reviewer Node implementation and critique process.
Reference this example from RULE.mdc using @examples_reviewer_node.py syntax.
"""

from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Review Status and Actions
# ============================================================================

class ReviewStatus(Enum):
    """
    Review status outcomes.
    
    This demonstrates review outcomes:
    - Approved: Quality meets threshold
    - NeedsRevision: Quality below threshold, needs improvement
    - Rejected: Quality too low, cannot proceed
    """
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    REJECTED = "rejected"


class ReviewAction(Enum):
    """
    Actions to take based on review.
    
    This demonstrates review actions:
    - Proceed: Send to Synthesizer
    - Revise: Send back to Worker for revision
    - Reject: Do not proceed, request human review
    """
    PROCEED = "proceed"
    REVISE = "revise"
    REJECT = "reject"


@dataclass
class ReviewResult:
    """
    Result of review evaluation.
    
    This demonstrates review result structure:
    - Status: Approval status
    - Quality score: Overall quality (0.0-1.0)
    - Dimension scores: Scores per dimension
    - Errors: List of errors found
    - Critique: Feedback for improvement
    - Action: Recommended action
    """
    status: ReviewStatus
    quality_score: float
    dimension_scores: Dict[str, float]
    errors: List[Dict[str, Any]]
    critique: str
    action: ReviewAction
    revision_instructions: Optional[str] = None


# ============================================================================
# Critique Prompts
# ============================================================================

class CritiquePromptTemplates:
    """
    Templates for structured critique prompts.
    
    This demonstrates critique prompt patterns:
    - Structured evaluation prompts
    - Multi-dimensional assessment
    - Error detection prompts
    """
    
    @staticmethod
    def get_evaluation_prompt(output: str, requirements: Dict[str, Any]) -> str:
        """
        Generate evaluation prompt.
        
        Args:
            output: Output to evaluate
            requirements: Requirements dictionary
        
        Returns:
            Evaluation prompt
        """
        return f"""Evaluate the following output against the requirements.

Output to evaluate:
{output}

Requirements:
- Accuracy: {requirements.get('accuracy_required', True)}
- Completeness: {requirements.get('completeness_required', True)}
- Coherence: {requirements.get('coherence_required', True)}
- Format: {requirements.get('format_requirements', 'Any format')}

Evaluate the output on these dimensions:
1. Factual Accuracy: Check if all facts are correct and verifiable
2. Completeness: Verify all required elements are present
3. Coherence: Check if content flows logically and consistently
4. Quality: Assess overall quality and usefulness

Provide:
- Quality score (0.0-1.0) for each dimension
- Overall quality score (0.0-1.0)
- List of errors found (if any)
- Critique and suggestions for improvement
- Recommendation: APPROVED, NEEDS_REVISION, or REJECTED"""
    
    @staticmethod
    def get_error_detection_prompt(output: str) -> str:
        """
        Generate error detection prompt.
        
        Args:
            output: Output to check for errors
        
        Returns:
            Error detection prompt
        """
        return f"""Check the following output for errors:

{output}

Check for:
1. Factual errors (incorrect information)
2. Logical errors (contradictions, inconsistencies)
3. Format errors (structure, schema violations)
4. Missing information (required elements not present)

For each error found, provide:
- Error type (factual/logical/format/missing)
- Severity (critical/major/minor)
- Description
- Location in output
- Suggested fix"""
    
    @staticmethod
    def get_revision_instructions_prompt(
        output: str,
        errors: List[Dict[str, Any]],
        critique: str
    ) -> str:
        """
        Generate revision instructions prompt.
        
        Args:
            output: Original output
            errors: List of errors found
            critique: Critique feedback
        
        Returns:
            Revision instructions prompt
        """
        errors_text = "\n".join([
            f"- {err.get('type', 'unknown')} ({err.get('severity', 'unknown')}): {err.get('description', '')}"
            for err in errors
        ])
        
        return f"""Based on the review, provide specific revision instructions.

Original output:
{output}

Errors found:
{errors_text}

Critique:
{critique}

Provide clear, actionable revision instructions:
1. Specific errors to fix
2. Missing elements to add
3. Improvements to make
4. Format corrections needed"""


# ============================================================================
# Reviewer Node
# ============================================================================

class ReviewerNode:
    """
    Reviewer Node for evaluating agent outputs.
    
    This demonstrates Reviewer Node pattern:
    - Evaluate outputs against criteria
    - Provide critique and feedback
    - Decide on approval/revision/rejection
    - Generate revision instructions
    """
    
    def __init__(
        self,
        llm_client: Any,
        quality_threshold: float = 0.8,
        rejection_threshold: float = 0.5
    ):
        """
        Initialize Reviewer Node.
        
        Args:
            llm_client: LLM client for evaluation
            quality_threshold: Minimum quality score for approval
            rejection_threshold: Maximum quality score for rejection
        """
        self.llm_client = llm_client
        self.quality_threshold = quality_threshold
        self.rejection_threshold = rejection_threshold
        self.prompt_templates = CritiquePromptTemplates()
    
    def review_output(
        self,
        output: str,
        requirements: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> ReviewResult:
        """
        Review an output.
        
        Args:
            output: Output to review
            requirements: Requirements dictionary
            context: Optional context for evaluation
        
        Returns:
            ReviewResult
        """
        # Generate evaluation prompt
        eval_prompt = self.prompt_templates.get_evaluation_prompt(output, requirements)
        
        # In real implementation, call LLM for evaluation
        # eval_response = self.llm_client.generate(eval_prompt)
        # For example, parse response:
        eval_response = self._parse_evaluation_response(eval_prompt)  # Placeholder
        
        # Extract scores and errors
        quality_score = eval_response.get("overall_score", 0.5)
        dimension_scores = eval_response.get("dimension_scores", {})
        errors = eval_response.get("errors", [])
        critique = eval_response.get("critique", "")
        recommendation = eval_response.get("recommendation", "NEEDS_REVISION")
        
        # Determine status and action
        status, action = self._determine_status_and_action(
            quality_score, recommendation
        )
        
        # Generate revision instructions if needed
        revision_instructions = None
        if action == ReviewAction.REVISE:
            revision_instructions = self._generate_revision_instructions(
                output, errors, critique
            )
        
        return ReviewResult(
            status=status,
            quality_score=quality_score,
            dimension_scores=dimension_scores,
            errors=errors,
            critique=critique,
            action=action,
            revision_instructions=revision_instructions
        )
    
    def _parse_evaluation_response(self, prompt: str) -> Dict[str, Any]:
        """
        Parse LLM evaluation response.
        
        Args:
            prompt: Evaluation prompt
        
        Returns:
            Parsed evaluation response
        """
        # In real implementation, parse LLM response
        # For example:
        return {
            "overall_score": 0.75,
            "dimension_scores": {
                "accuracy": 0.8,
                "completeness": 0.7,
                "coherence": 0.8,
                "quality": 0.75
            },
            "errors": [
                {
                    "type": "missing",
                    "severity": "major",
                    "description": "Missing required section: conclusion"
                }
            ],
            "critique": "Output is generally good but missing conclusion section.",
            "recommendation": "NEEDS_REVISION"
        }
    
    def _determine_status_and_action(
        self,
        quality_score: float,
        recommendation: str
    ) -> tuple[ReviewStatus, ReviewAction]:
        """
        Determine review status and action.
        
        Args:
            quality_score: Quality score
            recommendation: LLM recommendation
        
        Returns:
            Tuple of (ReviewStatus, ReviewAction)
        """
        if quality_score >= self.quality_threshold:
            return (ReviewStatus.APPROVED, ReviewAction.PROCEED)
        elif quality_score <= self.rejection_threshold:
            return (ReviewStatus.REJECTED, ReviewAction.REJECT)
        else:
            return (ReviewStatus.NEEDS_REVISION, ReviewAction.REVISE)
    
    def _generate_revision_instructions(
        self,
        output: str,
        errors: List[Dict[str, Any]],
        critique: str
    ) -> str:
        """
        Generate revision instructions.
        
        Args:
            output: Original output
            errors: List of errors
            critique: Critique feedback
        
        Returns:
            Revision instructions
        """
        # Generate revision prompt
        revision_prompt = self.prompt_templates.get_revision_instructions_prompt(
            output, errors, critique
        )
        
        # In real implementation, call LLM for revision instructions
        # revision_instructions = self.llm_client.generate(revision_prompt)
        
        # For example:
        revision_instructions = f"""Based on the review, please make the following revisions:

1. Fix the following errors:
{chr(10).join([f"   - {err.get('description', '')}" for err in errors])}

2. Address the critique:
   {critique}

3. Ensure all required elements are present and properly formatted."""
        
        return revision_instructions


# ============================================================================
# LangGraph Node Integration
# ============================================================================

def reviewer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for reviewer.
    
    This demonstrates reviewer node integration:
    - Read worker outputs from state
    - Review each output
    - Update state with review results
    - Route based on review status
    
    Args:
        state: GraphState
        
    Returns:
        Updated state
    """
    # Extract worker outputs
    worker_outputs = state.get("worker_outputs", [])
    requirements = state.get("requirements", {})
    
    # Initialize reviewer
    reviewer = ReviewerNode(llm_client=None)  # In real implementation, pass actual client
    
    # Review each output
    review_results = []
    for output in worker_outputs:
        result = reviewer.review_output(
            output=output.get("content", ""),
            requirements=requirements,
            context=state.get("context", {})
        )
        review_results.append({
            "output_id": output.get("id"),
            "review_result": result
        })
    
    # Update state
    state["review_results"] = review_results
    
    # Determine next action
    all_approved = all(
        result["review_result"].status == ReviewStatus.APPROVED
        for result in review_results
    )
    
    if all_approved:
        state["next_node"] = "synthesizer"
    else:
        # Check if any need revision
        needs_revision = any(
            result["review_result"].action == ReviewAction.REVISE
            for result in review_results
        )
        
        if needs_revision:
            state["next_node"] = "worker_revision"
        else:
            state["next_node"] = "human_review"
    
    return state
