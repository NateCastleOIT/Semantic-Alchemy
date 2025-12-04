"""
Seed data: Base elements for the alchemy system.
"""
from .models import Element
from .spell_circle_generator import SpellCircleGenerator


def get_base_elements() -> list[Element]:
    """
    Returns the foundational elements that all others are built from.

    These are carefully crafted to have rich, diverse properties that
    can combine in interesting ways.
    """
    generator = SpellCircleGenerator()

    # Create base elements first (without spell circles)
    base_elements = [
        Element(
            name="Fire",
            description="The primal force of heat and transformation. Fire consumes and purifies, turning matter into energy and ash. It represents passion, destruction, and rebirth.",
            tags=["heat", "energy", "destructive", "transformative", "consuming"],
            visual_hint="🔥",
            behavior_hints=["spreads", "consumes", "radiates", "transforms"],
            is_base=True
        ),

        Element(
            name="Water",
            description="The essence of flow and adaptation. Water shapes itself to any vessel, erodes the strongest stone, and carries life within its depths. It represents change, persistence, and emotion.",
            tags=["fluid", "adaptive", "erosive", "life-giving", "flowing"],
            visual_hint="💧",
            behavior_hints=["flows", "adapts", "erodes", "conducts", "cleanses"],
            is_base=True
        ),

        Element(
            name="Earth",
            description="The foundation of stability and growth. Earth endures through ages, provides shelter and sustenance, and holds ancient memory within its layers. It represents strength, permanence, and patience.",
            tags=["solid", "stable", "enduring", "grounding", "fertile"],
            visual_hint="🌍",
            behavior_hints=["stabilizes", "grounds", "grows", "endures", "shields"],
            is_base=True
        ),

        Element(
            name="Air",
            description="The breath of freedom and change. Air moves unseen but felt, carrying whispers and storms alike. It fills all empty spaces and cannot be grasped. It represents freedom, communication, and the intangible.",
            tags=["gaseous", "invisible", "swift", "pervasive", "untethered"],
            visual_hint="💨",
            behavior_hints=["disperses", "carries", "accelerates", "fills", "evades"],
            is_base=True
        ),

        Element(
            name="Light",
            description="The revelation that banishes shadow. Light exposes truth, brings warmth without consuming, and guides through darkness. It represents knowledge, hope, and clarity.",
            tags=["radiant", "revealing", "pure", "illuminating", "warm"],
            visual_hint="✨",
            behavior_hints=["reveals", "illuminates", "purifies", "guides", "blinds"],
            is_base=True
        ),

        Element(
            name="Shadow",
            description="The absence that defines presence. Shadow conceals and protects, holds secrets and fears, and exists only in relation to light. It represents mystery, the unknown, and hidden depths.",
            tags=["dark", "concealing", "cold", "subtle", "elusive"],
            visual_hint="🌑",
            behavior_hints=["conceals", "obscures", "chills", "lingers", "whispers"],
            is_base=True
        ),

        Element(
            name="Chaos",
            description="The primordial force of entropy and possibility. Chaos breaks patterns, defies prediction, and holds infinite potential in its randomness. It represents change, creativity, and raw power.",
            tags=["unpredictable", "entropic", "wild", "potential", "volatile"],
            visual_hint="🌀",
            behavior_hints=["randomizes", "destabilizes", "mutates", "erupts", "warps"],
            is_base=True
        ),

        Element(
            name="Order",
            description="The structure that emerges from chaos. Order creates patterns, establishes laws, and brings harmony through constraint. It represents control, predictability, and perfection.",
            tags=["structured", "lawful", "harmonious", "controlled", "perfect"],
            visual_hint="⚖️",  # Temporary, will be replaced with spell circle
            behavior_hints=["structures", "constrains", "harmonizes", "calculates", "perfects"],
            is_base=True
        ),
    ]

    # Generate unique spell circles for each base element
    for element in base_elements:
        spell_circle_svg = generator.generate(element)
        element.visual_hint = spell_circle_svg

    return base_elements


def initialize_base_elements(database):
    """
    Initialize the database with base elements if they don't exist.

    Args:
        database: AlchemyDatabase instance
    """
    existing_bases = database.get_base_elements()

    if len(existing_bases) == 0:
        print("Initializing base elements...")
        base_elements = get_base_elements()

        for element in base_elements:
            database.save_element(element)
            print(f"  ✓ Added: {element.name}")

        print(f"\n{len(base_elements)} base elements initialized.\n")
    else:
        print(f"Found {len(existing_bases)} existing base elements.\n")
