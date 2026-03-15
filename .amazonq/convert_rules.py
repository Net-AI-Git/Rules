# One-time script: strip Cursor frontmatter and convert @ refs for Amazon Q rules.
# Run from repo root: python .amazonq/convert_rules.py

import re
from pathlib import Path

RULES_ROOT = Path(__file__).parent / "rules"

def strip_frontmatter(content: str) -> str:
    if not content.strip().startswith("---"):
        return content
    # Find second --- (end of frontmatter)
    lines = content.split("\n")
    end = 0
    seen_one = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not seen_one:
                seen_one = True
            else:
                end = i + 1
                # Skip blank line after --- if present
                if end < len(lines) and lines[end].strip() == "":
                    end += 1
                break
    return "\n".join(lines[end:]).lstrip("\n") + ("\n" if not content.endswith("\n") else "")

def convert_refs(content: str) -> str:
    # **See:** `@examples_foo.py` -> For examples see the file ... in this folder
    content = re.sub(
        r'\*\*See:\*\*\s*`@(examples_[^`]+)`',
        r'For examples see the file `\1` in this folder. When using this rule, add the relevant example file(s) to the chat context.',
        content
    )
    # **See:** `@rule-name` (other rule reference)
    content = re.sub(
        r'\*\*See:\*\*\s*`@([a-zA-Z0-9-]+(?:/[a-zA-Z0-9-]+)*)`',
        r'See rule: \1 (in .amazonq/rules)',
        content
    )
    # Standalone `@examples_xxx` (backtick-wrapped)
    content = re.sub(
        r'`@(examples_[a-zA-Z0-9_.]+)`',
        r'`\1` (in this folder; add to chat context when needed)',
        content
    )
    # See @rule-name or **See:** @rule-name (kebab-case; avoid @server. in code - no dot after)
    content = re.sub(
        r'\*\*[Ss]ee:\*\*\s+@([a-z0-9]+(?:-[a-z0-9]+)+)',
        r'See rule: \1 (in .amazonq/rules)',
        content
    )
    content = re.sub(
        r'([Ss]ee|reference|Refer to|per)\s+@([a-z0-9]+(?:-[a-z0-9]+)+)',
        r'See rule: \2 (in .amazonq/rules)',
        content
    )
    content = re.sub(
        r'\([Ss]ee\s+@([a-z0-9]+(?:-[a-z0-9]+)+)\)',
        r'(See rule: \1 in .amazonq/rules)',
        content
    )
    content = re.sub(
        r'`@([a-z0-9]+(?:-[a-z0-9]+)+)`',
        r'rule: \1 (in .amazonq/rules)',
        content
    )
    # Standalone @rule-name at end of phrase (e.g. "strategies (Splunk per @monitoring-and-observability)")
    content = re.sub(
        r'\s+@([a-z0-9]+(?:-[a-z0-9]+)+)(?=[\s.).])',
        r' (See rule: \1 in .amazonq/rules)',
        content
    )
    return content

def main():
    for path in RULES_ROOT.rglob("RULE.md"):
        content = path.read_text(encoding="utf-8")
        content = strip_frontmatter(content)
        content = convert_refs(content)
        path.write_text(content, encoding="utf-8")
        print(path.relative_to(RULES_ROOT.parent))

if __name__ == "__main__":
    main()
