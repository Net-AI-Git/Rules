# Amazon Q Developer Rules Guide

This guide defines how to write and organize project rules for Amazon Q Developer. Use it when creating or updating rules in `.amazonq/rules`.

## Purpose

Rules in Amazon Q Developer are Markdown files that describe coding standards and best practices. They are automatically loaded as context when chatting with Amazon Q in the project, so the assistant follows your team's conventions without repeating instructions every time.

## Location and File Format

- **Location:** All rules live under `project-root/.amazonq/rules`.
- **File type:** Markdown only (`.md`). Amazon Q does not use `.mdc` or YAML frontmatter.
- **File names:** Any descriptive name (e.g. `core-python-standards.md`, `monitoring.md`).
- **Subdirectories:** Supported. You can organize by category (e.g. `.amazonq/rules/core/`, `.amazonq/rules/agents/`).

## Recommended Rule Structure

Amazon Q does not require a fixed format, but this structure works well:

- **# Rule Name** – Clear title for the rule.
- **## Purpose** – Why the rule exists; helps the model apply it correctly in edge cases.
- **## Instructions** – Specific, actionable directives (bullets or numbered list). Use consistent formatting; you can add optional IDs for traceability (e.g. `(ID: CHECK_MONITORING)`).
- **## Priority** – One of: Critical | High | Medium | Low. Use when multiple rules might apply so Q can resolve conflicts.
- **## Error Handling** – What to do when things go wrong (e.g. missing file, ambiguous case). Fallback behavior keeps the assistant helpful.

## What Not to Include

- **No YAML frontmatter** – Do not use `---` blocks with `alwaysApply`, `description`, or `globs`. Amazon Q does not use them.
- **No long code blocks in the rule** – Do not paste large code examples into the rule file. Point to example files instead.

## Code Examples and Helper Files

- **Do not embed long code snippets** in the rule Markdown. Keep rules focused on guidance.
- **Use example files** in the same folder as the rule (e.g. `examples_*.py`, `examples_*.md`). Name them clearly (e.g. `examples_server.py`, `examples_client.py`).
- **Reference them in the rule** with text like: "For examples see the file `examples_<name>.<ext>` in this folder. When using this rule, add the relevant example file(s) to the chat context."
- **User workflow:** The user can tag the rule file together with the desired example file(s) in the chat to give Amazon Q full context. Amazon Q also has workspace context and can see project files, including under `.amazonq/rules`.

## Loading and Toggling Rules

- When you first use Amazon Q in the project, it scans `.amazonq/rules` and loads applicable `.md` rules.
- Rules are re-evaluated per request and updates to rule files are picked up during the session.
- In the IDE chat, you can use the Rules control to turn individual rules on or off for the current conversation.

## Summary

- Store rules in `.amazonq/rules` as `.md` files.
- Use the structure: Purpose, Instructions, Priority, Error Handling.
- Do not use frontmatter; do not embed long code in the rule.
- Point to example files in the same folder and have users add them to context when needed.
