## Mandate

When creating or updating project rules for **Amazon Q Developer** in this repository, you **MUST** follow this guide. Rules live under `.amazonq/rules` and use Markdown (`.md`) files. This document defines structure and process for rules used by Amazon Q.

**Writing rules for Amazon Q Developer:** For the canonical format (location, structure, no frontmatter, how to reference example files), see **amazon-q-developer-rules-guide.md** in this folder. That guide is the source of truth for writing rules that Amazon Q loads from `.amazonq/rules`.

## What are Amazon Q project rules?

Project rules are Markdown files under `.amazonq/rules` that describe coding standards and best practices. Amazon Q Developer loads them automatically when you chat in the project, so the assistant follows your team's conventions without repeating instructions every time. Rules are version-controlled with the repo.

## Directory Structure

Rules in this repository are organized by category:

```
.amazonq/rules/
├── core/              # Core rules (Python standards, error handling)
├── security/          # Security and governance rules
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/      # Testing, code review, versioning
├── api/              # API-related rules
├── data/             # Data schemas, migrations
├── evaluation/       # LLM evaluation, judging, auditing
├── configuration/    # Configuration, dependency injection, prompts
└── rules-management/ # This rule and amazon-q-developer-rules-guide.md
```

### Rule Folder Structure

Each rule is a **folder** containing a `RULE.md` (Markdown) file and optionally example files:

```
.amazonq/rules/
  category-name/
    rule-name/
      RULE.md
      examples_*.py    # optional
```

**Important:**
- Each rule is in its own folder; folder name should be kebab-case (e.g., `core-python-standards`)
- The rule file is `RULE.md`. Amazon Q does not use YAML frontmatter

## Rule File Format (Amazon Q)

Every rule file is **Markdown** (`.md`). Amazon Q does **not** use YAML frontmatter. Use the structure recommended in **amazon-q-developer-rules-guide.md**: Purpose, Instructions, Priority, Error Handling. For Cursor-specific frontmatter and rule types (used in `.cursor/rules` in this repo), see rule: frontmatter-reference (in .amazonq/rules) for reference only.

## Creating a New Rule

### Step 1: Determine Category

Choose the appropriate category folder:
- `core/` - Essential rules for all projects
- `security/` - Security and governance
- `agents/` - Agent-specific patterns
- `infrastructure/` - Deployment and operations
- `development/` - Development workflow
- `api/` - API development
- `data/` - Data management
- `evaluation/` - LLM evaluation
- `configuration/` - Configuration management

### Step 2: Choose Rule Name

- Use kebab-case (lowercase with hyphens)
- Be descriptive and specific
- Examples: `core-python-standards`, `api-documentation-standards`, `error-handling-and-resilience`

### Step 3: Create Folder Structure

Create the folder path:
```
.amazonq/rules/[category]/[rule-name]/
  RULE.md
  [optional example files]
```

**CRITICAL: Use Helper Files for Code Examples**

**MANDATE:** When writing rules with code examples, you **MUST** use separate helper files instead of embedding large code blocks directly in the rule Markdown. This keeps rules focused on guidance rather than implementation details.

See rule: helper-files-guide (in .amazonq/rules) for complete guide on:
- When and how to use helper files
- Naming conventions and folder structure
- How to reference helper files using `@filename` syntax
- Best practices for organizing code examples
- Validation checklist

**Quick Summary:**
- Helper files should be in the same folder as the rule file (RULE.md)
- Use `examples_*.py` (or appropriate extension) naming convention
- In the rule text, reference helper files by name (e.g. "See example file `examples_server.py` in this folder"); add them to chat context when needed
- Keep the rule file under 400 lines by extracting code examples

### Step 4: Write Rule Content

- Use markdown formatting; recommended sections: Purpose, Instructions, Priority, Error Handling (see amazon-q-developer-rules-guide.md)
- **Do NOT** include a main title as `# Title` if the folder name is the title; start with `## Section` or content
- Be clear, actionable, and specific
- Reference other rules by name (e.g. "See rule: rule-name in .amazonq/rules") and example files by path/name

### Step 5: Validate Structure

Ensure:
- Folder name is kebab-case
- File is named `RULE.md` (Markdown)
- Content follows markdown best practices
- Rule is under 500 lines (split if larger)

## Updating an Existing Rule

### Step 1: Locate the Rule

Find the rule in the appropriate category folder:
```
.amazonq/rules/[category]/[rule-name]/RULE.md
```

### Step 2: Understand Current Structure

- Read the existing frontmatter
- Understand the rule type
- Note the current content structure

### Step 3: Update Content

When updating:
- **Maintain** the existing structure and style
- **Update** only the necessary sections
- **Keep** references to other rules/files intact
- **Ensure** markdown formatting is preserved

### Step 4: Validate

After update:
- Content is properly formatted
- Rule is still under 500 lines
- All references are still valid

## Best Practices

### Content Guidelines

1. **Keep Rules Focused**
   - Each rule should cover one specific domain
   - Avoid mixing unrelated topics
   - Split large rules into multiple, composable rules

2. **Length Limit and Helper Files**
   - Keep rules under 400 lines (target: 300 lines or less)
   - **MANDATE:** Use helper files for code examples - see rule: helper-files-guide (in .amazonq/rules) for complete guide
   - Move code examples to `examples_*.py` (or other appropriate extensions) files
   - Reference examples by file name (e.g. "See example file `examples_server.py` in this folder")
   - If a rule still exceeds 400 lines after extracting examples, split it into multiple rules

3. **Be Actionable**
   - Provide concrete, actionable guidance
   - Avoid vague instructions
   - Include examples when helpful

4. **Reference, Don't Copy**
   - **MANDATE:** Use helper files for code examples - see rule: helper-files-guide (in .amazonq/rules) for complete guide
- Reference files by name instead of copying content into the rule
  - Reference other rules: See rule: core-python-standards (in .amazonq/rules) for coding standards
  - Reference helper files in the same folder (e.g. "See example file `examples_server.py` in this folder"); add to chat context when needed
  - Amazon Q can use workspace context or the user can tag the example file with the rule
   - **Best practice:** For rules with multiple code examples, always create `examples_*.py` files and reference them

5. **Clear Structure**
   - Use markdown headers (`##`, `###`) for organization
   - Use lists for multiple items
   - Use code blocks for examples

### What to Avoid

1. **Don't Copy Entire Style Guides**
   - Use a linter instead
   - Agent already knows common style conventions

2. **Don't Document Every Command**
   - Agent knows common tools like npm, git, pytest
   - Focus on project-specific patterns

3. **Don't Add Edge Cases**
   - Keep rules focused on patterns you use frequently
   - Avoid documenting rare edge cases

4. **Don't Duplicate Code**
   - **MANDATE:** Use helper files for code examples - see rule: helper-files-guide (in .amazonq/rules)
   - Point to canonical examples instead of copying code
- Reference example files by name; only include very short snippets (under 10 lines) inline
- Always create separate helper files when the rule has multiple examples or examples are 15+ lines

5. **Don't Include Main Title**
   - Start with `## Section` or content directly
   - The rule name (folder name) is the title

## Examples

### Example: Rule with Helper Files

**Location:** `.amazonq/rules/api/mcp-protocol-implementation/RULE.md`

**Folder Structure:**
```
.amazonq/rules/api/mcp-protocol-implementation/
  RULE.md
  examples_server.py
  examples_client.py
  examples_integration.py
```

**RULE.md content (excerpt):**
```markdown
## MCP Server Implementation

For examples see the file `examples_server.py` in this folder. When using this rule, add the relevant example file(s) to the chat context.

## Client Implementation

For examples see the file `examples_client.py` in this folder. When using this rule, add the relevant example file(s) to the chat context.

## Complete Examples

- **`examples_server.py` (in this folder; add to chat context when needed)**: Server implementation examples
- **`examples_client.py` (in this folder; add to chat context when needed)**: Client implementation examples
- **`examples_integration.py` (in this folder; add to chat context when needed)**: Integration patterns
```

**Key Points:**
- Rule stays focused on guidance (~300 lines)
- Code examples are in separate helper files
- References use `@filename` syntax
- See rule: helper-files-guide (in .amazonq/rules) for complete guide on using helper files

### Other Rule Type Examples

For examples of all 4 rule types (Always Apply, Apply Intelligently, Apply to Specific Files, Apply Manually), see rule: frontmatter-reference (in .amazonq/rules) which includes complete examples for each type.

## Validation Checklist

Before finalizing any rule creation or update, verify:

- [ ] Folder name is kebab-case
- [ ] File is named `RULE.md` (Markdown)
- [ ] No YAML frontmatter (Amazon Q does not use it)
- [ ] No main title (`# Title`) if folder name is the title; start with sections or content
- [ ] Rule is under 400 lines (use helper files to achieve this)
- [ ] Markdown formatting is correct
- [ ] Example files are referenced by name in the rule
- [ ] Content is clear, actionable, and specific
- [ ] If using helper files (see rule: helper-files-guide (in .amazonq/rules)):
  - [ ] Helper files are in the same folder as RULE.md
  - [ ] Helper files use `examples_*.py` naming convention
  - [ ] Rule refers to each helper file (e.g. "See example file `examples_*.py` in this folder")
  - [ ] Helper files contain complete, runnable code
  - [ ] Rule explains what each helper file demonstrates

## Quick Reference

### Frontmatter Templates

See rule: frontmatter-reference (in .amazonq/rules) for complete frontmatter templates, detailed instructions, and quick reference for all 4 rule types.

### Helper Files Guide

See rule: helper-files-guide (in .amazonq/rules) for complete guide on using helper files for code examples, including:
- When to use helper files
- Naming conventions and structure
- How to reference helper files
- Best practices and validation checklist

## When Tagged

When a user tags this rule (rules-management) or asks you to create/update an Amazon Q rule:

1. **Identify the task:** Creating new rule or updating existing?
2. **Determine category:** Which category folder under `.amazonq/rules` is appropriate?
3. **Follow the process:** Use the steps above and **amazon-q-developer-rules-guide.md** for format
4. **Validate:** Run through the checklist before completion
5. **Confirm:** Show the user what was created/updated

Remember: **Always follow this guide exactly** when working with rules. Consistency is critical for maintainability.
