"""
LLM-powered element generator using Ollama.
"""
import json
import requests
from typing import Optional
from .models import Element
from .spell_circle_generator import SpellCircleGenerator
from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    COMBINATION_PROMPT,
    MAX_RETRIES,
    GENERATION_TIMEOUT
)


class GenerationError(Exception):
    """Raised when element generation fails."""
    pass


class ElementGenerator:
    """Handles LLM-based generation of new elements."""

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL
    ):
        """Initialize the generator with Ollama connection details."""
        self.base_url = base_url
        self.model = model
        self.generate_url = f"{base_url}/api/generate"
        self.spell_circle_gen = SpellCircleGenerator()

    def test_connection(self) -> bool:
        """Test if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def generate_combination(
        self,
        element_a: Element,
        element_b: Element
    ) -> Element:
        """
        Generate a new element from combining two elements.

        Uses the LLM to create a semantically meaningful combination.
        Order matters: Fire + Water != Water + Fire

        Args:
            element_a: The base element
            element_b: The modifying element

        Returns:
            A new Element representing the combination

        Raises:
            GenerationError: If generation fails after all retries
        """
        # Build the prompt
        prompt = COMBINATION_PROMPT.format(
            element_a_name=element_a.name,
            element_a_description=element_a.description,
            element_a_tags=", ".join(element_a.tags),
            element_b_name=element_b.name,
            element_b_description=element_b.description,
            element_b_tags=", ".join(element_b.tags)
        )

        # Try generation with retries
        for attempt in range(MAX_RETRIES):
            try:
                response_data = self._call_ollama(prompt)
                element_data = self._parse_response(response_data)

                # Create the new element
                new_element = Element(
                    name=element_data["name"],
                    description=element_data["description"],
                    tags=element_data["tags"],
                    visual_hint="",  # Will be generated as spell circle
                    behavior_hints=element_data["behavior_hints"],
                    is_base=False,
                    parent_a=element_a.id,
                    parent_b=element_b.id,
                    combination_order=f"{element_a.id}+{element_b.id}"
                )

                # Generate unique spell circle incorporating parent patterns
                spell_circle_svg = self.spell_circle_gen.generate(
                    new_element,
                    parent_a=element_a,
                    parent_b=element_b
                )
                new_element.visual_hint = spell_circle_svg

                return new_element

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"  ⚠ Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
                if attempt == MAX_RETRIES - 1:
                    raise GenerationError(
                        f"Failed to generate valid element after {MAX_RETRIES} attempts"
                    )
                continue

        raise GenerationError("Generation failed unexpectedly")

    def _call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"  # Request JSON format
        }

        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=GENERATION_TIMEOUT
            )
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.RequestException as e:
            raise GenerationError(f"Ollama API error: {e}")

    def _parse_response(self, response_text: str) -> dict:
        """
        Parse and validate the LLM's JSON response.

        Expected format:
        {
            "name": "Element Name",
            "description": "...",
            "tags": ["tag1", "tag2", ...],
            "visual_hint": "...",
            "behavior_hints": ["hint1", "hint2", ...]
        }
        """
        # Try to parse JSON
        data = json.loads(response_text)

        # Validate required fields
        required_fields = ["name", "description", "tags", "visual_hint", "behavior_hints"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Validate types
        if not isinstance(data["tags"], list):
            raise ValueError("tags must be a list")
        if not isinstance(data["behavior_hints"], list):
            raise ValueError("behavior_hints must be a list")

        # Ensure at least some content
        if len(data["name"].strip()) == 0:
            raise ValueError("name cannot be empty")
        if len(data["description"].strip()) == 0:
            raise ValueError("description cannot be empty")
        if len(data["tags"]) == 0:
            raise ValueError("tags cannot be empty")
        if len(data["behavior_hints"]) == 0:
            raise ValueError("behavior_hints cannot be empty")

        return data
