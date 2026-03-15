## Mandate

All agentic systems **MUST** implement a **Memory Node** as a LangGraph node (not a storage component) that provides historical context, enables learning from patterns, and feeds insights back to the Planner. The Memory Node uses the memory storage infrastructure but focuses on feedback loops and adaptive learning.

## 1. Memory Node Role and Position

### LangGraph Node (Not Storage Component)

* **Role:** LangGraph NODE that provides historical context and learning feedback.
* **Type:** Node in workflow, not storage infrastructure.
* **Purpose:**
  * Store experiences (actions, context, results)
  * Enable learning from patterns
  * Provide relevant historical context
  * Feed insights back to Planner (feedback loop)
  * Enable adaptation over time

* **Position in Workflow:** Can be called at:
  * **Conversation Start:** Load relevant memories
  * **On-Demand:** Retrieve context when needed
  * **Conversation End:** Store experiences and update memory

* **Workflow Integration:**
```
[PLANNER] → [Memory Node] (load memories) → [ORCHESTRATOR] → ...
... → [Memory Node] (store experiences) → [PLANNER] (feedback)
```

For examples see the file `examples_memory_node.py` in this folder. When using this rule, add the relevant example file(s) to the chat context. for Memory Node implementation following READ→DO→WRITE→CONTROL pattern.

## 2. Core Responsibilities

### Experience Storage

* **Mandate:** Memory Node stores experiences for future learning.

* **Experience Components:**
  * **Actions:** What actions were taken
  * **Context:** Situation and environment when actions occurred
  * **Results:** Outcomes and consequences of actions
  * **Feedback:** Success/failure indicators and user feedback

* **Storage Integration:**
  * Uses rule: memory-and-archival-management (in .amazonq/rules) for physical storage
  * Node orchestrates storage, doesn't implement it
  * Delegates to storage service for persistence
  * Manages experience extraction and formatting

* See rule: memory-and-archival-management (in .amazonq/rules) for storage patterns and infrastructure.

### Pattern Learning

* **Mandate:** Memory Node enables learning from patterns and experiences.

* **Learning Capabilities:**
  * **Pattern Recognition:** Identify recurring patterns in experiences
  * **Success Patterns:** Learn what works well
  * **Failure Patterns:** Learn what to avoid
  * **Adaptation:** Adjust behavior based on learned patterns

* **Learning Process:**
  * Analyze stored experiences
  * Extract patterns and insights
  * Update understanding based on patterns
  * Apply learned patterns to future decisions

For examples see the file `examples_learning_patterns.py` in this folder. When using this rule, add the relevant example file(s) to the chat context. for pattern learning and adaptation patterns.

### Historical Context Provision

* **Mandate:** Memory Node provides relevant historical context when needed.

* **Context Retrieval:**
  * **Semantic Search:** Find relevant memories by meaning
  * **Relevance Filtering:** Filter by recency and relevance
  * **Context Loading:** Load memories into context window
  * **Token Management:** Manage context window size

* **Retrieval Triggers:**
  * At conversation start (load user profile)
  * When context is needed (on-demand retrieval)
  * When user mentions past topics (triggered retrieval)
  * Periodically during long conversations (refresh context)

* See rule: memory-and-archival-management (in .amazonq/rules) for retrieval patterns and semantic search.

### Feedback to Planner

* **Mandate:** Memory Node feeds insights back to Planner to improve future decisions.

* **Feedback Loop:**
  * **Input:** Stored experiences and patterns
  * **Processing:** Analyze experiences for insights
  * **Output:** Feedback to Planner about past decisions
  * **Impact:** Planner uses feedback to improve planning

* **Feedback Types:**
  * **Success Feedback:** What worked well in the past
  * **Failure Feedback:** What didn't work and why
  * **Pattern Insights:** Recurring patterns and trends
  * **Recommendations:** Suggestions based on history

For examples see the file `examples_feedback_loop.py` in this folder. When using this rule, add the relevant example file(s) to the chat context. for feedback patterns to Planner and feedback loop implementation.

## 3. Node Implementation

### LangGraph Node Structure

* **Mandate:** Memory Node must follow READ→DO→WRITE→CONTROL pattern.

* **Node Structure:**
  * **READ:** Read state, context, and retrieve memories from storage
  * **DO:** Process memories, extract insights, provide feedback
  * **WRITE:** Write memories, feedback, or context to state
  * **CONTROL:** Route to next node based on operation type

* **State Management:**
  * Read: `user_request`, `context`, `conversation_history`
  * Write: `memories`, `feedback`, `historical_context`
  * Own: `memories` and `feedback` fields (single owner)

See rule: langgraph-architecture-and-nodes (in .amazonq/rules) for node implementation patterns and `examples_memory_node.py` (in this folder; add to chat context when needed) for complete Memory Node implementation.

### Node Operations

* **Load Memories Operation:**
  * **READ:** Read user context and conversation state
  * **DO:** Retrieve relevant memories from storage service
  * **WRITE:** Write memories to state for use by other nodes
  * **CONTROL:** Route to next node (Planner or Orchestrator)

* **Store Experience Operation:**
  * **READ:** Read actions, context, and results from state
  * **DO:** Extract experience, format, and store via storage service
  * **WRITE:** Write memory IDs and confirmation to state
  * **CONTROL:** Route to next node or end

* **Provide Feedback Operation:**
  * **READ:** Read stored experiences and patterns
  * **DO:** Analyze experiences, extract insights, generate feedback
  * **WRITE:** Write feedback to state for Planner
  * **CONTROL:** Route feedback to Planner node

## 4. What Memory Node MUST NOT Do

### Physical Storage Implementation

* **MUST NOT:** Handle physical storage infrastructure (memory-and-archival-management responsibility).
* **Reason:** Memory Node is a workflow node, not storage infrastructure.
* **Boundary:** Node uses storage service, doesn't implement Vector DB or PostgreSQL.

### Task Decomposition

* **MUST NOT:** Decompose tasks or create SECTIONS (Orchestrator responsibility).
* **Reason:** Memory Node provides context, doesn't plan tasks.
* **Boundary:** Node supplies memories, Orchestrator creates tasks.

### Action Execution

* **MUST NOT:** Execute actions or interact with external systems (Executor/Workers responsibility).
* **Reason:** Memory Node manages memory, doesn't execute work.
* **Boundary:** Node stores/retrieves memories, Executor/Workers execute actions.

## 5. Integration with Storage Infrastructure

### Memory Storage Service Integration

* **Purpose:** Memory Node uses memory storage service for persistence.

* **Integration Pattern:**
  * Node calls storage service methods
  * Storage service handles Vector DB and PostgreSQL
  * Node formats data for storage
  * Storage service persists data

* **Storage Operations:**
  * **Retrieve:** Call storage service to retrieve memories
  * **Store:** Call storage service to store experiences
  * **Update:** Call storage service to update memories
  * **Search:** Call storage service for semantic search

* See rule: memory-and-archival-management (in .amazonq/rules) for storage service patterns and infrastructure.

### Context Compression Integration

* **Purpose:** Memory Node integrates with context compression to manage token limits.

* **Integration:**
  * Load memories within token budget
  * Prioritize high-relevance memories
  * Compress or summarize less critical memories
  * Coordinate with compression system

* See rule: context-compression-and-optimization (in .amazonq/rules) for context compression strategies.

## 6. Integration with Planner

### Feedback Loop

* **Purpose:** Memory Node provides feedback to Planner to improve planning.

* **Feedback Flow:**
  * Memory Node analyzes stored experiences
  * Extracts insights and patterns
  * Generates feedback for Planner
  * Planner uses feedback in future planning

* **Feedback Content:**
  * Past decision outcomes
  * Success and failure patterns
  * Recommendations based on history
  * Risk assessments from past experiences

* See rule: planner-strategic-planning (in .amazonq/rules) for Planner integration patterns.

## 7. Integration with Other Systems

### API Contract Integration

* **Interface:** Memory Node must implement the Memory Node interface from rule: agent-component-interfaces (in .amazonq/rules).

* **Required Methods:**
  * `retrieve_memories(context: MemoryContext) -> List[Memory]`
  * `store_experience(experience: Experience, context: MemoryContext) -> MemoryID`
  * `provide_feedback(plan: StrategicPlan, context: MemoryContext) -> Feedback`

* See rule: agent-component-interfaces (in .amazonq/rules) for interface definitions and contract patterns.

### Error Handling

* **Memory Operations:**
  * Handle storage service failures gracefully
  * Manage missing or corrupted memories
  * Handle retrieval failures
  * Provide fallback when memories unavailable

* **Error Recovery:**
  * Log memory operation errors
  * Continue without memories if needed
  * Retry failed operations
  * Route to human review if critical

* See rule: error-handling-and-resilience (in .amazonq/rules) for comprehensive error handling patterns.

## 8. Best Practices

### Memory Quality

* **Experience Extraction:**
  * Extract meaningful experiences
  * Store actionable insights
  * Avoid storing redundant information
  * Focus on learnable patterns

* **Feedback Quality:**
  * Provide specific, actionable feedback
  * Base feedback on evidence
  * Prioritize high-impact insights
  * Keep feedback relevant and timely

### Performance Optimization

* **Efficient Retrieval:**
  * Cache frequently accessed memories
  * Optimize semantic search queries
  * Batch memory operations when possible
  * Minimize storage service calls

* **Token Management:**
  * Load memories within token budget
  * Prioritize high-relevance memories
  * Compress or summarize when needed
  * Coordinate with context compression

## 9. Examples and Patterns

For examples see the file `examples_memory_node.py` in this folder. When using this rule, add the relevant example file(s) to the chat context. for complete Memory Node implementation following READ→DO→WRITE→CONTROL pattern, including load, store, and feedback operations.

For examples see the file `examples_feedback_loop.py` in this folder. When using this rule, add the relevant example file(s) to the chat context. for feedback patterns to Planner, feedback generation, and feedback loop implementation.

For examples see the file `examples_learning_patterns.py` in this folder. When using this rule, add the relevant example file(s) to the chat context. for pattern learning and adaptation patterns, pattern recognition, and adaptive behavior.
