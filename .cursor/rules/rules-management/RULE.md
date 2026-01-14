---
globs:
  - "**/.cursor/rules/**/RULE.md"
alwaysApply: false
---

## Mandate

When creating or updating Cursor Rules, you **MUST** follow this guide strictly. This document defines the exact format, structure, and process for all rules in this repository.

## What are Cursor Rules?

Cursor Rules provide system-level instructions to Agent. They bundle prompts, scripts, and more together, making it easy to manage and share workflows across your team. Rules are stored in `.cursor/rules` and are version-controlled.

Rules are included at the start of the model context, giving the AI consistent guidance for generating code, interpreting edits, or helping with workflows.

## Directory Structure

Rules in this repository are organized by category:

```
.cursor/rules/
├── core/              # Always-applied core rules (Python standards, error handling)
├── security/          # Security and governance rules
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/      # Testing, code review, versioning
├── api/              # API-related rules
├── data/             # Data schemas, migrations
├── evaluation/       # LLM evaluation, judging, auditing
├── configuration/    # Configuration, dependency injection, prompts
└── rules-management/ # This rule (meta-rule for managing rules)
```

### Rule Folder Structure

Each rule is a **folder** containing a `RULE.md` file:

```
.cursor/rules/
  category-name/
    rule-name/
      RULE.md
```

**Important:** 
- Each rule must be in its own folder
- The folder name should be kebab-case (e.g., `core-python-standards`)
- The file inside must be named exactly `RULE.md` (capital letters)

## Rule File Format

Every `RULE.md` file **MUST** follow this structure:

### 1. Frontmatter Metadata

The file **MUST** start with YAML frontmatter between `---` markers:

```markdown
---
[metadata fields]
---

[rule content]
```

### 2. Rule Types and Frontmatter

There are 4 types of rules, each with different frontmatter requirements:

#### Type 1: Always Apply

Applied to every chat session automatically.

**Frontmatter Structure:**
```yaml
---
alwaysApply: true
---
```

**Detailed Frontmatter Instructions:**

1. **Start with `---` on the first line** (no content before it)
2. **Add `alwaysApply: true`** on the second line
   - Use lowercase `true` (not `True` or `TRUE`)
   - No quotes around `true`
   - Exactly one space after the colon: `alwaysApply: true`
3. **End with `---` on the third line** (exactly 3 dashes)
4. **Add one blank line** after the closing `---` before content starts

**Required Fields:**
- ✅ `alwaysApply: true` (required)
- ❌ `description` (MUST NOT be present)
- ❌ `globs` (MUST NOT be present)

**Common Mistakes to Avoid:**
- ❌ `alwaysApply: True` (use lowercase `true`)
- ❌ `alwaysApply: "true"` (no quotes)
- ❌ Adding `description` field
- ❌ Adding `globs` field
- ❌ Missing blank line after `---`

**Complete Example:**
```markdown
---
alwaysApply: true
---

## Core Python Standards

All Python code must follow these standards...
```

**Use when:** The rule should always be active (e.g., core coding standards, security requirements).

#### Type 2: Apply Intelligently

Applied when Agent decides it's relevant based on the description.

**Frontmatter Structure:**
```yaml
---
description: "Clear description of what this rule covers"
alwaysApply: false
---
```

**Detailed Frontmatter Instructions:**

1. **Start with `---` on the first line** (no content before it)
2. **Add `description:` field** on the second line
   - The value **MUST** be in double quotes: `"description text"`
   - Description should be clear and concise (1-2 sentences)
   - Description is used by Agent to decide if rule is relevant
3. **Add `alwaysApply: false`** on the third line
   - Use lowercase `false` (not `False` or `FALSE`)
   - No quotes around `false`
4. **End with `---` on the fourth line** (exactly 3 dashes)
5. **Add one blank line** after the closing `---` before content starts

**Required Fields:**
- ✅ `description: "..."` (required - must be in double quotes)
- ✅ `alwaysApply: false` (required)
- ❌ `globs` (MUST NOT be present)

**Field Order:**
- `description` must come before `alwaysApply`
- Both fields are required

**Common Mistakes to Avoid:**
- ❌ `description: text without quotes` (must use double quotes)
- ❌ `description: 'single quotes'` (must use double quotes)
- ❌ Missing `description` field
- ❌ Adding `globs` field
- ❌ `alwaysApply: False` (use lowercase `false`)
- ❌ Wrong field order

**Complete Example:**
```markdown
---
description: "Standards for CI/CD, Docker, Kubernetes, and infrastructure deployment"
alwaysApply: false
---

## Deployment Standards

When working on deployment...
```

**Use when:** The rule is relevant in specific contexts but not always needed (e.g., deployment standards, monitoring practices).

#### Type 3: Apply to Specific Files

Applied when working on files matching specified patterns.

**Frontmatter Structure:**
```yaml
---
globs:
  - "**/api/**/*.py"
  - "**/routes/**/*.py"
alwaysApply: false
---
```

**Detailed Frontmatter Instructions:**

1. **Start with `---` on the first line** (no content before it)
2. **Add `globs:` field** on the second line
   - Use colon after `globs`: `globs:`
   - The value is a YAML array (list)
3. **Add array items** starting from the third line
   - Each pattern on a new line
   - Start with `  - ` (2 spaces, dash, space)
   - Each pattern **MUST** be in double quotes: `"pattern"`
   - Patterns use glob syntax (e.g., `**/api/**/*.py`)
4. **Add `alwaysApply: false`** after the last glob pattern
   - Use lowercase `false`
   - No quotes around `false`
5. **End with `---` on a new line** (exactly 3 dashes)
6. **Add one blank line** after the closing `---` before content starts

**Required Fields:**
- ✅ `globs:` (required - must be a YAML array)
  - At least one pattern required
  - Each pattern in double quotes
- ✅ `alwaysApply: false` (required)
- ❌ `description` (MUST NOT be present)

**Field Order:**
- `globs` must come before `alwaysApply`
- Both fields are required

**Glob Pattern Syntax:**
- `**/` matches any directory at any depth
- `*.ext` matches files with extension
- Patterns are case-sensitive
- Use forward slashes `/` even on Windows

**Common Mistakes to Avoid:**
- ❌ `globs: "pattern"` (must be array, not string)
- ❌ `- pattern` without quotes (must use double quotes)
- ❌ `- 'pattern'` with single quotes (must use double quotes)
- ❌ Missing `alwaysApply: false`
- ❌ Adding `description` field
- ❌ Wrong indentation (must be 2 spaces for array items)
- ❌ Using backslashes `\` instead of forward slashes `/`

**Complete Example:**
```markdown
---
globs:
  - "**/tests/**/*.py"
  - "**/test_*.py"
alwaysApply: false
---

## Testing Standards

When writing test files...
```

**Use when:** The rule is only relevant for specific file types or locations (e.g., API endpoints, test files, migrations).

#### Type 4: Apply Manually

Applied only when @-mentioned in chat (e.g., `@rule-name`).

**Frontmatter Structure:**
```yaml
---
alwaysApply: false
---
```

**Detailed Frontmatter Instructions:**

1. **Start with `---` on the first line** (no content before it)
2. **Add `alwaysApply: false`** on the second line
   - Use lowercase `false` (not `False` or `FALSE`)
   - No quotes around `false`
   - Exactly one space after the colon: `alwaysApply: false`
3. **End with `---` on the third line** (exactly 3 dashes)
4. **Add one blank line** after the closing `---` before content starts

**Required Fields:**
- ✅ `alwaysApply: false` (required)
- ❌ `description` (MUST NOT be present)
- ❌ `globs` (MUST NOT be present)

**Common Mistakes to Avoid:**
- ❌ `alwaysApply: False` (use lowercase `false`)
- ❌ `alwaysApply: "false"` (no quotes)
- ❌ Adding `description` field
- ❌ Adding `globs` field
- ❌ Missing blank line after `---`

**Complete Example:**
```markdown
---
alwaysApply: false
---

## Special Audit Protocol

This rule is applied manually when needed...
```

**Use when:** The rule is rarely needed and should only be applied on demand (e.g., audit protocols, special review procedures, meta-rules like this one).

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
.cursor/rules/[category]/[rule-name]/
  RULE.md
```

### Step 4: Write Frontmatter

Based on the rule type, write the correct frontmatter following these exact specifications:

**For Always Apply:**

1. Start with `---` (3 dashes, no spaces)
2. Add `alwaysApply: true` (lowercase `true`, no quotes, one space after colon)
3. End with `---` (3 dashes, no spaces)
4. Add one blank line before content

```yaml
---
alwaysApply: true
---
```

**For Apply Intelligently:**

1. Start with `---` (3 dashes, no spaces)
2. Add `description: "Your description here"` (must be in double quotes, on its own line)
3. Add `alwaysApply: false` (lowercase `false`, no quotes, one space after colon)
4. End with `---` (3 dashes, no spaces)
5. Add one blank line before content

```yaml
---
description: "Clear, concise description of what this rule covers"
alwaysApply: false
---
```

**Important:** The description must be in double quotes and should be 1-2 sentences that clearly explain when this rule is relevant.

**For Apply to Specific Files:**

1. Start with `---` (3 dashes, no spaces)
2. Add `globs:` (colon, no value on same line)
3. Add each pattern on a new line with `  - "pattern"` (2 spaces, dash, space, pattern in double quotes)
4. Add `alwaysApply: false` (lowercase `false`, no quotes, one space after colon)
5. End with `---` (3 dashes, no spaces)
6. Add one blank line before content

```yaml
---
globs:
  - "**/pattern/**/*.ext"
  - "**/another-pattern/**/*.ext"
alwaysApply: false
---
```

**Important:** 
- `globs` must be a YAML array (list), not a string
- Each pattern must be in double quotes
- Use forward slashes `/` even on Windows
- Patterns use glob syntax with `**/` for recursive matching

**For Apply Manually:**

1. Start with `---` (3 dashes, no spaces)
2. Add `alwaysApply: false` (lowercase `false`, no quotes, one space after colon)
3. End with `---` (3 dashes, no spaces)
4. Add one blank line before content

```yaml
---
alwaysApply: false
---
```

### Step 5: Write Rule Content

- Start content immediately after frontmatter (no blank line needed, but one is fine)
- Use markdown formatting
- **Do NOT** include the main title as `# Title` - start with `## Section` or content directly
- Be clear, actionable, and specific
- Provide examples when helpful
- Reference other rules using `@rule-name` or `@filename` syntax

### Step 6: Validate Structure

Ensure:
- ✅ Folder name is kebab-case
- ✅ File is named exactly `RULE.md`
- ✅ Frontmatter is correct for the rule type
- ✅ Content follows markdown best practices
- ✅ Rule is under 500 lines (split if larger)

## Updating an Existing Rule

### Step 1: Locate the Rule

Find the rule in the appropriate category folder:
```
.cursor/rules/[category]/[rule-name]/RULE.md
```

### Step 2: Understand Current Structure

- Read the existing frontmatter
- Understand the rule type
- Note the current content structure

### Step 3: Update Content

When updating:
- **Preserve** the frontmatter format (unless changing rule type)
- **Maintain** the existing structure and style
- **Update** only the necessary sections
- **Keep** references to other rules/files intact
- **Ensure** markdown formatting is preserved

### Step 4: Update Metadata (if needed)

If changing rule type:
- Update frontmatter accordingly
- Remove/add fields as required by new type
- Ensure consistency with rule type requirements

### Step 5: Validate

After update:
- ✅ Frontmatter is still valid
- ✅ Content is properly formatted
- ✅ Rule is still under 500 lines
- ✅ All references are still valid

## Best Practices

### Content Guidelines

1. **Keep Rules Focused**
   - Each rule should cover one specific domain
   - Avoid mixing unrelated topics
   - Split large rules into multiple, composable rules

2. **Length Limit**
   - Keep rules under 500 lines
   - If a rule exceeds 500 lines, split it into multiple rules

3. **Be Actionable**
   - Provide concrete, actionable guidance
   - Avoid vague instructions
   - Include examples when helpful

4. **Reference, Don't Copy**
   - Use `@filename` to reference files instead of copying content
   - This keeps rules short and prevents staleness
   - Example: `See: @core-python-standards.md for coding standards`

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
   - Point to canonical examples instead of copying code
   - Use `@filename` references

5. **Don't Include Main Title**
   - Start with `## Section` or content directly
   - The rule name (folder name) is the title

## Examples

### Example 1: Always Apply Rule

**Location:** `.cursor/rules/core/core-python-standards/RULE.md`

```markdown
---
alwaysApply: true
---

## Mandate
You are an expert AI developer. You must strictly adhere to the following methodology and standards for all coding tasks.

## Code Quality
* **Full Type Hinting:** Use the `typing` module for all parameters and variables.
* **Function Length:** Functions **MUST NOT** exceed 20 lines of actual code.
...
```

### Example 2: Apply to Specific Files

**Location:** `.cursor/rules/api/api-documentation-standards/RULE.md`

```markdown
---
globs:
  - "**/api/**/*.py"
  - "**/routes/**/*.py"
  - "**/endpoints/**/*.py"
alwaysApply: false
---

## 1. OpenAPI/Swagger Specifications

* **Mandate:** All API endpoints must be documented using OpenAPI 3.0 specification.
...
```

### Example 3: Apply Intelligently

**Location:** `.cursor/rules/development/code-review-and-collaboration/RULE.md`

```markdown
---
description: "Standards for code review, Git workflow, and collaboration practices"
alwaysApply: false
---

## 1. PR Review Checklist

* **Code Quality:**
    * [ ] Code follows style guidelines (ruff, black).
...
```

### Example 4: Apply Manually

**Location:** `.cursor/rules/evaluation/llm-judge-protocol/RULE.md`

```markdown
---
alwaysApply: false
---

## Mandate

You are the **Supreme AI Adjudicator**. Your role is to evaluate the performance, safety, and logic of an Agentic System...
```

## Validation Checklist

Before finalizing any rule creation or update, verify:

- [ ] Folder name is kebab-case
- [ ] File is named exactly `RULE.md` (capital letters)
- [ ] Frontmatter is present and correctly formatted
- [ ] Frontmatter matches the rule type requirements:
  - [ ] Always Apply: only `alwaysApply: true`
  - [ ] Apply Intelligently: `description` + `alwaysApply: false`
  - [ ] Apply to Specific Files: `globs` array + `alwaysApply: false`
  - [ ] Apply Manually: only `alwaysApply: false`
- [ ] Content starts after frontmatter
- [ ] No main title (`# Title`) - start with sections or content
- [ ] Rule is under 500 lines
- [ ] Markdown formatting is correct
- [ ] References use `@filename` syntax
- [ ] Content is clear, actionable, and specific

## Quick Reference: Frontmatter Templates

### Always Apply

**Copy this exact template:**
```yaml
---
alwaysApply: true
---
```

**Key Points:**
- Only one field: `alwaysApply: true`
- Use lowercase `true`, no quotes
- No `description`, no `globs`

### Apply Intelligently

**Copy this exact template:**
```yaml
---
description: "Your rule description here"
alwaysApply: false
---
```

**Key Points:**
- Two fields: `description` and `alwaysApply`
- `description` must be in double quotes
- `description` comes first, then `alwaysApply: false`
- No `globs` field

### Apply to Specific Files

**Copy this exact template:**
```yaml
---
globs:
  - "**/pattern1/**/*.ext"
  - "**/pattern2/**/*.ext"
alwaysApply: false
---
```

**Key Points:**
- Two fields: `globs` (array) and `alwaysApply`
- `globs` is a YAML array (list), not a string
- Each pattern in double quotes, indented with 2 spaces and `- `
- `globs` comes first, then `alwaysApply: false`
- No `description` field

### Apply Manually

**Copy this exact template:**
```yaml
---
alwaysApply: false
---
```

**Key Points:**
- Only one field: `alwaysApply: false`
- Use lowercase `false`, no quotes
- No `description`, no `globs`

## When Tagged

When a user tags `@rules-management` or asks you to create/update a rule:

1. **Identify the task:** Creating new rule or updating existing?
2. **Determine category:** Which category folder is appropriate?
3. **Choose rule type:** Which of the 4 types fits best?
4. **Follow the process:** Use the steps above strictly
5. **Validate:** Run through the checklist before completion
6. **Confirm:** Show the user what was created/updated

Remember: **Always follow this guide exactly** when working with rules. Consistency is critical for maintainability.
