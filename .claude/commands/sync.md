# Sync with Remote

Synchronize the current branch with the remote repository.

## Steps

1. **Check current branch**: Run `git branch --show-current`

2. **Check git status**: Run `git status`
   - If there are uncommitted changes, warn the user:
     "⚠️ You have uncommitted changes. You can either:
     - Commit them first (use `/save`)
     - Stash them temporarily
     - Continue anyway (may cause conflicts)"
   - Ask user how to proceed

3. **Fetch latest changes**: Run `git fetch origin`

4. **Pull changes**:
   - Ask user: "How would you like to sync?"
     - Option 1: `git pull` (merge)
     - Option 2: `git pull --rebase` (rebase)
   - Execute their choice

5. **Handle conflicts**: If conflicts occur, show them and guide resolution

6. **Show summary**: Display what changed (commits pulled, files updated)
