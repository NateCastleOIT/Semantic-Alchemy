"""
Command-line interface for the Alchemy Laboratory.
"""
import sys
from .database import AlchemyDatabase
from .generator import ElementGenerator, GenerationError
from .engine import AlchemyEngine
from .seed_data import initialize_base_elements


class AlchemyCLI:
    """Interactive command-line interface for the alchemy engine."""

    def __init__(self, engine: AlchemyEngine):
        """Initialize the CLI with an alchemy engine."""
        self.engine = engine

    def run(self):
        """Run the main CLI loop."""
        self.print_welcome()

        while True:
            try:
                command = input("\n> ").strip()

                if not command:
                    continue

                self.handle_command(command)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def print_welcome(self):
        """Print welcome message and instructions."""
        print("\n" + "="*70)
        print("✨ ALCHEMY LABORATORY ✨".center(70))
        print("="*70)
        print("\nWelcome to the Semantic Alchemy Engine!")
        print("Combine elements to discover new ones. Order matters!\n")
        print("Commands:")
        print("  list                  - Show all available elements")
        print("  combine <a> <b>       - Combine element A with element B")
        print("  show <name or #>      - Show detailed info about an element")
        print("  lineage <name or #>   - Show the lineage tree of an element")
        print("  stats                 - Show database statistics")
        print("  help                  - Show this help message")
        print("  quit                  - Exit the laboratory")
        print("\nExamples:")
        print("  combine Fire Water")
        print("  combine 1 2")
        print("  show Steam")
        print("  lineage 9")
        print("="*70)

    def handle_command(self, command: str):
        """Handle a user command."""
        parts = command.split()
        cmd = parts[0].lower()

        if cmd in ["quit", "exit", "q"]:
            print("\nGoodbye!")
            sys.exit(0)

        elif cmd == "help":
            self.print_welcome()

        elif cmd == "list":
            self.list_elements()

        elif cmd == "combine":
            if len(parts) < 3:
                print("Usage: combine <element_a> <element_b>")
                print("Example: combine Fire Water")
                print("Example: combine 1 2")
                return
            self.combine_elements(parts[1], parts[2])

        elif cmd == "show":
            if len(parts) < 2:
                print("Usage: show <element_name or number>")
                print("Example: show Fire")
                print("Example: show 1")
                return
            self.show_element(" ".join(parts[1:]))

        elif cmd == "lineage":
            if len(parts) < 2:
                print("Usage: lineage <element_name or number>")
                return
            self.show_lineage(" ".join(parts[1:]))

        elif cmd == "stats":
            self.show_stats()

        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")

    def list_elements(self):
        """List all available elements."""
        elements = self.engine.list_all_elements()

        if not elements:
            print("\nNo elements found. Something went wrong!")
            return

        print("\n" + "="*70)
        print("AVAILABLE ELEMENTS")
        print("="*70)

        # Separate base and combined elements
        base_elements = [e for e in elements if e.is_base]
        combined_elements = [e for e in elements if not e.is_base]

        print("\nBase Elements:")
        for i, element in enumerate(base_elements, 1):
            print(f"  {i}. {element.name}")

        if combined_elements:
            print(f"\nDiscovered Combinations ({len(combined_elements)}):")
            start_idx = len(base_elements) + 1
            for i, element in enumerate(combined_elements, start_idx):
                # Get parent names
                if element.parent_a and element.parent_b:
                    parent_a = self.engine.get_element_by_id(element.parent_a)
                    parent_b = self.engine.get_element_by_id(element.parent_b)
                    parent_info = f" ({parent_a.name} + {parent_b.name})"
                else:
                    parent_info = ""
                print(f"  {i}. {element.name}{parent_info}")

        print("="*70)
        print(f"\nTotal: {len(elements)} elements")

    def combine_elements(self, a: str, b: str):
        """Combine two elements."""
        try:
            # Try to parse as numbers first
            element_a = self._get_element(a)
            element_b = self._get_element(b)

            if not element_a or not element_b:
                return

            # Perform combination
            result = self.engine.combine(element_a, element_b, verbose=True)

            # Display result
            print(result.get_display_info())

        except GenerationError as e:
            print(f"\n❌ Generation failed: {e}")
            print("The LLM may not be responding correctly. Check your Ollama setup.")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def show_element(self, identifier: str):
        """Show detailed information about an element."""
        element = self._get_element(identifier)
        if element:
            print(element.get_display_info())

    def show_lineage(self, identifier: str):
        """Show the lineage tree of an element."""
        element = self._get_element(identifier)
        if element:
            print("\n" + "="*70)
            print(f"LINEAGE TREE: {element.name}")
            print("="*70)
            print()
            print(self.engine.get_lineage(element))
            print("="*70)

    def show_stats(self):
        """Show database statistics."""
        stats = self.engine.get_stats()

        print("\n" + "="*70)
        print("LABORATORY STATISTICS")
        print("="*70)
        print(f"\nBase Elements:      {stats['base_elements']}")
        print(f"Combined Elements:  {stats['combined_elements']}")
        print(f"Total Elements:     {stats['total_elements']}")
        print(f"Total Combinations: {stats['total_combinations']}")
        print("="*70)

    def _get_element(self, identifier: str):
        """
        Get an element by name or number.

        Args:
            identifier: Either an element name or a number (from list command)

        Returns:
            Element if found, None otherwise
        """
        # Try as number first
        try:
            num = int(identifier)
            elements = self.engine.list_all_elements()
            if 1 <= num <= len(elements):
                return elements[num - 1]
            else:
                print(f"Number {num} is out of range (1-{len(elements)})")
                return None
        except ValueError:
            pass

        # Try as name
        try:
            return self.engine.get_element_by_name(identifier)
        except ValueError:
            print(f"Element '{identifier}' not found")
            return None


def main():
    """Main entry point for the CLI."""
    print("\nInitializing Alchemy Laboratory...")

    # Initialize database
    db = AlchemyDatabase()

    # Initialize base elements
    initialize_base_elements(db)

    # Initialize generator
    generator = ElementGenerator()

    # Test Ollama connection
    print("Testing Ollama connection...")
    if not generator.test_connection():
        print("\n❌ ERROR: Cannot connect to Ollama!")
        print("\nOllama doesn't appear to be running.")
        print("Please ensure Ollama is installed and running.")
        print("\nSee the README for setup instructions.")
        sys.exit(1)

    print("✓ Ollama connection successful!")

    # Initialize engine
    engine = AlchemyEngine(db, generator)

    # Start CLI
    cli = AlchemyCLI(engine)
    cli.run()


if __name__ == "__main__":
    main()
