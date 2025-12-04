"""
Procedural icon generation for alchemical elements.
Creates unique visual representations based on element properties.
"""
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import hashlib
import os


# Tag to color mapping (RGB)
TAG_COLORS = {
    # Primary elements
    "heat": (220, 50, 30),
    "energy": (255, 150, 0),
    "destructive": (180, 0, 0),
    "fluid": (30, 100, 200),
    "adaptive": (50, 150, 220),
    "solid": (101, 67, 33),
    "stable": (120, 90, 60),
    "gaseous": (200, 220, 255),
    "invisible": (230, 240, 255),
    "radiant": (255, 220, 100),
    "pure": (255, 255, 240),
    "dark": (40, 30, 50),
    "concealing": (60, 50, 80),
    "unpredictable": (200, 50, 200),
    "wild": (180, 100, 220),
    "structured": (100, 200, 255),
    "lawful": (150, 180, 230),

    # Secondary properties
    "transformative": (255, 100, 50),
    "consuming": (200, 80, 0),
    "flowing": (60, 120, 200),
    "erosive": (80, 140, 180),
    "grounding": (90, 70, 50),
    "fertile": (80, 120, 60),
    "swift": (220, 230, 255),
    "pervasive": (180, 200, 230),
    "revealing": (255, 240, 150),
    "illuminating": (255, 230, 120),
    "cold": (80, 90, 120),
    "subtle": (120, 110, 140),
    "entropic": (150, 80, 180),
    "volatile": (220, 100, 200),
    "harmonious": (120, 180, 220),
    "controlled": (140, 170, 200),
}


def get_element_color(tags: list[str]) -> Tuple[int, int, int]:
    """
    Determine primary color for an element based on its tags.

    Args:
        tags: List of element tags

    Returns:
        RGB color tuple
    """
    # Try to find a matching tag color
    for tag in tags:
        if tag in TAG_COLORS:
            return TAG_COLORS[tag]

    # Fallback: generate deterministic color from tag hash
    if tags:
        hash_val = int(hashlib.md5(tags[0].encode()).hexdigest()[:6], 16)
        r = (hash_val >> 16) & 0xFF
        g = (hash_val >> 8) & 0xFF
        b = hash_val & 0xFF
        return (r, g, b)

    # Default gray
    return (128, 128, 128)


def get_secondary_color(tags: list[str]) -> Tuple[int, int, int]:
    """
    Get a secondary color for gradients/accents.

    Args:
        tags: List of element tags

    Returns:
        RGB color tuple
    """
    # Use second tag if available
    if len(tags) > 1 and tags[1] in TAG_COLORS:
        return TAG_COLORS[tags[1]]

    # Otherwise brighten/darken the primary color
    primary = get_element_color(tags)
    return (
        min(255, primary[0] + 50),
        min(255, primary[1] + 50),
        min(255, primary[2] + 50)
    )


def create_gradient_circle(size: int, color1: Tuple[int, int, int],
                          color2: Tuple[int, int, int]) -> Image.Image:
    """
    Create a circular gradient from center to edge.

    Args:
        size: Diameter of the circle
        color1: Center color (RGB)
        color2: Edge color (RGB)

    Returns:
        PIL Image with gradient circle
    """
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    center = size // 2

    # Draw gradient in concentric circles
    steps = 50
    for i in range(steps):
        t = i / steps
        # Interpolate colors
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)

        # Calculate radius for this step
        radius = center * (1 - t)

        # Draw circle
        bbox = [
            center - radius, center - radius,
            center + radius, center + radius
        ]
        draw.ellipse(bbox, fill=(r, g, b, 255))

    return image


def add_pattern_overlay(image: Image.Image, tags: list[str],
                        name: str) -> Image.Image:
    """
    Add decorative patterns based on element properties.

    Args:
        image: Base image to overlay on
        tags: Element tags
        name: Element name

    Returns:
        Image with pattern overlay
    """
    draw = ImageDraw.Draw(image)
    size = image.size[0]
    center = size // 2

    # Add patterns based on tags
    if "structured" in tags or "lawful" in tags or "ordered" in tags:
        # Draw geometric grid pattern
        for i in range(4):
            angle = i * 90
            x = center + int(center * 0.6 * (1 if i % 2 == 0 else -1))
            y = center
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 255, 180))

    if "wild" in tags or "chaotic" in tags or "unpredictable" in tags:
        # Draw random-ish splatters
        hash_val = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
        for i in range(5):
            x = center + ((hash_val >> (i * 3)) % 40 - 20)
            y = center + ((hash_val >> (i * 3 + 8)) % 40 - 20)
            r = 2 + (hash_val >> (i * 2)) % 3
            draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, 100))

    if "flowing" in tags or "fluid" in tags:
        # Draw wave pattern
        draw.arc([center-25, center-25, center+25, center+25],
                 0, 180, fill=(255, 255, 255, 150), width=2)
        draw.arc([center-25, center-25, center+25, center+25],
                 180, 360, fill=(255, 255, 255, 150), width=2)

    return image


def generate_icon(element_name: str, tags: list[str],
                  size: int = 64) -> Image.Image:
    """
    Generate a procedural icon for an element.

    Args:
        element_name: Name of the element
        tags: Element tags
        size: Icon size in pixels (square)

    Returns:
        PIL Image of the icon
    """
    # Get colors based on tags
    primary_color = get_element_color(tags)
    secondary_color = get_secondary_color(tags)

    # Create base gradient circle
    icon = create_gradient_circle(size, primary_color, secondary_color)

    # Add pattern overlay
    icon = add_pattern_overlay(icon, tags, element_name)

    # Add outer glow/border
    draw = ImageDraw.Draw(icon)
    border_color = tuple(list(primary_color) + [200])
    draw.ellipse([2, 2, size-2, size-2], outline=border_color, width=2)

    return icon


def save_icon(icon: Image.Image, element_id: str, cache_dir: str = "data/icons"):
    """
    Save an icon to the cache directory.

    Args:
        icon: PIL Image to save
        element_id: Unique element ID
        cache_dir: Directory to save icons
    """
    os.makedirs(cache_dir, exist_ok=True)
    filepath = os.path.join(cache_dir, f"{element_id}.png")
    icon.save(filepath, "PNG")


def get_or_generate_icon(element_name: str, element_id: str, tags: list[str],
                        size: int = 64, cache_dir: str = "data/icons") -> Image.Image:
    """
    Get icon from cache or generate new one.

    Args:
        element_name: Name of the element
        element_id: Unique element ID
        tags: Element tags
        size: Icon size
        cache_dir: Cache directory

    Returns:
        PIL Image of the icon
    """
    filepath = os.path.join(cache_dir, f"{element_id}.png")

    # Try to load from cache
    if os.path.exists(filepath):
        return Image.open(filepath)

    # Generate new icon
    icon = generate_icon(element_name, tags, size)
    save_icon(icon, element_id, cache_dir)

    return icon
