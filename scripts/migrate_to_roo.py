"""
One-time migration: .cursor/rules, .cursor/skills, .cursor/commands -> .roo/
Run from repo root: python scripts/migrate_to_roo.py
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURSOR_RULES = ROOT / ".cursor" / "rules"
CURSOR_SKILLS = ROOT / ".cursor" / "skills"
CURSOR_CMD = ROOT / ".cursor" / "commands"
ROO_RULES = ROOT / ".roo" / "rules"
ROO_SKILLS = ROOT / ".roo" / "skills"
ROO_CMD = ROOT / ".roo" / "commands"


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) >= 3 and parts[0] == "":
        return parts[2].lstrip("\n")
    return text


def migrate_rules() -> None:
    if not CURSOR_RULES.is_dir():
        raise SystemExit(f"Missing {CURSOR_RULES}")
    ROO_RULES.mkdir(parents=True, exist_ok=True)
    for path in CURSOR_RULES.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(CURSOR_RULES)
        if path.name == "RULE.mdc":
            topic = path.parent.name
            out_dir = ROO_RULES / path.parent.relative_to(CURSOR_RULES)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{topic}.md"
            content = path.read_text(encoding="utf-8")
            out_file.write_text(strip_frontmatter(content), encoding="utf-8")
        else:
            if path.name in ("README.md", "README_HE.md"):
                # Roo-specific documentation; do not overwrite from `.cursor/rules/`.
                continue
            dest = ROO_RULES / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


def migrate_skills() -> None:
    if not CURSOR_SKILLS.is_dir():
        return
    ROO_SKILLS.mkdir(parents=True, exist_ok=True)
    for skill_dir in CURSOR_SKILLS.iterdir():
        if not skill_dir.is_dir():
            continue
        dest_dir = ROO_SKILLS / skill_dir.name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(skill_dir, dest_dir)
        skill_md = dest_dir / "SKILL.md"
        if skill_md.is_file():
            text = skill_md.read_text(encoding="utf-8")
            # Remove Cursor-only frontmatter line if present
            text = re.sub(
                r"^disable-model-invocation:\s*.+\n",
                "",
                text,
                flags=re.MULTILINE,
            )
            text = text.replace(
                "Trigger with **`@evaluate-with-llm-judge`**.",
                "Roo loads this skill when the request matches the `description` in SKILL.md frontmatter.",
            )
            text = text.replace(
                "Trigger with **`@splunk-instrumentation`**.",
                "Roo loads this skill when the request matches the `description` in SKILL.md frontmatter.",
            )
            text = text.replace("**`@splunk-instrumentation`**", "this skill")
            text = text.replace("**`@evaluate-with-llm-judge`**", "this skill")
            skill_md.write_text(text, encoding="utf-8")


# Slash command path -> Roo filename stem (category-name)
CMD_MAP = [
    ("testing/run-test-suite", "testing-run-test-suite"),
    ("testing/write-targeted-tests", "testing-write-targeted-tests"),
    ("testing/run-evaluation-suite", "testing-run-evaluation-suite"),
    ("monitoring/analyze-langsmith-traces", "monitoring-analyze-langsmith-traces"),
    ("monitoring/comprehensive-system-analysis", "monitoring-comprehensive-system-analysis"),
    ("monitoring/performance-analysis", "monitoring-performance-analysis"),
    ("monitoring/profile-code-bottlenecks", "monitoring-profile-code-bottlenecks"),
    ("monitoring/audit-prompt-registry-splunk", "monitoring-audit-prompt-registry-splunk"),
    ("monitoring/run-all-monitoring", "monitoring-run-all-monitoring"),
    ("agents/setup-new-agent-system", "agents-setup-new-agent-system"),
    ("agents/create-agent-node", "agents-create-agent-node"),
    ("agents/implement-agent-tool", "agents-implement-agent-tool"),
    ("agents/run-all-agents", "agents-run-all-agents"),
    ("security/security-audit", "security-security-audit"),
    ("security/analyze-audit-logs", "security-analyze-audit-logs"),
    ("review/code-review-checklist", "review-code-review-checklist"),
    ("review/final-compliance-check", "review-final-compliance-check"),
]


def extract_overview_for_description(body: str) -> str:
    m = re.search(r"## Overview\s*\n+(.+?)(?=\n## |\Z)", body, re.DOTALL)
    if m:
        line = m.group(1).strip().split("\n")[0].strip()
        if len(line) > 240:
            return line[:237] + "..."
        return line
    first = body.strip().split("\n")
    for line in first[:20]:
        line = line.strip()
        if line and not line.startswith("#"):
            if len(line) > 240:
                return line[:237] + "..."
            return line
    return "Workflow command for this repository."


def migrate_commands() -> None:
    ROO_CMD.mkdir(parents=True, exist_ok=True)
    for old_path, stem in CMD_MAP:
        src = CURSOR_CMD / f"{old_path}.md"
        if not src.is_file():
            continue
        raw = src.read_text(encoding="utf-8")
        # Replace slash references
        new_body = raw
        for o, n in CMD_MAP:
            new_body = new_body.replace(f"/{o}", f"/{n}")
        new_body = new_body.replace(".cursor/rules", ".roo/rules")
        new_body = new_body.replace(".cursor/skills", ".roo/skills")
        new_body = new_body.replace(
            "`/testing/*`",
            "testing slash commands (e.g. `/testing-run-test-suite`)",
        )
        # Description line for frontmatter
        desc = extract_overview_for_description(new_body)
        fm = f"---\ndescription: {json.dumps(desc)}\n---\n\n"
        if new_body.startswith("---"):
            # Already has frontmatter in source - strip old if any
            parts = new_body.split("---", 2)
            if len(parts) >= 3:
                new_body = parts[2].lstrip("\n")
        out = ROO_CMD / f"{stem}.md"
        out.write_text(fm + new_body.lstrip(), encoding="utf-8")

    # Human-maintained index: `.roo/commands/slash-commands-documentation.md` (do not use README.md here — it would register as `/readme`).


def patch_repo_references() -> None:
    """Update remaining references under .roo/rules after copy."""
    replacements: list[tuple[str, str]] = []
    for o, n in CMD_MAP:
        replacements.append((f"/{o}", f"/{n}"))
    replacements.append((".cursor/commands", ".roo/commands"))
    replacements.append((".cursor/rules", ".roo/rules"))
    replacements.append((".cursor/skills", ".roo/skills"))
    for path in ROO_RULES.rglob("*.md"):
        t = path.read_text(encoding="utf-8")
        orig = t
        for a, b in replacements:
            t = t.replace(a, b)
        if t != orig:
            path.write_text(t, encoding="utf-8")
    for path in ROO_SKILLS.rglob("*.md"):
        t = path.read_text(encoding="utf-8")
        orig = t
        for a, b in replacements:
            t = t.replace(a, b)
        if t != orig:
            path.write_text(t, encoding="utf-8")


def main() -> None:
    migrate_rules()
    migrate_skills()
    migrate_commands()
    patch_repo_references()


if __name__ == "__main__":
    main()
