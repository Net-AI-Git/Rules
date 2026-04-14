## 1. Beyond Unit Testing

* **The Gap:** Standard `pytest` checks logic consistency. It cannot verify if an answer is "helpful" or "factually correct."

* **Mandate:** You must implement **LLM-based Evaluations (Evals)** for every agentic workflow.

* **Frameworks:** Use **Ragas** or **DeepEval** for running evals. **Evaluation results and metrics MUST be sent to Splunk** (via HEC) for storage, dashboards, and analysis using **SPL**.


## 2. Mandatory Metrics

For every generative task, you must define and measure:

* **Faithfulness:** Does the answer rely *only* on the retrieved context? (Prevents hallucinations).

* **Answer Relevance:** Does the answer actually address the user's prompt?

* **Context Precision:** Did the retrieval step fetch relevant chunks?

* **Tool Usage Accuracy:** Did the agent select the correct tool and parameters for the task?


## 3. Implementation Strategy

* **Golden Datasets:** Create a dedicated test set (`datasets/golden_qa.json`) with inputs and "expected ideal answers" (Ground Truth).

* **LLM-as-a-Judge (traces, audit tables, verdict JSON):** Use the **`@evaluate-with-llm-judge`** skill only—full mandate, rubric, and output schema live in that skill (not in a separate rule).

* **CI/CD Integration:** Evals must run on a subset of data during PR checks. They are slower/costlier than unit tests, so treat them as integration tests.

* **Synthetic Data:** Use the LLM to generate test cases for itself (e.g., "Given this document, generate 5 questions and answers") to bootstrap coverage.


## 4. Deterministic vs. Probabilistic

* **Separate Concerns:** Keep deterministic logic tests (math, routing rules) in `pytest`. Keep probabilistic quality checks in the Evaluation suite.

## 5. Evaluation Best Practices

* **Production Monitoring:** Use evaluation frameworks to monitor quality and compliance in production environments.

* **Continuous Improvement:** Regularly update evaluation datasets and metrics based on production feedback.

* **Resources:** Reference OpenAI Evaluation best practices for detailed guidance on building evals to monitor quality and compliance in production.

* **See:** `@security-governance-and-observability` for release/eval posture alongside agent security.
