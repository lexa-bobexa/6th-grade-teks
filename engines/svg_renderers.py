from typing import Dict, Any, List, Tuple


def render_trapezoid(b1: int, b2: int, h: int, units: str = "cm") -> str:
    """Render a trapezoid SVG with given dimensions."""
    # Calculate coordinates for trapezoid
    # b1 = bottom base, b2 = top base, h = height
    width = max(b1, b2) + 4  # Add padding
    height = h + 4
    
    # Center the trapezoid
    offset_x = 2
    offset_y = 2
    
    # Calculate trapezoid points
    # Bottom base: b1, centered
    bottom_left = offset_x
    bottom_right = offset_x + b1
    
    # Top base: b2, centered
    top_left = offset_x + (b1 - b2) // 2
    top_right = top_left + b2
    
    # Height
    top_y = offset_y
    bottom_y = offset_y + h
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <polygon points="{bottom_left},{bottom_y} {bottom_right},{bottom_y} {top_right},{top_y} {top_left},{top_y}" 
           fill="none" stroke="black" stroke-width="2"/>
  <text x="{bottom_left + b1//2}" y="{bottom_y + 15}" text-anchor="middle" font-size="12">{b1} {units}</text>
  <text x="{top_left + b2//2}" y="{top_y - 5}" text-anchor="middle" font-size="12">{b2} {units}</text>
  <text x="{offset_x - 10}" y="{top_y + h//2}" text-anchor="middle" font-size="12" transform="rotate(-90, {offset_x - 10}, {top_y + h//2})">{h} {units}</text>
</svg>'''
    return svg


def render_number_line(min_val: int = -10, max_val: int = 10, highlight: List[float] = None) -> str:
    """Render a number line SVG."""
    if highlight is None:
        highlight = []
    
    width = 400
    height = 60
    tick_height = 20
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <line x1="20" y1="{height//2}" x2="{width-20}" y2="{height//2}" stroke="black" stroke-width="2"/>
'''
    
    # Add ticks and numbers
    for i in range(min_val, max_val + 1):
        x = 20 + (i - min_val) * (width - 40) // (max_val - min_val)
        svg += f'  <line x1="{x}" y1="{height//2 - tick_height//2}" x2="{x}" y2="{height//2 + tick_height//2}" stroke="black" stroke-width="1"/>\n'
        svg += f'  <text x="{x}" y="{height//2 + tick_height + 15}" text-anchor="middle" font-size="12">{i}</text>\n'
    
    # Highlight specific points
    for val in highlight:
        if min_val <= val <= max_val:
            x = 20 + (val - min_val) * (width - 40) // (max_val - min_val)
            svg += f'  <circle cx="{x}" cy="{height//2}" r="4" fill="red"/>\n'
    
    svg += '</svg>'
    return svg


def render_coordinate_plane(min_x: int = -5, max_x: int = 5, min_y: int = -5, max_y: int = 5, points: List[Tuple[float, float]] = None) -> str:
    """Render a coordinate plane SVG."""
    if points is None:
        points = []
    
    width = 400
    height = 400
    margin = 40
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ccc" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#grid)"/>
'''
    
    # Draw axes
    center_x = width // 2
    center_y = height // 2
    svg += f'  <line x1="{margin}" y1="{center_y}" x2="{width-margin}" y2="{center_y}" stroke="black" stroke-width="2"/>\n'
    svg += f'  <line x1="{center_x}" y1="{margin}" x2="{center_x}" y2="{height-margin}" stroke="black" stroke-width="2"/>\n'
    
    # Add axis labels
    for i in range(min_x, max_x + 1):
        if i != 0:
            x = center_x + i * (width - 2*margin) // (max_x - min_x)
            svg += f'  <text x="{x}" y="{center_y + 20}" text-anchor="middle" font-size="12">{i}</text>\n'
    
    for i in range(min_y, max_y + 1):
        if i != 0:
            y = center_y - i * (height - 2*margin) // (max_y - min_y)
            svg += f'  <text x="{center_x - 20}" y="{y + 5}" text-anchor="middle" font-size="12">{i}</text>\n'
    
    # Plot points
    for x, y in points:
        if min_x <= x <= max_x and min_y <= y <= max_y:
            px = center_x + x * (width - 2*margin) // (max_x - min_x)
            py = center_y - y * (height - 2*margin) // (max_y - min_y)
            svg += f'  <circle cx="{px}" cy="{py}" r="4" fill="red"/>\n'
    
    svg += '</svg>'
    return svg
