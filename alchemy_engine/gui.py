"""
Pygame-based visual interface for the Alchemy Engine.
Provides drag-and-drop element combination and discovery journal.
"""
import pygame
import sys
from typing import Optional, Tuple
from .models import Element
from .engine import AlchemyEngine
from .icon_generator import get_or_generate_icon


# Colors
BACKGROUND = (20, 20, 30)
PANEL_BG = (35, 35, 50)
PANEL_BORDER = (60, 60, 80)
TEXT_COLOR = (220, 220, 220)
TEXT_DIM = (150, 150, 160)
SLOT_EMPTY = (50, 50, 70)
SLOT_FILLED = (70, 90, 110)
SLOT_HOVER = (90, 110, 130)
BUTTON_BG = (80, 100, 140)
BUTTON_HOVER = (100, 120, 160)


class ElementCard:
    """Represents a draggable element card."""

    def __init__(self, element: Element, x: int, y: int, size: int = 64):
        self.element = element
        self.x = x
        self.y = y
        self.size = size
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.icon = None
        self.load_icon()

    def load_icon(self):
        """Load the procedural icon for this element."""
        pil_icon = get_or_generate_icon(
            self.element.name,
            self.element.id,
            self.element.tags,
            self.size
        )
        # Convert PIL image to Pygame surface
        mode = pil_icon.mode
        size = pil_icon.size
        data = pil_icon.tobytes()
        self.icon = pygame.image.fromstring(data, size, mode)

    def get_rect(self) -> pygame.Rect:
        """Get the rectangle bounds of this card."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is inside this card."""
        return self.get_rect().collidepoint(x, y)

    def start_drag(self, mouse_x: int, mouse_y: int):
        """Start dragging this card."""
        self.dragging = True
        self.offset_x = self.x - mouse_x
        self.offset_y = self.y - mouse_y

    def update_drag(self, mouse_x: int, mouse_y: int):
        """Update position while dragging."""
        if self.dragging:
            self.x = mouse_x + self.offset_x
            self.y = mouse_y + self.offset_y

    def stop_drag(self):
        """Stop dragging this card."""
        self.dragging = False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw the element card."""
        # Draw icon
        if self.icon:
            screen.blit(self.icon, (self.x, self.y))

        # Draw name below icon
        name_surface = font.render(self.element.name, True, TEXT_COLOR)
        name_rect = name_surface.get_rect(centerx=self.x + self.size // 2,
                                         top=self.y + self.size + 4)
        screen.blit(name_surface, name_rect)


class CombinationSlot:
    """A slot for dropping elements to combine."""

    def __init__(self, x: int, y: int, size: int = 80, label: str = ""):
        self.x = x
        self.y = y
        self.size = size
        self.label = label
        self.element: Optional[Element] = None
        self.hover = False

    def get_rect(self) -> pygame.Rect:
        """Get the rectangle bounds of this slot."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is inside this slot."""
        return self.get_rect().collidepoint(x, y)

    def set_element(self, element: Element):
        """Place an element in this slot."""
        self.element = element

    def clear(self):
        """Clear the element from this slot."""
        self.element = None

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, small_font: pygame.font.Font):
        """Draw the combination slot."""
        # Determine color
        if self.element:
            color = SLOT_FILLED
        elif self.hover:
            color = SLOT_HOVER
        else:
            color = SLOT_EMPTY

        # Draw slot background
        pygame.draw.rect(screen, color, self.get_rect(), border_radius=8)
        pygame.draw.rect(screen, PANEL_BORDER, self.get_rect(), width=2, border_radius=8)

        # Draw label
        if self.label:
            label_surface = small_font.render(self.label, True, TEXT_DIM)
            label_rect = label_surface.get_rect(centerx=self.x + self.size // 2,
                                               bottom=self.y - 5)
            screen.blit(label_surface, label_rect)

        # Draw element if present
        if self.element:
            icon = get_or_generate_icon(
                self.element.name,
                self.element.id,
                self.element.tags,
                self.size - 10
            )
            # Convert PIL to Pygame
            mode = icon.mode
            size = icon.size
            data = icon.tobytes()
            icon_surface = pygame.image.fromstring(data, size, mode)

            icon_x = self.x + 5
            icon_y = self.y + 5
            screen.blit(icon_surface, (icon_x, icon_y))

            # Draw element name
            name_surface = small_font.render(self.element.name, True, TEXT_COLOR)
            name_rect = name_surface.get_rect(centerx=self.x + self.size // 2,
                                             top=self.y + self.size + 4)
            screen.blit(name_surface, name_rect)


class AlchemyGUI:
    """Main GUI application for the Alchemy Engine."""

    def __init__(self, engine: AlchemyEngine):
        pygame.init()

        self.engine = engine
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Semantic Alchemy - Discovery Lab")

        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 36)

        # UI state
        self.scroll_offset = 0
        self.dragging_card: Optional[ElementCard] = None

        # Combination slots
        self.slot_a = CombinationSlot(450, 300, 80, "First Element")
        self.slot_b = CombinationSlot(650, 300, 80, "Second Element")

        # Result display
        self.result_element: Optional[Element] = None
        self.combining = False

        # Clock for FPS
        self.clock = pygame.time.Clock()

    def get_all_elements(self) -> list[Element]:
        """Get all discovered elements from the engine."""
        return self.engine.db.get_all_elements()

    def create_element_cards(self) -> list[ElementCard]:
        """Create element cards for the discovery journal."""
        elements = self.get_all_elements()
        cards = []

        # Layout cards in a grid in the left panel
        card_size = 64
        padding = 10
        cards_per_row = 2
        start_x = 20
        start_y = 80

        for i, element in enumerate(elements):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_size + padding + 60)
            y = start_y + row * (card_size + padding + 30) - self.scroll_offset

            card = ElementCard(element, x, y, card_size)
            cards.append(card)

        return cards

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEWHEEL:
                # Scroll the discovery journal
                self.scroll_offset -= event.y * 20
                self.scroll_offset = max(0, self.scroll_offset)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    self.handle_mouse_down(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    self.handle_mouse_up(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                self.handle_mouse_motion(mouse_x, mouse_y)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_c:
                    # Clear slots
                    self.slot_a.clear()
                    self.slot_b.clear()
                    self.result_element = None

        return True

    def handle_mouse_down(self, mouse_x: int, mouse_y: int):
        """Handle mouse button down."""
        # Check if clicking on an element card in the journal
        cards = self.create_element_cards()
        for card in cards:
            # Only allow dragging from journal area (left panel)
            if mouse_x < 350 and card.contains_point(mouse_x, mouse_y):
                self.dragging_card = card
                self.dragging_card.start_drag(mouse_x, mouse_y)
                break

    def handle_mouse_up(self, mouse_x: int, mouse_y: int):
        """Handle mouse button up."""
        if self.dragging_card:
            # Check if dropped on a slot
            if self.slot_a.contains_point(mouse_x, mouse_y):
                self.slot_a.set_element(self.dragging_card.element)
                self.check_combination()
            elif self.slot_b.contains_point(mouse_x, mouse_y):
                self.slot_b.set_element(self.dragging_card.element)
                self.check_combination()

            self.dragging_card.stop_drag()
            self.dragging_card = None

    def handle_mouse_motion(self, mouse_x: int, mouse_y: int):
        """Handle mouse motion."""
        # Update dragging card position
        if self.dragging_card:
            self.dragging_card.update_drag(mouse_x, mouse_y)

        # Update slot hover states
        self.slot_a.hover = self.slot_a.contains_point(mouse_x, mouse_y)
        self.slot_b.hover = self.slot_b.contains_point(mouse_x, mouse_y)

    def check_combination(self):
        """Check if both slots are filled and combine."""
        if self.slot_a.element and self.slot_b.element:
            # Perform combination
            self.result_element = self.engine.combine(
                self.slot_a.element,
                self.slot_b.element
            )

    def draw(self):
        """Draw the entire GUI."""
        # Clear screen
        self.screen.fill(BACKGROUND)

        # Draw panels
        self.draw_journal_panel()
        self.draw_combination_panel()
        self.draw_result_panel()

        # Draw dragging card on top
        if self.dragging_card:
            self.dragging_card.draw(self.screen, self.small_font)

        pygame.display.flip()

    def draw_journal_panel(self):
        """Draw the discovery journal panel."""
        # Panel background
        panel_rect = pygame.Rect(10, 10, 350, self.height - 20)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, width=2, border_radius=10)

        # Title
        title = self.title_font.render("Discovery Journal", True, TEXT_COLOR)
        self.screen.blit(title, (20, 20))

        # Element count
        element_count = len(self.get_all_elements())
        count_text = self.small_font.render(f"{element_count} elements discovered", True, TEXT_DIM)
        self.screen.blit(count_text, (20, 55))

        # Draw element cards (with clipping to panel)
        clip_rect = pygame.Rect(10, 70, 350, self.height - 80)
        self.screen.set_clip(clip_rect)

        cards = self.create_element_cards()
        for card in cards:
            if not card.dragging:  # Don't draw if being dragged
                card.draw(self.screen, self.small_font)

        self.screen.set_clip(None)

    def draw_combination_panel(self):
        """Draw the combination panel."""
        # Panel background
        panel_rect = pygame.Rect(370, 10, 460, self.height - 20)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, width=2, border_radius=10)

        # Title
        title = self.title_font.render("Combination Lab", True, TEXT_COLOR)
        title_rect = title.get_rect(centerx=600, top=20)
        self.screen.blit(title, title_rect)

        # Instructions
        instruction = self.small_font.render("Drag elements here to combine them", True, TEXT_DIM)
        instruction_rect = instruction.get_rect(centerx=600, top=60)
        self.screen.blit(instruction, instruction_rect)

        # Draw combination slots
        self.slot_a.draw(self.screen, self.font, self.small_font)
        self.slot_b.draw(self.screen, self.font, self.small_font)

        # Draw plus sign between slots
        plus_text = self.title_font.render("+", True, TEXT_COLOR)
        plus_rect = plus_text.get_rect(center=(600, 340))
        self.screen.blit(plus_text, plus_rect)

        # Draw arrow pointing down
        arrow_text = self.title_font.render("↓", True, TEXT_COLOR)
        arrow_rect = arrow_text.get_rect(centerx=600, top=420)
        self.screen.blit(arrow_text, arrow_rect)

        # Keyboard shortcut hint
        hint = self.small_font.render("Press 'C' to clear slots | ESC to quit", True, TEXT_DIM)
        hint_rect = hint.get_rect(centerx=600, bottom=self.height - 30)
        self.screen.blit(hint, hint_rect)

    def draw_result_panel(self):
        """Draw the result panel."""
        # Panel background
        panel_rect = pygame.Rect(840, 10, 350, self.height - 20)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, width=2, border_radius=10)

        # Title
        title = self.title_font.render("Result", True, TEXT_COLOR)
        title_rect = title.get_rect(centerx=1015, top=20)
        self.screen.blit(title, title_rect)

        # Draw result element if present
        if self.result_element:
            # Large icon
            icon_size = 100
            icon = get_or_generate_icon(
                self.result_element.name,
                self.result_element.id,
                self.result_element.tags,
                icon_size
            )
            # Convert PIL to Pygame
            mode = icon.mode
            size = icon.size
            data = icon.tobytes()
            icon_surface = pygame.image.fromstring(data, size, mode)

            icon_x = 1015 - icon_size // 2
            icon_y = 100
            self.screen.blit(icon_surface, (icon_x, icon_y))

            # Name
            name_text = self.title_font.render(self.result_element.name, True, TEXT_COLOR)
            name_rect = name_text.get_rect(centerx=1015, top=220)
            self.screen.blit(name_text, name_rect)

            # Description (wrapped)
            self.draw_wrapped_text(
                self.result_element.description,
                850, 270, 330,
                self.small_font, TEXT_DIM
            )

            # Tags
            tags_y = 420
            tags_title = self.small_font.render("Tags:", True, TEXT_COLOR)
            self.screen.blit(tags_title, (850, tags_y))

            tags_text = ", ".join(self.result_element.tags[:5])  # Limit to 5 tags
            tags_surface = self.small_font.render(tags_text, True, TEXT_DIM)
            self.screen.blit(tags_surface, (850, tags_y + 25))

            # Is it new?
            if hasattr(self, 'last_was_new') and self.last_was_new:
                new_text = self.title_font.render("⭐ NEW DISCOVERY! ⭐", True, (255, 215, 0))
                new_rect = new_text.get_rect(centerx=1015, top=500)
                self.screen.blit(new_text, new_rect)

        else:
            # Placeholder text
            placeholder = self.font.render("Combine elements to", True, TEXT_DIM)
            placeholder_rect = placeholder.get_rect(centerx=1015, centery=300)
            self.screen.blit(placeholder, placeholder_rect)

            placeholder2 = self.font.render("see the result", True, TEXT_DIM)
            placeholder2_rect = placeholder2.get_rect(centerx=1015, centery=330)
            self.screen.blit(placeholder2, placeholder2_rect)

    def draw_wrapped_text(self, text: str, x: int, y: int, max_width: int,
                         font: pygame.font.Font, color: Tuple[int, int, int]):
        """Draw text with word wrapping."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Draw lines
        line_height = font.get_height() + 4
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (x, y + i * line_height))

    def run(self):
        """Main game loop."""
        running = True

        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()


def launch_gui(engine: AlchemyEngine):
    """Launch the GUI application."""
    gui = AlchemyGUI(engine)
    gui.run()
