# Review Recent Changes

Review recent commits and current changes in the repository.

## What to Show

1. **Current branch**: Run `git branch --show-current`

2. **Recent commits**: Run `git log --oneline -10 --graph --all`
   - Show last 10 commits with graph visualization

3. **Current changes**: Run `git status`
   - Show modified, staged, and untracked files

4. **Detailed diff**: If there are uncommitted changes:
   - Run `git diff --stat` for summary
   - Ask if user wants to see full diff

5. **Branch comparison**: Ask user if they want to compare with another branch
   - If yes: `git diff <branch>..HEAD --stat`

## Summary

Provide a brief summary:
- Number of commits ahead/behind remote
- Number of modified/untracked files
- Overall project status
