# Reference rules (commands & skills only)

Rules in this tree are **authoritative specs** for Cursor **Commands** (`.cursor/commands/`) and **Skills** (`.cursor/skills/`).

**Do not** load them manually with `@rule-name` in chat unless you have a rare debugging need. Prefer invoking the command or skill that applies them (for example `@splunk-instrumentation`, `@evaluate-with-llm-judge`).

Folder layout mirrors the original category (`evaluation/`, `security/`) so paths stay predictable.
