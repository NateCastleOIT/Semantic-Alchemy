# Clean Build Artifacts

Clean up build artifacts, cache files, and temporary files from the project.

## Safety Check

1. **Show what will be removed** (dry run):
   - Python: `__pycache__`, `*.pyc`, `.pytest_cache`, `*.egg-info`
   - Frontend: `node_modules`, `dist`, `build`, `.vite` cache
   - Database: `*.db-journal` (but NOT `*.db` unless user confirms)
   - Other: `.DS_Store`, `Thumbs.db`, temp files

2. **Ask for confirmation**:
   - List all directories/files that will be deleted
   - Get explicit user confirmation

## Cleaning Steps

3. **Python cleanup**:
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   find . -type d -name "*.egg-info" -exec rm -rf {} +
   rm -rf .pytest_cache
   ```

4. **Frontend cleanup**:
   ```bash
   cd frontend && rm -rf node_modules dist build .vite
   ```
   - Ask if they want to reinstall: `npm install`

5. **Git cleanup** (optional):
   - Offer to run `git clean -xdf` (removes all untracked files)
   - ⚠️ WARNING: This is destructive, require explicit confirmation

6. **Summary**: Show disk space freed and what was removed

## Post-cleanup

7. **Verify project still works**:
   - Suggest running `/test` to ensure nothing broke
   - Remind to reinstall dependencies if needed
