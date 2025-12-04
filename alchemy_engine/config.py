"""
Configuration settings for the Alchemy Engine.
"""
import os

# Database settings
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'alchemy.db')

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"  # Can be changed to other models like "mistral", "qwen2.5", etc.

# Generation settings
MAX_RETRIES = 3  # How many times to retry on JSON parse errors
GENERATION_TIMEOUT = 60  # Seconds to wait for LLM response

# Combination prompt template
COMBINATION_PROMPT = """You are an ancient arcane codex that records the fundamental laws of elemental magic.

Two elements are being combined IN A SPECIFIC ORDER. The first element is the BASE, the second is the MODIFIER. Order matters - Fire modified by Water is different from Water modified by Fire.

FIRST ELEMENT (Base): {element_a_name}
Description: {element_a_description}
Tags: {element_a_tags}

SECOND ELEMENT (Modifier): {element_b_name}
Description: {element_b_description}
Tags: {element_b_tags}

Create a new element that represents {element_a_name} modified/influenced by {element_b_name}.

Respond with ONLY a valid JSON object in this exact format:
{{
  "name": "The Element Name",
  "description": "A 2-3 sentence poetic but coherent description of what this element is and what it represents",
  "tags": ["tag1", "tag2", "tag3", "tag4"],
  "visual_hint": "A single emoji that best represents this element",
  "behavior_hints": ["hint1", "hint2", "hint3"]
}}

Guidelines:
- The name should feel magical but make semantic sense
- Description should explain WHY this combination makes sense
- Tags should be single words or short phrases describing properties
- Visual hint must be a single emoji character (like 🔥, 💧, ⚡, etc.)
- Behavior hints describe what this element DOES (spreads, erupts, flows, crystallizes, etc)
- Make it feel inevitable, not random
- Consider the ORDER: base element modified by the second element
- Be creative but coherent - avoid nonsense

Return ONLY the JSON object, no other text."""
