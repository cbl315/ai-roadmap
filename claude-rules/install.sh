#!/bin/bash
# Install Claude Code global rules from this repo
# Usage: bash claude-rules/install.sh

set -e

RULES_DIR="$HOME/.claude/rules"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$RULES_DIR"

for file in "$SOURCE_DIR"/*.md; do
    name=$(basename "$file")
    cp "$file" "$RULES_DIR/$name"
    echo "Installed: $name"
done

echo ""
echo "Done! Rules installed to $RULES_DIR"
echo "Restart Claude Code for changes to take effect."
