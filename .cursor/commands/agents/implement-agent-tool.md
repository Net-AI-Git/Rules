# Implement Agent Tool

## Overview
Implement a new tool for agent use following LangChain tool definition standards with proper Pydantic schemas, documentation, and integration into the tool registry.

## Rules Applied
- `agentic-logic-and-tools` - LangChain fundamentals, tool definitions, tool documentation
- `data-schemas-and-interfaces` - Pydantic schema standards, field descriptions, structured outputs
- `core-python-standards` - Code quality standards, type hints, function length

## Steps

1. **Define Tool Purpose**
   - **Tool Functionality**:
     - Define what the tool does and its purpose
     - Identify input parameters and return values
     - Determine tool's role in agent workflow
   - **Tool Requirements**:
     - Identify required dependencies
     - Determine if tool needs external services
     - Check if tool needs authentication or authorization

2. **Create Pydantic Schema**
   - **Schema Definition**:
     - Create Pydantic model inheriting from `pydantic.BaseModel`
     - Define all input parameters as fields
     - Use standard Python types (`str`, `int`, `float`, `bool`)
   - **Field Descriptions**:
     - Add `Field(description="...")` to EVERY field
     - Provide clear, descriptive field descriptions
     - Include examples in descriptions where helpful
   - **Constraints**:
     - Use `typing.Literal` for fields with finite options
     - Add validation constraints where needed
     - Ensure schema is reusable and well-structured

3. **Implement Tool Function**
   - **Function Implementation**:
     - Implement tool function with proper logic
     - Keep functions under 20 lines (split if needed)
     - Use full type hints for all parameters
   - **Error Handling**:
     - Implement proper error handling
     - Classify errors (transient vs permanent)
     - Return appropriate error responses
   - **Logging**:
     - Use logger (not print) for all logging
     - Log tool execution with structured format
     - Include tool name, parameters, and results in logs

4. **Add Tool Decorator**
   - **Tool Definition**:
     - Use `@tool` decorator from LangChain
     - Bind tool to the model using `.bind_tools(tools=[Schema])`
     - Configure tool with proper name and description
   - **Tool Documentation**:
     - Provide deep explanation of what tool does
     - Document parameters with types and descriptions
     - Include return value description
     - Provide input/output examples
     - Add comprehensive docstring

5. **Integrate with LLM**
   - **Structured Outputs**:
     - Use structured outputs for tool calls
     - Define schema with Pydantic models
     - Use `with_structured_output()` where applicable
   - **Tool Call Extraction**:
     - Access arguments via `response.tool_calls[0]['args']`
     - Avoid parsing raw strings
     - Validate tool call arguments against schema

6. **Add to Tool Registry**
   - **Registry Integration**:
     - Add tool to tool registry
     - Configure tool availability by environment (Dev vs Prod)
     - Set up tool whitelisting if required
   - **Access Control**:
     - Configure tool access control
     - Set up tool sandboxing if needed
     - Document tool access requirements

7. **Create Tests**
   - **Test Structure**:
     - Create test file `test_<tool_name>.py` in `tests/` directory
     - Use Arrange-Act-Assert pattern
     - Ensure tests are atomic and independent
   - **Test Cases**:
     - Test tool with valid inputs
     - Test tool with invalid inputs
     - Test error handling
     - Test tool integration with LLM
     - Test tool registry integration
   - **Mocking**:
     - Mock external dependencies
     - Use mocks for deterministic tests
     - Only integration tests should hit real services

8. **Documentation**
   - **Tool Documentation**:
     - Document tool purpose and use cases
     - Document input parameters and return values
     - Include usage examples
     - Document error conditions
   - **Code Documentation**:
     - Add docstrings to all functions
     - Include type hints for all parameters
     - Document complex logic with comments

9. **Versioning** (if applicable)
   - **Tool Versioning**:
     - Version tool if experimental or subject to change
     - Document version history
     - Support multiple versions if needed

10. **Generate Tool Implementation Report**
    - Create tool implementation summary
    - Document tool structure and functionality
    - Include test coverage information
    - Provide integration status

## Data Sources
- Tool requirements and specifications
- Existing tool patterns in codebase
- Pydantic schema examples
- LangChain tool documentation

## Output
A complete tool implementation including:
- **Pydantic Schema**: Complete schema with field descriptions and constraints
- **Tool Function**: Implementation with proper error handling and logging
- **Tool Decorator**: Properly configured LangChain tool
- **LLM Integration**: Structured outputs and tool call handling
- **Tool Registry**: Tool added to registry with access control
- **Tests**: Complete test suite with good coverage
- **Documentation**: Complete tool and code documentation
- **Implementation Report**: Summary of tool implementation with next steps
