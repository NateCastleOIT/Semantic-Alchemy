"""
Data models for the Alchemy Engine.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime
import uuid
import json


@dataclass
class Element:
    """
    Represents an alchemical element.

    Elements can be base elements (fire, water, etc.) or combinations of other elements.
    Order matters in combinations: Fire + Water != Water + Fire
    """
    name: str
    description: str
    tags: list[str]
    visual_hint: str
    behavior_hints: list[str]

    # Unique identifier
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Lineage tracking
    is_base: bool = False
    parent_a: Optional[str] = None  # Element ID of first parent
    parent_b: Optional[str] = None  # Element ID of second parent
    combination_order: Optional[str] = None  # "parent_a_id+parent_b_id"

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # Flexible properties for future use
    properties: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert element to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Element':
        """Create an Element from a dictionary."""
        return cls(**data)

    def __str__(self) -> str:
        """String representation for display."""
        lineage = ""
        if self.parent_a and self.parent_b:
            lineage = f" (combination)"
        elif self.is_base:
            lineage = " (base element)"

        return f"{self.name}{lineage}"

    def get_display_info(self) -> str:
        """Get formatted display information about this element."""
        info = []
        info.append(f"\n{'='*60}")
        info.append(f"✨ {self.name.upper()}")
        info.append(f"{'='*60}")
        info.append(f"\n{self.description}")
        info.append(f"\nTags: {', '.join(self.tags)}")
        info.append(f"Visual: {self.visual_hint}")
        info.append(f"Behaviors: {', '.join(self.behavior_hints)}")

        if self.parent_a and self.parent_b:
            info.append(f"\nLineage: Combination of two elements")
        elif self.is_base:
            info.append(f"\nType: Base Element")

        info.append(f"\nID: {self.id}")
        info.append(f"{'='*60}\n")

        return '\n'.join(info)
