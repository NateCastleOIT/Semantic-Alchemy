# Project Context: Semantic Alchemy Game

## Project Vision

Building a game with **infinite emergent combinations** of elements/spells using LLM-powered semantic generation. Inspired by:
- **Infinite Craft**: LLM-based element discovery where meaning drives combinations
- **Ball X Pit**: Power balls with stackable/evolving effects
- **Noita**: 2D pixel-simulation roguelike with complex element interactions

**Core Philosophy**: "You're not building recipes. You're building a meaning engine with memory and a consistency contract."

## Current Status (Phase 2)

### ✅ What's Been Built

We've completed the **Semantic Alchemy Engine** with both CLI and visual GUI interfaces:

**Tech Stack:**
- Python 3.x
- Ollama (local LLM inference)
- SQLite (deterministic storage)
- Pygame (visual interface)
- Pillow (procedural icon generation)
- Model: llama3.2 (configurable)

**Core Systems Implemented:**

1. **Element Data Model** (`alchemy_engine/models.py`)
   - Structured elements with name, description, tags, visual_hint, behavior_hints
   - Lineage tracking (parent_a, parent_b, combination_order)
   - Base vs. combined element distinction
   - Flexible properties dict for future expansion

2. **Database Layer** (`alchemy_engine/database.py`)
   - SQLite for persistent storage
   - Two tables: `elements` and `combinations`
   - Deterministic caching: same inputs → same output forever
   - Lineage queries and statistics

3. **LLM Generator** (`alchemy_engine/generator.py`)
   - Ollama integration via REST API
   - Structured JSON output from LLM
   - Auto-retry on parse errors (max 3 attempts)
   - Validation of required fields

4. **Combination Engine** (`alchemy_engine/engine.py`)
   - Order-aware: Fire + Water ≠ Water + Fire
   - Deterministic: results cached in database
   - Lineage tree traversal
   - Statistics tracking

5. **Seed Elements** (`alchemy_engine/seed_data.py`)
   - 8 base elements: Fire, Water, Earth, Air, Light, Shadow, Chaos, Order
   - Rich descriptions with thematic depth
   - Designed for interesting combinations

6. **CLI Interface** (`alchemy_engine/cli.py`)
   - Interactive laboratory for testing
   - Commands: list, combine, show, lineage, stats
   - User-friendly element selection (by name or number)

7. **Procedural Icon Generator** (`alchemy_engine/icon_generator.py`)
   - Generates unique visual icons for each element based on tags
   - Color mapping based on element properties (fire=red, water=blue, etc.)
   - Gradient circles with pattern overlays
   - Icon caching in `data/icons/` directory
   - Different patterns for different element types (structured, chaotic, flowing)

8. **Visual GUI Interface** (`alchemy_engine/gui.py`)
   - Pygame-based drag-and-drop interface
   - Three panel layout: Discovery Journal, Combination Lab, Result Display
   - Scrollable element list with procedurally generated icons
   - Real-time combination with visual feedback
   - 60 FPS performance

## Key Design Decisions

### 1. Order Matters
**Decision**: `combine(A, B)` produces different results than `combine(B, A)`

**Rationale**:
- More interesting combinations (Fire modified by Water vs Water modified by Fire)
- Richer semantic space to explore
- Future UI: spell circles where layer order matters

**Implementation**: Combination key is `element_a.id + "+" + element_b.id` (order-sensitive)

### 2. Deterministic Generation
**Decision**: Once a combination is generated, it's locked forever

**Rationale**:
- Creates a consistent, explorable universe
- Players discover "laws of magic" rather than random results
- Enables sharing discoveries between players
- Cache in `combinations` table prevents re-generation

**Implementation**: Check database before calling LLM; never regenerate existing combos

### 3. Structured LLM Output
**Decision**: LLM returns JSON with specific fields, not pure natural language

**Rationale**:
- Easier to parse and validate
- Ensures we get usable data (tags, behavior hints)
- Still allows creative freedom in descriptions
- Separates "flavor generation" from "mechanical interpretation"

**Implementation**: Prompt requests JSON format; Ollama's `format: "json"` parameter enforces it

**Fields Generated**:
```json
{
  "name": "Element Name",
  "description": "2-3 sentence poetic description",
  "tags": ["tag1", "tag2", "tag3"],
  "visual_hint": "appearance description",
  "behavior_hints": ["hint1", "hint2", "hint3"]
}
```

### 4. Two-Layer Design
**Decision**: Separate "flavor generation" (LLM) from "mechanical interpretation" (future)

**Current**: LLM generates flavor + hints
**Future**: Game code interprets hints into actual mechanics

**Rationale**:
- LLMs are bad at precise numbers/balance
- LLMs are great at creative concepts
- Keeps generation quality high
- Allows mechanical tuning without regenerating

**Example Flow**:
```
LLM generates: "spreads", "consumes", "radiates"
↓
Game interprets: area_damage=true, dot_effect=fire, aoe_radius=3
```

### 5. No Fusion/Evolution Distinction Yet
**Decision**: Only one type of combination for Phase 1

**Rationale**:
- Simplifies testing
- Can add distinction later (player choice or LLM decision)
- Current system supports both conceptually

**Future Options**:
- Player chooses fusion vs evolution
- LLM decides based on semantic similarity
- Different prompts for each type

## Technical Architecture

```
┌─────────────────────────────────────┐
│  CLI Interface (cli.py)             │
│  - User interaction                 │
│  - Display formatting               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Alchemy Engine (engine.py)         │
│  - Combination logic                │
│  - Cache checking                   │
│  - Lineage tracking                 │
└──────┬──────────────────────┬───────┘
       │                      │
       ▼                      ▼
┌─────────────┐      ┌────────────────┐
│ Generator   │      │ Database       │
│ (Ollama)    │      │ (SQLite)       │
│             │      │                │
│ - Prompts   │      │ - Elements     │
│ - JSON      │      │ - Combos       │
│ - Validate  │      │ - Lineage      │
└─────────────┘      └────────────────┘
```

## LLM Prompt Strategy

**Current Prompt** (in `config.py`):
- Emphasizes ORDER: "Base element modified by second element"
- Requests specific JSON format
- Guidelines for coherence ("make it feel inevitable, not random")
- Encourages poetic but logical descriptions

**Key Insight**: Frame LLM as "ancient arcane codex recording laws of magic" rather than "generator making up random stuff"

## Database Schema

```sql
-- All elements (base + combinations)
CREATE TABLE elements (
    id TEXT PRIMARY KEY,              -- UUID
    name TEXT NOT NULL,
    description TEXT,
    tags TEXT,                        -- JSON array
    visual_hint TEXT,
    behavior_hints TEXT,              -- JSON array
    is_base BOOLEAN,
    parent_a TEXT,                    -- FK to elements.id
    parent_b TEXT,                    -- FK to elements.id
    combination_order TEXT,           -- "id_a+id_b"
    created_at TEXT,                  -- ISO timestamp
    properties TEXT                   -- JSON for future use
);

-- Deterministic cache
CREATE TABLE combinations (
    combo_key TEXT PRIMARY KEY,       -- "id_a+id_b"
    result_id TEXT,                   -- FK to elements.id
    created_at TEXT
);
```

## What's NOT Built Yet

### Immediate Needs:
- [ ] Ollama installation complete (user currently installing)
- [ ] Test first combinations
- [ ] Refine prompts based on quality of outputs

### Future (Phase 2+):
- [ ] Visual combination interface (drag-drop, spell circles)
- [ ] Actual gameplay implementation
- [ ] Element effect → game mechanic mapping
- [ ] Sprite/visual representation of elements
- [ ] Sound effects
- [ ] Game loop (roguelike? Noita-like? TBD)

## Key Learnings & Notes

### Why Not Unity/Godot/Unreal?
**User's Request**: Avoid learning a full game engine

**Solution**:
- Phase 1: Pure Python CLI (no engine needed)
- Phase 2: Could use Pygame (library, not engine)
- Phase 3: Evaluate if engine needed based on scope

**Rationale**: Build the core system first, game wrapper later

### Why Local LLM (Ollama)?
**Alternatives Considered**: OpenAI API, Anthropic API, local transformers

**Chosen**: Ollama + llama3.2

**Reasons**:
- No API costs (important for experimentation)
- Easy setup (single installer)
- Good quality models available
- REST API (simple integration)
- Can switch models easily

**Tradeoffs**:
- Requires decent CPU/RAM
- Slower than cloud APIs
- Quality varies by model

### Why SQLite?
**Alternatives**: JSON files, PostgreSQL, MongoDB

**Chosen**: SQLite

**Reasons**:
- Built into Python
- No server setup
- Fast for local data
- Relational model fits element relationships
- Easy to inspect/debug
- Can export/import easily

## Development Phases (Planned)

### Phase 1: Semantic Alchemy Engine ✅ (Current)
**Goal**: Build and test the combination generation system

**Tasks**:
- ✅ Core engine architecture
- ✅ Database layer
- ✅ LLM integration
- ✅ CLI interface
- 🔄 Ollama setup (in progress)
- ⏳ Test combinations and refine prompts
- ⏳ Build library of interesting elements

**Success Criteria**:
- Combinations feel "inevitable, not random"
- Same inputs always give same outputs
- Can discover 50+ interesting combinations
- Prompts produce coherent results

### Phase 2: Visual Combination Lab
**Goal**: Replace CLI with visual interface

**Ideas**:
- Drag-drop element mixing
- Visual representation of elements (sprites/icons)
- Spell circle UI concept (layers matter)
- Discovery journal
- Share/export combinations

**Tech**: Pygame or simple web UI (HTML/Canvas)

### Phase 3: Game Integration
**Goal**: Decide on and implement actual gameplay

**Open Questions**:
- What's the core gameplay loop?
- Noita-like pixel simulation?
- Roguelike spell crafting?
- Puzzle game?
- Something else?

**Key**: Element effects must map to game mechanics

**Challenge**: How do "behavior_hints" become actual behaviors?

### Phase 4: Polish & Expansion
- Multiplayer discovery sharing?
- Balance and tuning
- Content expansion
- Visual/audio polish

## Important Files

- `PROJECT_CONTEXT.md` - This file (read first!)
- `README.md` - Setup instructions and user guide
- `gui_main.py` - Visual GUI entry point ⭐ NEW
- `main.py` - CLI entry point
- `alchemy_engine/config.py` - Configuration (LLM model, prompts, settings)
- `alchemy_engine/seed_data.py` - Base elements definitions
- `alchemy_engine/gui.py` - Pygame visual interface ⭐ NEW
- `alchemy_engine/icon_generator.py` - Procedural icon generation ⭐ NEW

## Common Tasks for Future Sessions

### Launch Visual GUI
```bash
python gui_main.py
```
Then drag elements from the journal to combine them!

### View Current Combinations (CLI)
```bash
python main.py
> list
> show ElementName
> lineage ElementName
```

### Change LLM Model
Edit `alchemy_engine/config.py`:
```python
OLLAMA_MODEL = "mistral"  # or "llama3.1", "qwen2.5", etc.
```

### Modify Prompt
Edit `COMBINATION_PROMPT` in `alchemy_engine/config.py`

### Reset Database
```bash
rm data/alchemy.db  # Delete database
python main.py      # Recreates with base elements
```

### Add New Base Elements
Edit `alchemy_engine/seed_data.py` and add to `get_base_elements()`

## Design Philosophy Reminders

From the Infinite Craft analysis:

> **"Infinite Craft is not really: 'Water + Fire = Steam'. It is: 'Generate an outcome that makes sense to a human.'"**

Key principles:
1. **Semantic alchemy** - Meaning drives mechanics, not lookup tables
2. **Deterministic memory** - Same inputs → same outputs (builds trust)
3. **First discovery magic** - New combinations feel like discoveries
4. **Language-driven** - Let weird/unexpected results exist if coherent
5. **Narrative-first outputs** - Ask "What IS this spell?" not "What does it do?"
6. **Consistency over realism** - Internal logic matters, not physics

## User Preferences & Context

- **Technical Background**: Python, JavaScript/TypeScript
- **Platform**: Desktop app (Windows)
- **Development Approach**: Hybrid (engine first, gameplay later)
- **LLM Preference**: Local models (Ollama)
- **No interest in**: Learning Unity/Godot/Unreal
- **Inspiration**: Infinite Craft's semantic generation + Noita's emergent interactions

## Next Immediate Steps

### Phase 1 & 2 Complete! ✅
1. ✅ Complete Ollama installation
2. ✅ Download llama3.2 model (`ollama pull llama3.2`)
3. ✅ Test CLI with first combinations
4. ✅ Build visual GUI with drag-and-drop
5. ✅ Implement procedural icon generation
6. ✅ Create discovery journal

### GUI Improvements Needed (Phase 2 Polish)
- **UX Tweaks**: Interface needs refinement (user noted "some tweaks")
  - Possible improvements to consider:
    - Better visual feedback when dragging
    - Animation when creating new elements
    - Improved scrolling behavior in journal
    - Better layout/spacing of elements
    - Add element search/filter
    - Show "NEW!" indicator for fresh discoveries
    - Sound effects (optional)
    - Better color schemes/visual polish

### Future Enhancements
- Experiment with different combinations to build element library
- Evaluate generation quality and refine prompts if needed
- Document interesting emergent results
- Consider AI-generated icons (Stable Diffusion) vs procedural
- Implement spell circle UI concept

## Questions to Revisit Later

- Should we add fusion/evolution distinction?
- How to handle "bad" generations? (player rejection? manual curation?)
- What's the eventual gameplay loop?
- How to visualize spell circles?
- Should element effects be emergent or have some base rules?
- Multiplayer discovery sharing?
- How to balance infinite combinations with game balance?

---

**Last Updated**: 2025-11-30
**Current Status**: Phase 2 complete! Visual GUI with drag-and-drop and procedural icons working. Needs UX polish/tweaks before Phase 3.

## How to Run

**Visual GUI (Recommended)**:
```bash
python gui_main.py
```

**CLI Mode**:
```bash
python main.py
```

**First time setup**:
```bash
pip install -r requirements.txt
ollama pull llama3.2
```
