# Setup New Agent System

## Overview
Systematic setup of a new multi-agent system from initial planning through implementation structure. This command creates the foundation for a new agent system following multi-agent architecture patterns and LangGraph best practices.

## Rules Applied
- `multi-agent-systems` - Multi-agent architecture patterns, Orchestrator/Worker/Synthesizer, SECTIONS pattern
- `langgraph-architecture-and-nodes` - LangGraph workflow design, state definition, node implementation
- `agentic-logic-and-tools` - LangChain fundamentals, tool definitions, agent internals
- `core-python-standards` - Code quality standards, project structure

## Steps

1. **Define Requirements**
   - **Clarify Feature Scope**:
     - Understand the agent system's purpose and goals
     - Define user stories and acceptance criteria
     - Identify key capabilities and constraints
   - **Plan Technical Approach**:
     - Determine agent architecture (Orchestrator/Worker/Synthesizer)
     - Identify required tools and capabilities
     - Plan state management strategy

2. **Create Project Structure**
   - **Directory Structure**:
     - Create `langgraph/` or `workflows/` directory for workflows
     - Create `nodes/` directory for node implementations
     - Create `tools/` directory for tool definitions
     - Create `prompts/` directory for prompt templates
     - Create `schemas/` directory for Pydantic models
     - Create `tests/` directory for tests
   - **File Organization**:
     - Create main workflow file
     - Create node implementation files
     - Create tool definition files
     - Create configuration files

3. **Define LangGraph Workflow**
   - **State Schema Design**:
     - Define TypedDict for application state
     - Use clear, flat state schemas (avoid deeply nested structures)
     - Ensure state fields have meaningful names
     - Consult with team on state design (critical for multi-agent systems)
   - **Workflow Structure**:
     - Design simple, modular, and maintainable workflow
     - Plan nodes and edges for logic and conditional routing
     - Support loops and branching via graph structure
     - Plan error handling and control flow from the beginning

4. **Define Nodes (Orchestrator/Workers/Synthesizer)**
   - **Orchestrator (Planner)**:
     - Create orchestrator node to decompose user requests into sub-tasks
     - Define SECTIONS list structure
     - Attach structured fields per section
     - Ensure orchestrator does NOT execute work or produce final output
   - **Worker Agents (Specialists)**:
     - Create worker nodes for specialized sub-tasks
     - Ensure each worker focuses on one domain
     - Define worker state with assigned SECTION
     - Ensure workers do NOT modify SECTIONS list or write to other workers' SECTIONS
   - **Synthesizer**:
     - Create synthesizer node to unify worker outputs
     - Define conflict resolution logic
     - Ensure synthesizer does NOT create new tasks or call workers again

5. **Implement Node Structure**
   - **Four-Part Structure**:
     - Implement READ (inputs) → DO (logic/tool) → WRITE (outputs) → CONTROL (next action)
     - Ensure single purpose per node
     - Assign state field ownership to avoid overwrites
   - **Error Handling**:
     - Wrap core logic in try/except
     - Append errors to dedicated `errors` field
     - Route persistent failures to error-handling nodes
   - **State Management**:
     - Implement state field ownership
     - Add agent summaries to messages list in Global State

6. **Define Tools**
   - **Tool Registry**:
     - Define tools using `@tool` decorator
     - Provide deep explanations for every tool
     - Include parameters, return values, input/output examples, docstrings
   - **Tool Binding**:
     - Bind tools to the model
     - Configure tool access control (whitelisting)
     - Set up tool sandboxing if needed

7. **Create Visualization**
   - **Graph Visualization**:
     - Create/ensure `images/` directory exists
     - Save graph visualization using `workflow.get_graph().draw_png()`
     - Verify visualization shows complete workflow structure

8. **Create Basic Tests**
   - **Test Structure**:
     - Create test files in `tests/` directory
     - Mirror source code structure in tests
     - Create atomic test files named `test_<component_name>.py`
   - **Initial Tests**:
     - Test workflow initialization
     - Test basic node execution
     - Test state transitions
     - Test error handling

9. **Configuration Setup**
   - **Environment Configuration**:
     - Set up `pydantic-settings` for configuration
     - Define environment variables (no hardcoded secrets)
     - Configure logging system
   - **Tool Registry Configuration**:
     - Set up tool registry with environment-based tool selection
     - Configure Dev vs Prod tool sets

10. **Generate Setup Report**
    - Create comprehensive setup report
    - Document project structure
    - Include workflow visualization
    - Provide next steps for development

## Data Sources
- Project requirements and specifications
- Existing codebase patterns (if extending existing system)
- Team architecture decisions
- LangGraph and LangChain documentation patterns

## Output
A comprehensive agent system setup including:
- **Project Structure**: Complete directory and file organization
- **Workflow Definition**: LangGraph workflow with state schema
- **Node Implementations**: Orchestrator, Workers, Synthesizer with proper structure
- **Tool Definitions**: Tool registry with complete documentation
- **Visualization**: Graph visualization of the workflow
- **Basic Tests**: Initial test suite for workflow and nodes
- **Configuration**: Environment setup and tool registry configuration
- **Setup Report**: Documentation of setup with next steps
