# Save Changes (Smart Commit)

You are helping create a git commit with guardrails and best practices.

## Safety Checks

1. **Check current branch**: Run `git branch --show-current`
   - If branch is `main` or `master`, STOP and warn the user:
     "⚠️ You're on the {branch} branch. It's recommended to work on feature branches. Do you want to continue anyway?"
   - Wait for user confirmation before proceeding

2. **Check for uncommitted changes**: Run `git status`
   - If no changes, inform user and stop
   - If there are changes, show them briefly

## Review Changes

3. Show the user what will be committed:
   - Run `git diff --stat` to show file summary
   - Run `git diff` to show detailed changes (if reasonable size)
   - List any untracked files

## Commit Message Template

4. Ask the user for commit details and suggest following this format:

```
<type>: <short summary>

<optional detailed description>

<optional footer with references>
```

**Types**: feat, fix, refactor, docs, test, chore, style, perf

**Examples**:
- `feat: add element combination preview`
- `fix: resolve inventory duplication bug`
- `refactor: simplify discovery logic`
- `docs: update API documentation`

5. After gathering information, create a well-formatted commit message

## Create Commit

6. Stage and commit the changes:
   - Add files as appropriate (ask if there are many untracked files)
   - Create the commit with the formatted message
   - Show the commit hash and summary

## Push Option

7. Ask the user: "Would you like to push these changes to remote?"
   - If yes, run `git push` (or `git push -u origin <branch>` if needed)
   - If no, remind them they can push later with `git push`

## Additional Guidelines

- Be concise but thorough
- If the user wants to commit specific files only, respect that
- Never force push without explicit user request
- If pre-commit hooks fail, show the errors and ask how to proceed
