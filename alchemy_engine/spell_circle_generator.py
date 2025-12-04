"""
Procedural spell circle generator for element icons.
Generates unique, intricate SVG-based magical circles based on element properties.
"""
import hashlib
import math
from typing import List, Tuple, Optional
from .models import Element


class SpellCircleGenerator:
    """Generates unique, intricate spell circle SVGs based on element properties."""

    # Expanded color mappings
    TAG_COLORS = {
        # Primary elements
        "heat": "#ff4444", "fire": "#ff6633", "energy": "#ffaa00", "destructive": "#ff2222",
        "fluid": "#4488ff", "water": "#3399ff", "flowing": "#66bbff", "adaptive": "#44ffff",
        "solid": "#8b6f47", "earth": "#654321", "stone": "#808080", "stable": "#996633",
        "gaseous": "#e0e0ff", "air": "#c0d0ff", "swift": "#d0e0ff", "invisible": "#aabbcc",
        "radiant": "#ffee44", "light": "#ffffaa", "illuminating": "#ffff88", "pure": "#ffffcc",
        "dark": "#222244", "shadow": "#1a1a2a", "concealing": "#2a2a3a", "cold": "#1a2a3a",
        "entropic": "#9933ff", "chaos": "#cc44ff", "wild": "#ff33cc", "volatile": "#dd22ee",
        "lawful": "#44aaff", "order": "#66ccff", "structured": "#88ddff", "perfect": "#aaeeff",
        "life-giving": "#44ff88", "transformative": "#ff8844",
    }

    # Mystical runes (simplified alchemical/mystical symbols)
    RUNES = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ", "ᚺ", "ᚾ", "ᛁ", "ᛃ", "ᛇ", "ᛈ", "ᛉ", "ᛊ", "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛜ", "ᛞ", "ᛟ"]

    def __init__(self):
        self.size = 200
        self.center = self.size / 2

    def generate(self, element: Element, parent_a: Optional[Element] = None,
                 parent_b: Optional[Element] = None) -> str:
        """Generate a unique, intricate spell circle SVG."""
        seed = self._hash_to_seed(element.id)
        colors = self._get_color_palette(element.tags, seed)

        # Determine element archetype for pattern selection
        archetype = self._determine_archetype(element.tags)

        svg_parts = []

        # Background layer (1-2 circles max, used sparingly)
        svg_parts.extend(self._generate_background_circles(colors, seed, min(len(element.tags), 2)))

        # Main geometric pattern based on archetype
        svg_parts.extend(self._generate_sacred_geometry(archetype, colors, seed, element))

        # Runic symbols around perimeter
        svg_parts.extend(self._generate_runes(element, colors, seed))

        # Symbolic constellation connecting behavior hints
        svg_parts.extend(self._generate_constellation(element.behavior_hints, colors, seed))

        # Parent integration (if derived element)
        if parent_a and parent_b:
            svg_parts.extend(self._generate_parent_blend(parent_a, parent_b, colors, seed))

        # Complex center design
        svg_parts.append(self._generate_center_sigil(archetype, colors[0], seed, element.name))

        # Apply rotation for some elements
        rotation = self._get_rotation(seed, archetype)

        return self._compose_svg(svg_parts, element.name, rotation)

    def _hash_to_seed(self, element_id: str) -> int:
        """Convert element ID to deterministic seed."""
        hash_obj = hashlib.md5(element_id.encode())
        return int(hash_obj.hexdigest()[:8], 16)

    def _determine_archetype(self, tags: List[str]) -> str:
        """Determine element archetype from tags."""
        tags_lower = [t.lower() for t in tags]

        if any(t in tags_lower for t in ["heat", "fire", "energy", "destructive"]):
            return "fire"
        elif any(t in tags_lower for t in ["fluid", "water", "flowing", "adaptive"]):
            return "water"
        elif any(t in tags_lower for t in ["solid", "earth", "stone", "stable"]):
            return "earth"
        elif any(t in tags_lower for t in ["gaseous", "air", "swift", "invisible"]):
            return "air"
        elif any(t in tags_lower for t in ["radiant", "light", "illuminating"]):
            return "light"
        elif any(t in tags_lower for t in ["dark", "shadow", "concealing"]):
            return "shadow"
        elif any(t in tags_lower for t in ["entropic", "chaos", "wild", "volatile"]):
            return "chaos"
        elif any(t in tags_lower for t in ["lawful", "order", "structured", "perfect"]):
            return "order"
        else:
            return "neutral"

    def _get_color_palette(self, tags: List[str], seed: int) -> List[str]:
        """Generate color palette from tags."""
        colors = []
        for tag in tags:
            for key, color in self.TAG_COLORS.items():
                if key in tag.lower():
                    colors.append(color)
                    break

        while len(colors) < 4:
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            hue = (seed % 360)
            colors.append(f"hsl({hue}, 70%, 60%)")

        return colors[:6]

    def _generate_background_circles(self, colors: List[str], seed: int, count: int) -> List[str]:
        """Generate 1-2 background circles as accent, not main structure."""
        circles = []
        max_radius = self.center * 0.95

        for i in range(min(count, 2)):  # Max 2 circles
            radius = max_radius - (i * 25)
            color = colors[i % len(colors)]
            seed = (seed * 1103515245 + 12345) & 0x7fffffff

            opacity = 0.2 + (seed % 30) / 100
            dash = ""
            if seed % 2 == 0:
                dash = f'stroke-dasharray="8 4"'

            circles.append(
                f'<circle cx="{self.center}" cy="{self.center}" r="{radius}" '
                f'fill="none" stroke="{color}" stroke-width="1.5" {dash} opacity="{opacity}"/>'
            )

        return circles

    def _generate_sacred_geometry(self, archetype: str, colors: List[str],
                                   seed: int, element: Element) -> List[str]:
        """Generate main geometric pattern based on element archetype."""
        patterns = []

        if archetype == "fire":
            patterns.extend(self._pattern_fire(colors, seed))
        elif archetype == "water":
            patterns.extend(self._pattern_water(colors, seed))
        elif archetype == "earth":
            patterns.extend(self._pattern_earth(colors, seed))
        elif archetype == "air":
            patterns.extend(self._pattern_air(colors, seed))
        elif archetype == "light":
            patterns.extend(self._pattern_light(colors, seed))
        elif archetype == "shadow":
            patterns.extend(self._pattern_shadow(colors, seed))
        elif archetype == "chaos":
            patterns.extend(self._pattern_chaos(colors, seed))
        elif archetype == "order":
            patterns.extend(self._pattern_order(colors, seed))
        else:
            patterns.extend(self._pattern_neutral(colors, seed))

        return patterns

    def _pattern_fire(self, colors: List[str], seed: int) -> List[str]:
        """Sharp triangular rays radiating outward."""
        patterns = []
        ray_count = 8 + (seed % 5)

        for i in range(ray_count):
            angle = (360 / ray_count) * i
            angle_rad = math.radians(angle)

            # Inner and outer points for triangular rays
            inner_r = self.center * 0.4
            outer_r = self.center * 0.85

            x1 = self.center + inner_r * math.cos(angle_rad)
            y1 = self.center + inner_r * math.sin(angle_rad)
            x2 = self.center + outer_r * math.cos(angle_rad)
            y2 = self.center + outer_r * math.sin(angle_rad)

            # Side points for triangle
            side_angle = 15
            x3 = self.center + (inner_r + outer_r) / 2 * math.cos(math.radians(angle + side_angle))
            y3 = self.center + (inner_r + outer_r) / 2 * math.sin(math.radians(angle + side_angle))
            x4 = self.center + (inner_r + outer_r) / 2 * math.cos(math.radians(angle - side_angle))
            y4 = self.center + (inner_r + outer_r) / 2 * math.sin(math.radians(angle - side_angle))

            color = colors[i % len(colors)]
            patterns.append(
                f'<path d="M {x1} {y1} L {x3} {y3} L {x2} {y2} L {x4} {y4} Z" '
                f'fill="{color}" opacity="0.6" stroke="{colors[0]}" stroke-width="1"/>'
            )

        return patterns

    def _pattern_water(self, colors: List[str], seed: int) -> List[str]:
        """Flowing curves and wave patterns."""
        patterns = []
        wave_count = 6

        for i in range(wave_count):
            radius = self.center * (0.3 + i * 0.1)
            amplitude = 5 + (seed % 10)

            # Create flowing sine wave path
            path = f"M {self.center + radius} {self.center}"
            for angle in range(0, 360, 10):
                angle_rad = math.radians(angle)
                wave = amplitude * math.sin(math.radians(angle * 3))
                r = radius + wave
                x = self.center + r * math.cos(angle_rad)
                y = self.center + r * math.sin(angle_rad)
                path += f" L {x} {y}"
            path += " Z"

            color = colors[i % len(colors)]
            patterns.append(
                f'<path d="{path}" fill="none" stroke="{color}" '
                f'stroke-width="2" opacity="0.65"/>'
            )

        return patterns

    def _pattern_earth(self, colors: List[str], seed: int) -> List[str]:
        """Crystalline hexagonal grid structure."""
        patterns = []

        # Generate hexagon
        hex_points = []
        hex_radius = self.center * 0.7
        for i in range(6):
            angle = math.radians(60 * i)
            x = self.center + hex_radius * math.cos(angle)
            y = self.center + hex_radius * math.sin(angle)
            hex_points.append((x, y))

        # Main hexagon
        hex_path = "M " + " L ".join([f"{x} {y}" for x, y in hex_points]) + " Z"
        patterns.append(
            f'<path d="{hex_path}" fill="none" stroke="{colors[0]}" '
            f'stroke-width="2" opacity="0.7"/>'
        )

        # Inner geometric divisions
        for i in range(6):
            x, y = hex_points[i]
            patterns.append(
                f'<line x1="{self.center}" y1="{self.center}" x2="{x}" y2="{y}" '
                f'stroke="{colors[1 % len(colors)]}" stroke-width="1" opacity="0.6"/>'
            )

        # Smaller inner hexagon
        small_hex_radius = self.center * 0.35
        small_hex = []
        for i in range(6):
            angle = math.radians(60 * i + 30)
            x = self.center + small_hex_radius * math.cos(angle)
            y = self.center + small_hex_radius * math.sin(angle)
            small_hex.append((x, y))

        small_path = "M " + " L ".join([f"{x} {y}" for x, y in small_hex]) + " Z"
        patterns.append(
            f'<path d="{small_path}" fill="{colors[0]}" opacity="0.2" '
            f'stroke="{colors[1 % len(colors)]}" stroke-width="1.5"/>'
        )

        return patterns

    def _pattern_air(self, colors: List[str], seed: int) -> List[str]:
        """Swirling spirals and curved lines."""
        patterns = []
        spiral_count = 3

        for s in range(spiral_count):
            path = f"M {self.center} {self.center}"
            turns = 2 + (seed % 3)

            for i in range(360 * turns):
                angle = math.radians(i)
                radius = (i / (360 * turns)) * self.center * 0.8
                x = self.center + radius * math.cos(angle + s * math.pi * 2 / spiral_count)
                y = self.center + radius * math.sin(angle + s * math.pi * 2 / spiral_count)

                if i % 5 == 0:  # Sample points
                    path += f" L {x} {y}"

            color = colors[s % len(colors)]
            patterns.append(
                f'<path d="{path}" fill="none" stroke="{color}" '
                f'stroke-width="1.5" opacity="0.6"/>'
            )

        return patterns

    def _pattern_light(self, colors: List[str], seed: int) -> List[str]:
        """Radiating beams and sunburst pattern."""
        patterns = []
        beam_count = 12 + (seed % 8)

        for i in range(beam_count):
            angle = (360 / beam_count) * i
            angle_rad = math.radians(angle)

            # Alternating long and short beams
            if i % 2 == 0:
                outer_r = self.center * 0.9
            else:
                outer_r = self.center * 0.7

            inner_r = self.center * 0.2

            x1 = self.center + inner_r * math.cos(angle_rad)
            y1 = self.center + inner_r * math.sin(angle_rad)
            x2 = self.center + outer_r * math.cos(angle_rad)
            y2 = self.center + outer_r * math.sin(angle_rad)

            # Create gradient-like effect with opacity
            opacity = 0.3 + (i % 5) * 0.1
            patterns.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{colors[0]}" stroke-width="2" opacity="{opacity}" '
                f'stroke-linecap="round"/>'
            )

        return patterns

    def _pattern_shadow(self, colors: List[str], seed: int) -> List[str]:
        """Interlocking crescents and void patterns."""
        patterns = []
        crescent_count = 6

        for i in range(crescent_count):
            angle = (360 / crescent_count) * i
            radius = self.center * 0.6

            # Create crescent using two circles (one filled, one cut out)
            angle_rad = math.radians(angle)
            x = self.center + radius * 0.3 * math.cos(angle_rad)
            y = self.center + radius * 0.3 * math.sin(angle_rad)

            patterns.append(
                f'<circle cx="{x}" cy="{y}" r="{radius * 0.4}" '
                f'fill="{colors[i % len(colors)]}" opacity="0.4"/>'
            )

        # Add shadow voids (darker circles)
        for i in range(3):
            angle = i * 120
            angle_rad = math.radians(angle)
            x = self.center + self.center * 0.5 * math.cos(angle_rad)
            y = self.center + self.center * 0.5 * math.sin(angle_rad)

            patterns.append(
                f'<circle cx="{x}" cy="{y}" r="15" '
                f'fill="#000000" opacity="0.3"/>'
            )

        return patterns

    def _pattern_chaos(self, colors: List[str], seed: int) -> List[str]:
        """Asymmetric, broken geometry with jagged patterns."""
        patterns = []

        # Create intentionally chaotic, asymmetric shapes
        for i in range(8):
            seed = (seed * 1103515245 + 12345) & 0x7fffffff

            # Random polygon
            sides = 3 + (seed % 5)
            path = "M "

            for j in range(sides):
                angle = math.radians((360 / sides) * j + (seed % 60) - 30)
                radius = self.center * (0.4 + (seed % 400) / 1000)
                x = self.center + radius * math.cos(angle)
                y = self.center + radius * math.sin(angle)
                path += f"{x} {y} L "

            path += "Z"

            color = colors[i % len(colors)]
            patterns.append(
                f'<path d="{path}" fill="none" stroke="{color}" '
                f'stroke-width="{1 + seed % 2}" opacity="0.5"/>'
            )

        return patterns

    def _pattern_order(self, colors: List[str], seed: int) -> List[str]:
        """Perfect symmetry, mandala-like precision."""
        patterns = []

        # Create perfect mandala with 8-fold symmetry
        symmetry = 8
        layers = 4

        for layer in range(layers):
            radius = self.center * (0.3 + layer * 0.15)

            for i in range(symmetry):
                angle = (360 / symmetry) * i
                angle_rad = math.radians(angle)

                # Perfect geometric shapes at each point
                x = self.center + radius * math.cos(angle_rad)
                y = self.center + radius * math.sin(angle_rad)

                # Small perfect circles at symmetry points
                patterns.append(
                    f'<circle cx="{x}" cy="{y}" r="6" '
                    f'fill="{colors[layer % len(colors)]}" opacity="0.7" '
                    f'stroke="{colors[0]}" stroke-width="1"/>'
                )

                # Connect with perfect lines
                if layer > 0:
                    prev_radius = self.center * (0.3 + (layer - 1) * 0.15)
                    prev_x = self.center + prev_radius * math.cos(angle_rad)
                    prev_y = self.center + prev_radius * math.sin(angle_rad)

                    patterns.append(
                        f'<line x1="{prev_x}" y1="{prev_y}" x2="{x}" y2="{y}" '
                        f'stroke="{colors[1 % len(colors)]}" stroke-width="1" opacity="0.55"/>'
                    )

        return patterns

    def _pattern_neutral(self, colors: List[str], seed: int) -> List[str]:
        """Varied geometric patterns for neutral/hybrid elements."""
        patterns = []

        # Choose from several different patterns based on seed
        pattern_type = seed % 5

        if pattern_type == 0:
            # Interlocking triangles
            size = self.center * 0.6
            patterns.append(
                f'<path d="M {self.center} {self.center - size} '
                f'L {self.center - size} {self.center + size} '
                f'L {self.center + size} {self.center + size} Z" '
                f'fill="none" stroke="{colors[0]}" stroke-width="2" opacity="0.6"/>'
            )
            patterns.append(
                f'<path d="M {self.center} {self.center + size * 0.6} '
                f'L {self.center - size * 0.6} {self.center - size * 0.6} '
                f'L {self.center + size * 0.6} {self.center - size * 0.6} Z" '
                f'fill="none" stroke="{colors[1 % len(colors)]}" stroke-width="2" opacity="0.6"/>'
            )
        elif pattern_type == 1:
            # Concentric squares rotated
            for i in range(3):
                size = self.center * (0.3 + i * 0.15)
                rotation = 45 if i % 2 else 0
                patterns.append(
                    f'<rect x="{self.center - size}" y="{self.center - size}" '
                    f'width="{size * 2}" height="{size * 2}" fill="none" '
                    f'stroke="{colors[i % len(colors)]}" stroke-width="1.5" opacity="0.5" '
                    f'transform="rotate({rotation} {self.center} {self.center})"/>'
                )
        elif pattern_type == 2:
            # Cross pattern with diamonds
            length = self.center * 0.7
            patterns.append(
                f'<line x1="{self.center}" y1="{self.center - length}" '
                f'x2="{self.center}" y2="{self.center + length}" '
                f'stroke="{colors[0]}" stroke-width="2" opacity="0.6"/>'
            )
            patterns.append(
                f'<line x1="{self.center - length}" y1="{self.center}" '
                f'x2="{self.center + length}" y2="{self.center}" '
                f'stroke="{colors[1 % len(colors)]}" stroke-width="2" opacity="0.6"/>'
            )
            # Diamonds at ends
            diamond_size = 8
            for angle in [0, 90, 180, 270]:
                angle_rad = math.radians(angle)
                x = self.center + length * math.cos(angle_rad)
                y = self.center + length * math.sin(angle_rad)
                patterns.append(
                    f'<rect x="{x - diamond_size}" y="{y - diamond_size}" '
                    f'width="{diamond_size * 2}" height="{diamond_size * 2}" fill="{colors[0]}" '
                    f'opacity="0.5" transform="rotate(45 {x} {y})"/>'
                )
        elif pattern_type == 3:
            # Octagon with radial divisions
            sides = 8
            radius = self.center * 0.7
            oct_path = "M "
            for i in range(sides):
                angle = math.radians((360 / sides) * i)
                x = self.center + radius * math.cos(angle)
                y = self.center + radius * math.sin(angle)
                oct_path += f"{x} {y} L "
                # Radial lines
                patterns.append(
                    f'<line x1="{self.center}" y1="{self.center}" x2="{x}" y2="{y}" '
                    f'stroke="{colors[1 % len(colors)]}" stroke-width="1" opacity="0.55"/>'
                )
            oct_path += "Z"
            patterns.append(
                f'<path d="{oct_path}" fill="none" stroke="{colors[0]}" '
                f'stroke-width="2" opacity="0.6"/>'
            )
        else:
            # Vesica piscis (two overlapping circles)
            offset = self.center * 0.25
            radius = self.center * 0.6
            patterns.append(
                f'<circle cx="{self.center - offset}" cy="{self.center}" r="{radius}" '
                f'fill="none" stroke="{colors[0]}" stroke-width="2" opacity="0.5"/>'
            )
            patterns.append(
                f'<circle cx="{self.center + offset}" cy="{self.center}" r="{radius}" '
                f'fill="none" stroke="{colors[1 % len(colors)]}" stroke-width="2" opacity="0.5"/>'
            )

        return patterns

    def _generate_runes(self, element: Element, colors: List[str], seed: int) -> List[str]:
        """Generate mystical runes around the perimeter."""
        runes = []
        rune_count = min(len(element.tags) + len(element.behavior_hints), 12)

        if rune_count == 0:
            return runes

        rune_radius = self.center * 0.9

        for i in range(rune_count):
            angle = (360 / rune_count) * i
            angle_rad = math.radians(angle)

            x = self.center + rune_radius * math.cos(angle_rad)
            y = self.center + rune_radius * math.sin(angle_rad)

            # Select rune based on seed and index
            rune_index = (seed + i * 7) % len(self.RUNES)
            rune = self.RUNES[rune_index]

            color = colors[i % len(colors)]

            runes.append(
                f'<text x="{x}" y="{y}" font-family="serif" font-size="14" '
                f'fill="{color}" opacity="0.7" text-anchor="middle" '
                f'dominant-baseline="middle">{rune}</text>'
            )

        return runes

    def _generate_constellation(self, behavior_hints: List[str], colors: List[str], seed: int) -> List[str]:
        """Create subtle constellation by connecting behavior symbols."""
        constellation = []
        symbol_count = min(len(behavior_hints), 6)  # Reduced from 8

        if symbol_count < 3:  # Require at least 3 for variety
            return constellation

        # Only add constellation 50% of the time based on seed
        if seed % 2 == 0:
            return constellation

        symbol_radius = self.center * 0.55
        points = []

        # Place symbols (smaller and more subtle)
        for i in range(symbol_count):
            angle = (360 / symbol_count) * i + (seed % 45)
            angle_rad = math.radians(angle)
            x = self.center + symbol_radius * math.cos(angle_rad)
            y = self.center + symbol_radius * math.sin(angle_rad)
            points.append((x, y))

            # Smaller, more subtle markers
            color = colors[i % len(colors)]
            constellation.append(
                f'<circle cx="{x}" cy="{y}" r="2.5" fill="{color}" opacity="0.7"/>'
            )

        # Only connect to adjacent points (not full polygon)
        # Create more varied connection patterns
        for i in range(len(points)):
            # Connect to next point only if it's not creating a regular polygon feel
            if i < len(points) - 1 and seed % 3 != 0:  # Skip some connections
                x1, y1 = points[i]
                x2, y2 = points[i + 1]

                constellation.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{colors[0]}" stroke-width="0.8" opacity="0.45" '
                    f'stroke-dasharray="2 3"/>'
                )

        return constellation

    def _generate_parent_blend(self, parent_a: Element, parent_b: Element,
                                colors: List[str], seed: int) -> List[str]:
        """Blend parent patterns into the design."""
        blend = []

        parent_a_color = self._get_primary_color_from_tags(parent_a.tags)
        parent_b_color = self._get_primary_color_from_tags(parent_b.tags)

        # Create vesica piscis (two overlapping circles) representing parent fusion
        offset = self.center * 0.15

        # Parent A circle (left)
        blend.append(
            f'<circle cx="{self.center - offset}" cy="{self.center}" r="25" '
            f'fill="none" stroke="{parent_a_color}" stroke-width="2" opacity="0.4"/>'
        )

        # Parent B circle (right)
        blend.append(
            f'<circle cx="{self.center + offset}" cy="{self.center}" r="25" '
            f'fill="none" stroke="{parent_b_color}" stroke-width="2" opacity="0.4"/>'
        )

        # Add parent symbols in quadrants
        archetype_a = self._determine_archetype(parent_a.tags)
        archetype_b = self._determine_archetype(parent_b.tags)

        # Small parent signature patterns in corners
        blend.append(
            f'<text x="{self.center - 70}" y="{self.center - 70}" '
            f'font-family="serif" font-size="10" fill="{parent_a_color}" '
            f'opacity="0.5">{archetype_a[0].upper()}</text>'
        )

        blend.append(
            f'<text x="{self.center + 70}" y="{self.center + 70}" '
            f'font-family="serif" font-size="10" fill="{parent_b_color}" '
            f'opacity="0.5">{archetype_b[0].upper()}</text>'
        )

        return blend

    def _get_primary_color_from_tags(self, tags: List[str]) -> str:
        """Get primary color for tags."""
        for tag in tags:
            for key, color in self.TAG_COLORS.items():
                if key in tag.lower():
                    return color
        return "#888888"

    def _generate_center_sigil(self, archetype: str, color: str, seed: int, name: str) -> str:
        """Generate complex center design."""
        center_parts = []

        # Archetype-specific center symbol
        if archetype == "fire":
            # Upward triangle
            size = 12
            center_parts.append(
                f'<path d="M {self.center} {self.center - size} '
                f'L {self.center - size} {self.center + size} '
                f'L {self.center + size} {self.center + size} Z" '
                f'fill="{color}" opacity="0.8"/>'
            )
        elif archetype == "water":
            # Downward triangle
            size = 12
            center_parts.append(
                f'<path d="M {self.center} {self.center + size} '
                f'L {self.center - size} {self.center - size} '
                f'L {self.center + size} {self.center - size} Z" '
                f'fill="{color}" opacity="0.8"/>'
            )
        elif archetype == "earth":
            # Square
            size = 10
            center_parts.append(
                f'<rect x="{self.center - size}" y="{self.center - size}" '
                f'width="{size * 2}" height="{size * 2}" fill="{color}" opacity="0.8"/>'
            )
        elif archetype == "air":
            # Circle
            center_parts.append(
                f'<circle cx="{self.center}" cy="{self.center}" r="10" '
                f'fill="{color}" opacity="0.8"/>'
            )
        elif archetype == "order":
            # Perfect hexagon
            hex_size = 12
            hex_path = "M "
            for i in range(6):
                angle = math.radians(60 * i)
                x = self.center + hex_size * math.cos(angle)
                y = self.center + hex_size * math.sin(angle)
                hex_path += f"{x} {y} L "
            hex_path += "Z"
            center_parts.append(f'<path d="{hex_path}" fill="{color}" opacity="0.8"/>')
        else:
            # Default: pentagram
            points = 5
            outer = 12
            inner = 5
            path = "M "
            for i in range(points * 2):
                angle = math.radians(i * 180 / points - 90)
                r = outer if i % 2 == 0 else inner
                x = self.center + r * math.cos(angle)
                y = self.center + r * math.sin(angle)
                path += f"{x} {y} L "
            path += "Z"
            center_parts.append(f'<path d="{path}" fill="{color}" opacity="0.8"/>')

        return "\n  ".join(center_parts)

    def _get_rotation(self, seed: int, archetype: str) -> float:
        """Determine rotation angle based on archetype."""
        if archetype == "chaos":
            return (seed % 360)  # Random rotation for chaos
        elif archetype == "order":
            return 0  # No rotation for perfect order
        else:
            return (seed % 8) * 45  # 45-degree increments

    def _compose_svg(self, parts: List[str], element_name: str, rotation: float) -> str:
        """Compose final SVG with all enhancements."""
        svg_content = "\n    ".join(parts)

        transform = f'transform="rotate({rotation} {self.center} {self.center})"' if rotation != 0 else ''

        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.size} {self.size}" width="100%" height="100%">
  <title>{element_name} Spell Circle</title>
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="innerGlow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <g filter="url(#glow)" {transform}>
    {svg_content}
  </g>
</svg>'''
