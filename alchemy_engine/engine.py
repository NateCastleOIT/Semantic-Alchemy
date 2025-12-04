"""
Core alchemy engine: Handles element combinations.
"""
from .models import Element
from .database import AlchemyDatabase
from .generator import ElementGenerator, GenerationError
from datetime import datetime


class AlchemyEngine:
    """
    The core alchemy system.

    Handles combining elements with deterministic caching.
    Order matters: Fire + Water != Water + Fire
    """

    def __init__(
        self,
        database: AlchemyDatabase,
        generator: ElementGenerator
    ):
        """Initialize the engine with database and generator."""
        self.db = database
        self.generator = generator

    def combine(
        self,
        element_a: Element,
        element_b: Element,
        verbose: bool = True
    ) -> Element:
        """
        Combine two elements to create a new one.

        Order matters: the result of A+B is different from B+A.
        Results are deterministic: the same combination always produces
        the same result.

        Args:
            element_a: The first (base) element
            element_b: The second (modifier) element
            verbose: Whether to print status messages

        Returns:
            The resulting element (either cached or newly generated)

        Raises:
            GenerationError: If generation fails
        """
        # Create deterministic combination key (order-sensitive)
        combo_key = f"{element_a.id}+{element_b.id}"

        # Check if this combination has been done before
        existing = self.db.get_combination(combo_key)
        if existing:
            if verbose:
                print(f"\n✓ Found existing combination: {existing.name}")
            return existing

        # Generate new element
        if verbose:
            print(f"\n⚗ Combining {element_a.name} + {element_b.name}...")
            print("  Calling LLM...")

        new_element = self.generator.generate_combination(element_a, element_b)

        # Save to database
        self.db.save_element(new_element)
        self.db.save_combination(
            combo_key,
            new_element.id,
            datetime.now().isoformat()
        )

        if verbose:
            print(f"  ✨ Created: {new_element.name}")

        return new_element

    def get_element_by_id(self, element_id: str) -> Element:
        """Get an element by ID."""
        element = self.db.get_element(element_id)
        if not element:
            raise ValueError(f"Element with ID {element_id} not found")
        return element

    def get_element_by_name(self, name: str) -> Element:
        """Get an element by name."""
        element = self.db.get_element_by_name(name)
        if not element:
            raise ValueError(f"Element '{name}' not found")
        return element

    def list_all_elements(self) -> list[Element]:
        """Get all elements."""
        return self.db.get_all_elements()

    def list_base_elements(self) -> list[Element]:
        """Get only base elements."""
        return self.db.get_base_elements()

    def get_lineage(self, element: Element, depth: int = 0) -> str:
        """
        Get a textual representation of an element's lineage tree.

        Args:
            element: The element to trace
            depth: Current recursion depth (for indentation)

        Returns:
            Formatted string showing the element's ancestry
        """
        indent = "  " * depth
        lines = [f"{indent}{element.name}"]

        if element.parent_a and element.parent_b:
            parent_a = self.db.get_element(element.parent_a)
            parent_b = self.db.get_element(element.parent_b)

            if parent_a and parent_b:
                lines.append(f"{indent}├─ Base: {parent_a.name}")
                if parent_a.parent_a:
                    lines.append(self.get_lineage(parent_a, depth + 1))

                lines.append(f"{indent}└─ Modifier: {parent_b.name}")
                if parent_b.parent_a:
                    lines.append(self.get_lineage(parent_b, depth + 1))

        return "\n".join(lines)

    def get_stats(self) -> dict:
        """Get engine statistics."""
        return self.db.get_stats()
