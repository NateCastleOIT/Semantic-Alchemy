# Create Pull Request

Create a pull request for the current branch.

## Pre-flight Checks

1. **Verify branch**: Run `git branch --show-current`
   - If on main/master, warn and suggest creating a feature branch

2. **Check remote**: Run `git remote -v`
   - Ensure origin is set up

3. **Check if pushed**: Run `git status`
   - If branch is not pushed, offer to push it first
   - Run: `git push -u origin <branch>`

## PR Creation

4. **Gather PR information**:
   - **Title**: Short summary of changes
   - **Description**: What changed and why
   - **Base branch**: Usually `main` or `master` (confirm with user)

5. **Compare changes**: Show commits that will be in PR:
   - Run: `git log <base-branch>..HEAD --oneline`
   - Run: `git diff <base-branch>..HEAD --stat`

6. **Create PR**:
   - If `gh` CLI is available: Use `gh pr create`
   - Otherwise: Provide the URL to create PR manually
   - Template the PR description with:
     ```
     ## Summary
     [Description of changes]

     ## Changes
     - [List key changes]

     ## Testing
     - [How this was tested]
     ```

7. **Next steps**: Remind user to:
   - Request reviewers
   - Link any related issues
   - Check CI/CD status
