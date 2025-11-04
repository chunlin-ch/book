#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def fix_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    # Identify frontmatter region
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        return False
    frontmatter = m.group(1)
    fixed = frontmatter
    # Replace duplicated quotes around double-bracket links: ""[[...]]"" -> "[[...]]"
    fixed = re.sub(r'""\[\[([^\]]+)\]\]""', r'"[[\1]]"', fixed)
    # Also handle list items like - ""[[...]]""
    fixed = re.sub(r'\-\s+""\[\[([^\]]+)\]\]""', r'- "[[\1]]"', fixed)
    # If changed, write back
    if fixed != frontmatter:
        new_text = text.replace(frontmatter, fixed, 1)
        path.write_text(new_text, encoding='utf-8')
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_double_bracket_quotes.py <content_dir>")
        sys.exit(1)
    root = Path(sys.argv[1])
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)
    total = 0
    fixed_count = 0
    for p in root.rglob('*.md'):
        total += 1
        try:
            if fix_file(p):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {p}: {e}")
    print(f"Processed {total} files, fixed {fixed_count} files.")

if __name__ == '__main__':
    main()

