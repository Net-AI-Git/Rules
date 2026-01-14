# Run Evaluation Suite

## Overview
Execute the complete LLM evaluation suite using specialized evaluation frameworks (Ragas, DeepEval, LangSmith) to measure agent performance, quality, and compliance. This command provides comprehensive evaluation metrics for generative AI systems.

## Rules Applied
- `llm-evaluation-and-metrics` - LLM evaluation standards and mandatory metrics
- `llm-judge-protocol` - LLM Judge evaluation protocol and rubric
- `monitoring-and-observability` - LangSmith integration and tracing

## Steps

1. **Prepare Evaluation Environment**
   - Verify evaluation frameworks are installed (Ragas, DeepEval, LangSmith)
   - Check for golden dataset (`datasets/golden_qa.json` or similar)
   - Validate evaluation configuration and parameters
   - Ensure LangSmith tracing is enabled if applicable

2. **Execute Evaluation Metrics**
   - **Faithfulness**: Verify answers rely only on retrieved context (prevent hallucinations)
   - **Answer Relevance**: Check if answers address user prompts correctly
   - **Context Precision**: Validate retrieval step fetched relevant chunks
   - **Tool Usage Accuracy**: Evaluate agent tool selection and parameter validity
   - Run evaluation on golden dataset or specified test set

3. **Collect Evaluation Data**
   - Gather evaluation results from all frameworks
   - Collect LangSmith traces for LLM operations
   - Extract performance metrics (latency, token usage, costs)
   - Capture evaluation execution logs

4. **Compare Against Golden Dataset**
   - Compare actual outputs with expected ideal answers (Ground Truth)
   - Calculate accuracy metrics and deviation scores
   - Identify cases where outputs don't match expectations
   - Analyze patterns in mismatches

5. **Analyze Evaluation Results**
   - Calculate average scores for each metric
   - Identify metrics below acceptable thresholds
   - Find specific test cases with poor performance
   - Detect systematic issues (e.g., consistent hallucination patterns)

6. **Generate Evaluation Report**
   - Create structured report with all metrics
   - Include per-metric breakdowns and scores
   - Highlight areas requiring improvement
   - Provide specific examples of failures or low scores
   - Compare current results with previous evaluations (if available)

7. **Provide Improvement Recommendations**
   - Suggest prompt engineering improvements
   - Recommend retrieval strategy adjustments
   - Propose tool usage optimizations
   - Identify areas needing additional training data

## Data Sources
- Golden dataset (`datasets/golden_qa.json` or similar)
- Evaluation framework outputs (Ragas, DeepEval)
- LangSmith traces and evaluation runs
- Evaluation configuration files
- Previous evaluation results (for comparison)

## Output
A comprehensive evaluation report including:
- Metric scores (Faithfulness, Answer Relevance, Context Precision, Tool Usage Accuracy)
- Comparison with golden dataset results
- Performance metrics (latency, token usage, costs)
- Specific test case analysis with examples
- Areas requiring improvement with priority levels
- Actionable recommendations for each metric
- Trend analysis if historical data available
