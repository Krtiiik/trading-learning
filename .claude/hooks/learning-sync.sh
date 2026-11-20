#!/bin/sh
# PostToolUse hook for Bash and PowerShell: after a git commit (or merge) on main, if learning/ changed since the last
# publish of the learning site, tell Claude to rebuild it and republish the private artifact.
# The last published commit is kept in learning/.published-commit (gitignored, local to this checkout).

input=$(cat)
printf '%s' "$input" | grep -Eq '(^|[^[:alnum:]_-])git(\.exe)?([[:space:]]+-[^[:space:]]+([[:space:]]+[^-[:space:]][^[:space:]]*)?)*[[:space:]]+(commit|merge)' || exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
head=$(git rev-parse --verify -q HEAD) || exit 0
# The artifact shows main; commits on worktree branches reach it once merged into main.
[ "$(git symbolic-ref --short -q HEAD)" = main ] || exit 0
git cat-file -e "HEAD:learning/build.py" 2>/dev/null || exit 0

published=$(cat learning/.published-commit 2>/dev/null)
if [ -n "$published" ] && git cat-file -e "$published^{commit}" 2>/dev/null; then
  git diff --quiet "$published" "$head" -- learning/ ':!learning/SPEC.md' ':!learning/serve.py' && exit 0
fi

url=$(head -n 1 learning/artifact-url.txt 2>/dev/null)
msg="The learning site changed (learning/ differs from the last publish). Republish it now: \
1) run 'uv run python learning/build.py --files-json' and fix any build errors; \
2) publish with the Artifact tool: file_path learning/dist/index.html, root learning/dist, files = the printed JSON list, url $url (read the artifact first if this conversation has not published it, and pass null for paths of removed pages); \
3) write the output of 'git rev-parse HEAD' to learning/.published-commit."
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$msg"
