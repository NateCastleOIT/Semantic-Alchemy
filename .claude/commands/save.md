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
   - Briefly summarize the key changes

## Generate Commit Message

4. Automatically analyze the changes and create a comprehensive commit message following this format:

```
<type>: <short summary>

<detailed description>

<optional footer with references>
```

**Types**: feat, fix, refactor, docs, test, chore, style, perf

**Examples**:
- `feat: add element combination preview`
- `fix: resolve inventory duplication bug`
- `refactor: simplify discovery logic`
- `docs: update API documentation`

## Create Commit

5. Stage and commit the changes:
   - Add all relevant files automatically
   - Create the commit with the generated message
   - Show the commit hash and summary
   - Show the generated commit message for user's reference

## Additional Guidelines

- Be concise but thorough
- Generate comprehensive commit messages that accurately describe all changes
- Never force push without explicit user request
- If pre-commit hooks fail, show the errors and ask how to proceed
- User will manually push when ready, so don't ask about pushing
