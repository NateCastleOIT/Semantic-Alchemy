# Developer Notes - Quick Reference

## Quick Start (For Future Sessions)

1. **Read**: `PROJECT_CONTEXT.md` first for full context
2. **Check**: Ollama is running (`ollama list`)
3. **Run**: `python main.py`

## Project Structure

```
alchemy_engine/
├── models.py       # Element dataclass, core data structures
├── database.py     # SQLite operations (save/load/cache)
├── generator.py    # LLM/Ollama integration
├── engine.py       # Combination logic, lineage tracking
├── seed_data.py    # Base elements (Fire, Water, etc.)
├── cli.py          # Command-line interface
└── config.py       # Settings, prompts, LLM model
```

## Common Development Tasks

### Test a Combination
```bash
python main.py
> combine Fire Water
```

### Change LLM Model
Edit `config.py`:
```python
OLLAMA_MODEL = "mistral"  # or llama3.1, qwen2.5, etc.
```
Then: `ollama pull mistral`

### Modify Generation Prompt
Edit `COMBINATION_PROMPT` in `config.py`

### Add Base Elements
Edit `seed_data.py` → `get_base_elements()` list

### Reset Everything
```bash
rm data/alchemy.db
python main.py  # Recreates fresh database
```

### Inspect Database
```bash
sqlite3 data/alchemy.db
> SELECT name FROM elements;
> SELECT * FROM combinations;
```

### Export All Elements
Use CLI:
```
> list  # Shows all elements with IDs
```

Or query database:
```python
from alchemy_engine import AlchemyDatabase
db = AlchemyDatabase()
elements = db.get_all_elements()
for e in elements:
    print(f"{e.name}: {e.description}")
```

## Key Files to Edit

### To change behavior/mechanics:
- `engine.py` - Core combination logic
- `generator.py` - LLM calling and parsing

### To change prompts/settings:
- `config.py` - All configuration

### To change UI/commands:
- `cli.py` - CLI interface

### To add/modify base elements:
- `seed_data.py` - Seed element definitions

### To change data structure:
- `models.py` - Element dataclass
- `database.py` - Schema (need to recreate DB after changes)

## Debugging

### LLM Not Responding
```python
# Test Ollama directly:
import requests
r = requests.get("http://localhost:11434/api/tags")
print(r.json())  # Should show available models
```

### Bad Generations
1. Check prompt in `config.py`
2. Try different model
3. Increase `MAX_RETRIES`
4. Check Ollama logs

### Database Issues
```bash
# Check if database exists
ls data/

# Check tables
sqlite3 data/alchemy.db ".schema"

# Recreate
rm data/alchemy.db && python main.py
```

## Testing New Prompts

1. Edit `COMBINATION_PROMPT` in `config.py`
2. Delete `data/alchemy.db` (fresh start)
3. Run `python main.py`
4. Try same combinations with new prompt
5. Compare quality

## Performance Notes

- **Generation time**: 5-30 seconds per combination (depends on model/CPU)
- **Caching**: Second request for same combo is instant (database lookup)
- **Database size**: Grows ~1KB per element

## Code Style

- Type hints used throughout
- Docstrings for public methods
- Config in `config.py`, not hardcoded
- Database operations isolated in `database.py`
- LLM operations isolated in `generator.py`

## Error Handling

- `GenerationError`: LLM failed after retries
- `ValueError`: Element not found
- `JSONDecodeError`: Auto-retried (up to MAX_RETRIES)

## Current Limitations

- No GUI (CLI only)
- No actual game mechanics yet
- No visual representation of elements
- Single-user (no multiplayer)
- No undo/manual rejection of bad generations
- No export/import of elements

## Future TODOs (Not Implemented Yet)

- [ ] Visual combination interface
- [ ] Element sprites/icons
- [ ] Spell circle UI
- [ ] Gameplay integration
- [ ] Mechanical interpretation layer
- [ ] Balance/tuning system
- [ ] Export/import functionality
- [ ] Manual element editing
- [ ] Combination history/timeline
- [ ] Element rarity/tiers
- [ ] "First discovery" tracking

## Dependencies

```
requests>=2.31.0  # For Ollama API calls
# SQLite: built into Python
# UUID: built into Python
```

## Ollama Commands

```bash
# List installed models
ollama list

# Download a model
ollama pull llama3.2

# Test a model
ollama run llama3.2 "Hello"

# Check if running
curl http://localhost:11434/api/tags

# View model details
ollama show llama3.2
```

## Useful SQL Queries

```sql
-- All combinations with parent names
SELECT
    e.name as result,
    p1.name as parent_a,
    p2.name as parent_b
FROM elements e
LEFT JOIN elements p1 ON e.parent_a = p1.id
LEFT JOIN elements p2 ON e.parent_b = p2.id
WHERE e.is_base = 0;

-- Most used elements in combinations
SELECT
    e.name,
    COUNT(*) as usage_count
FROM combinations c
JOIN elements e ON (c.combo_key LIKE e.id || '+%' OR c.combo_key LIKE '%+' || e.id)
GROUP BY e.name
ORDER BY usage_count DESC;

-- Elements by creation date
SELECT name, created_at
FROM elements
ORDER BY created_at DESC;
```

## Git Ignore

Already set up in `.gitignore`:
- `data/` (database is user-specific, don't commit)
- `__pycache__/` (Python bytecode)
- IDE files

## Performance Optimization Ideas (Future)

- Batch generation (queue multiple combinations)
- Streaming LLM responses
- Cached embeddings for semantic similarity
- Pre-generate common combinations
- Use smaller/faster models for simple combos
- GPU acceleration for local LLM

---

**Remember**: Read `PROJECT_CONTEXT.md` for the full picture! This is just quick reference for development tasks.
