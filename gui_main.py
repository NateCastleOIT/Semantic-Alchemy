"""
Entry point for the visual GUI version of the Alchemy Engine.
"""
from alchemy_engine.database import AlchemyDatabase
from alchemy_engine.generator import ElementGenerator
from alchemy_engine.engine import AlchemyEngine
from alchemy_engine.seed_data import initialize_base_elements
from alchemy_engine.gui import launch_gui
from alchemy_engine.config import DATABASE_PATH


def main():
    """Initialize and launch the visual GUI."""
    print("🧪 Semantic Alchemy - Visual Lab")
    print("=" * 50)

    # Initialize components
    database = AlchemyDatabase(DATABASE_PATH)
    generator = ElementGenerator()
    engine = AlchemyEngine(database, generator)

    # Initialize base elements if needed
    initialize_base_elements(database)

    print("✨ Launching visual interface...")
    print("\nControls:")
    print("  - Drag elements from the journal to combination slots")
    print("  - Press 'C' to clear slots")
    print("  - Press ESC to quit")
    print("  - Mouse wheel to scroll journal")
    print("\n" + "=" * 50 + "\n")

    # Launch GUI
    launch_gui(engine)

    print("\n👋 Thanks for exploring the Alchemy Lab!")


if __name__ == "__main__":
    main()
