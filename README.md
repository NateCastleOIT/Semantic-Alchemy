# Alchemy Laboratory - Semantic Element Combination System

An experimental system for generating infinite element combinations using LLM-powered semantic alchemy. Inspired by games like Infinite Craft, this creates a deterministic universe where elements combine based on meaning rather than hardcoded rules.

## Concept

This is **not a game yet** - it's a laboratory for testing the core combination engine. The goal is to build a robust semantic alchemy system that can later be integrated into a game (similar to Noita's pixel simulation, but with LLM-generated element interactions).

### Key Features

- **Order Matters**: Fire + Water ≠ Water + Fire
- **Deterministic**: Same inputs always produce the same output
- **Semantic**: Combinations are meaningful, not random
- **Infinite**: Any element can be combined with any other
- **Emergent**: Complex elements arise from simple base elements

## Project Structure

```
Combination Game/
├── alchemy_engine/          # Core engine modules
│   ├── models.py            # Element data structures
│   ├── database.py          # SQLite storage
│   ├── generator.py         # LLM integration
│   ├── engine.py            # Combination logic
│   ├── seed_data.py         # Base elements
│   ├── icon_generator.py    # Procedural icon generation
│   ├── cli.py               # Command-line interface
│   └── gui.py               # Visual GUI interface
├── data/                    # SQLite database + icon cache
├── main.py                  # CLI entry point
├── gui_main.py              # GUI entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Ollama is a tool for running local LLMs. You need it to generate element combinations.

#### Windows:

1. Download Ollama from: https://ollama.com/download
2. Run the installer
3. Ollama will start automatically in the background

#### Verify Installation:

Open a command prompt and run:
```bash
ollama --version
```

You should see version information.

### 3. Download an LLM Model

The system is configured to use **llama3.2** by default. Download it:

```bash
ollama pull llama3.2
```

This will download the model (a few GB). It only needs to be done once.

#### Alternative Models:

You can try other models by editing `alchemy_engine/config.py` and changing `OLLAMA_MODEL`:

```python
OLLAMA_MODEL = "mistral"     # Faster, smaller
OLLAMA_MODEL = "llama3.1"    # Larger, more creative
OLLAMA_MODEL = "qwen2.5"     # Better at structured output
```

Then pull the model:
```bash
ollama pull mistral
```

### 4. Run the Laboratory

You can run the laboratory in two modes:

#### Visual GUI Mode (Recommended)

```bash
python gui_main.py
```

This launches a visual interface with:
- **Discovery Journal**: Scrollable list of all discovered elements with icons
- **Combination Lab**: Drag-and-drop elements to combine them
- **Result Panel**: See your newly created elements with full details

**Controls**:
- Drag elements from the journal to the combination slots
- Mouse wheel to scroll the journal
- Press 'C' to clear combination slots
- Press ESC to quit

#### CLI Mode

```bash
python main.py
```

This launches the text-based command-line interface.

You should see:
```
Initializing Alchemy Laboratory...
Initializing base elements...
  ✓ Added: Fire
  ✓ Added: Water
  ...
Testing Ollama connection...
✓ Ollama connection successful!

===========================================
✨ ALCHEMY LABORATORY ✨
===========================================
```

## Using the Laboratory (CLI Mode)

### List Available Elements

```
> list
```

Shows all elements (base + discovered combinations).

### Combine Elements

Combine by name:
```
> combine Fire Water
```

Or by number:
```
> combine 1 2
```

The system will:
1. Check if this combination has been done before
2. If new, call the LLM to generate a result
3. Save the result permanently
4. Display the new element

**Remember: Order matters!**
- `Fire + Water` might create "Steam"
- `Water + Fire` might create "Quenching Torrent"

### View Element Details

```
> show Steam
```

or

```
> show 9
```

Shows full description, tags, visual hints, and behavior hints.

### View Lineage

See the ancestry tree of a combined element:

```
> lineage Steam
```

Shows which elements were combined to create it.

### View Statistics

```
> stats
```

Shows:
- Number of base elements
- Number of discovered combinations
- Total combinations performed

## Troubleshooting

### "Cannot connect to Ollama"

**Problem**: The CLI reports it can't connect to Ollama.

**Solutions**:
1. Make sure Ollama is installed
2. Check if Ollama is running:
   ```bash
   ollama list
   ```
3. Try starting Ollama manually (it should auto-start on Windows)
4. Verify the URL in `alchemy_engine/config.py`:
   ```python
   OLLAMA_BASE_URL = "http://localhost:11434"
   ```

### Generation Takes Too Long

**Problem**: LLM generation is slow.

**Solutions**:
1. Use a smaller/faster model like `mistral`
2. Increase timeout in `config.py`:
   ```python
   GENERATION_TIMEOUT = 120  # Increase to 2 minutes
   ```
3. Check your CPU - local LLMs are compute-intensive

### Bad/Nonsensical Generations

**Problem**: The LLM creates weird or illogical combinations.

**Solutions**:
1. Try a different model (llama3.1, qwen2.5)
2. Edit the prompt in `config.py` to be more specific
3. This is part of the experiment! Refining prompts is Phase 1's goal

### Database Issues

**Problem**: Database errors or corruption.

**Solution**: Delete the database and restart:
```bash
# Delete the database
rm data/alchemy.db  # Linux/Mac
del data\alchemy.db  # Windows

# Run main.py again - it will recreate with base elements
python main.py
```

## Database

The system uses SQLite (built into Python, no installation needed).

- **Location**: `data/alchemy.db`
- **Tables**:
  - `elements` - All elements (base + combined)
  - `combinations` - Mapping of inputs → results for deterministic caching

You can explore the database with any SQLite browser if you're curious.

## Next Steps (Future Development)

**Phase 1: Semantic Alchemy Engine** ✅
- ✅ CLI laboratory
- ✅ Test prompt engineering
- ✅ Refine generation quality
- ✅ Build up a library of interesting combinations

**Phase 2: Visual Combination Interface** ✅ (Partially Complete)
- ✅ Drag-and-drop element mixing
- ✅ Visual representation of elements (procedural icons)
- ✅ Discovery journal
- ⏳ Spell circle UI concept (future enhancement)
- ⏳ Better icon generation (AI-generated icons)

**Phase 3: Game Integration** (Future)
- Decide on gameplay (Noita-like? Roguelike? Other?)
- Implement element effects in-game
- Map semantic properties to game mechanics

## Configuration

Edit `alchemy_engine/config.py` to customize:

- **LLM Model**: `OLLAMA_MODEL`
- **Generation Timeout**: `GENERATION_TIMEOUT`
- **Max Retries**: `MAX_RETRIES`
- **Prompt Template**: `COMBINATION_PROMPT`

## Philosophy

This system follows the "Infinite Craft" principle:

> You're not building recipes. You're building a meaning engine with memory and a consistency contract.

The LLM acts as:
- Concept generator
- Naming engine
- Behavior inference model

Once a combination is discovered, it becomes **canonical truth** in your universe. This deterministic memory creates a consistent, explorable system rather than random chaos.

## License

This is an experimental project. Do with it what you will.
