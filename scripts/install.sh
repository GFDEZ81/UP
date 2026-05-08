#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL=""
CATEGORIES=()

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Install UP agents to a supported AI coding tool.

Options:
  --tool <name>       Target tool to install agents for (required)
                      Supported: claude-code
  --category <name>   Install only a specific category (repeatable)
                      Available: engineering, design, data
                      Default: all categories
  -h, --help          Show this help message

Examples:
  $(basename "$0") --tool claude-code
  $(basename "$0") --tool claude-code --category engineering
  $(basename "$0") --tool claude-code --category engineering --category design
EOF
}

die() {
  echo "error: $*" >&2
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      [[ -n "${2-}" ]] || die "--tool requires a value"
      TOOL="$2"
      shift 2
      ;;
    --category)
      [[ -n "${2-}" ]] || die "--category requires a value"
      CATEGORIES+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

[[ -n "$TOOL" ]] || { usage; exit 1; }

# Resolve install target
case "$TOOL" in
  claude-code)
    AGENTS_DIR="${HOME}/.claude/agents"
    ;;
  *)
    die "unsupported tool: '$TOOL'. Supported tools: claude-code"
    ;;
esac

# Default to all categories if none specified
if [[ ${#CATEGORIES[@]} -eq 0 ]]; then
  while IFS= read -r -d '' dir; do
    category="$(basename "$dir")"
    # Skip hidden dirs and non-category dirs
    [[ "$category" != scripts ]] && CATEGORIES+=("$category")
  done < <(find "$REPO_ROOT" -maxdepth 1 -mindepth 1 -type d -not -name '.*' -not -name scripts -print0 | sort -z)
fi

# Validate categories
for category in "${CATEGORIES[@]}"; do
  [[ -d "$REPO_ROOT/$category" ]] || die "category not found: '$category' (looked in $REPO_ROOT/$category)"
done

# Install
mkdir -p "$AGENTS_DIR"

installed=0
for category in "${CATEGORIES[@]}"; do
  src_dir="$REPO_ROOT/$category"
  count=0
  while IFS= read -r -d '' file; do
    filename="$(basename "$file")"
    dest="$AGENTS_DIR/$filename"
    cp "$file" "$dest"
    echo "  installed: $filename -> $dest"
    (( count++ )) || true
    (( installed++ )) || true
  done < <(find "$src_dir" -maxdepth 1 -name '*.md' -print0 | sort -z)
  echo "[$category] $count agent(s) installed"
done

echo ""
echo "Done. $installed agent(s) installed to $AGENTS_DIR"
echo ""
echo "Activate in Claude Code:"
echo "  \"Hey Claude, activate <agent-name> mode and ...\""
echo ""
echo "Available agents:"
for category in "${CATEGORIES[@]}"; do
  echo "  [$category]"
  while IFS= read -r -d '' file; do
    name="$(basename "$file" .md)"
    echo "    - $name"
  done < <(find "$REPO_ROOT/$category" -maxdepth 1 -name '*.md' -print0 | sort -z)
done
