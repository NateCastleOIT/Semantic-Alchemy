# Run Tests

Run the test suite for both backend and frontend.

## Test Execution

1. **Ask user what to test**:
   - All (both backend and frontend)
   - Backend only (Python tests)
   - Frontend only (React tests)
   - Specific test file/pattern

2. **Backend Tests** (if selected):
   - Check for pytest or unittest
   - Run: `python -m pytest` or appropriate test command
   - Show results with coverage if available

3. **Frontend Tests** (if selected):
   - Navigate to frontend directory
   - Run: `npm test` or `npm run test`
   - Show results

4. **Summary**:
   - Report pass/fail status
   - Highlight any failures
   - If failures exist, ask if user wants to see details or fix them

## Additional Options

- Offer to run linters (flake8, eslint) if tests pass
- Suggest running with coverage: `pytest --cov`
- For frontend: offer to run `npm run build` to check for build errors
