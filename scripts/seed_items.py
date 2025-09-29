#!/usr/bin/env python3
"""
Seed script to generate a batch of items for testing and caching.
"""

import json
import random
from pathlib import Path
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from services.item_factory import ItemFactory


def generate_items_batch(template_id: str, count: int = 50) -> list:
    """Generate a batch of items from a template."""
    factory = ItemFactory()
    items = []
    
    for i in range(count):
        try:
            seed = random.randint(1000, 9999)
            item = factory.generate_item(template_id, seed)
            items.append(item)
            print(f"Generated item {i+1}/{count} for {template_id}")
        except Exception as e:
            print(f"Error generating item {i+1} for {template_id}: {e}")
            continue
    
    return items


def main():
    """Generate items for all templates."""
    # Create output directory
    output_dir = Path("generated_items")
    output_dir.mkdir(exist_ok=True)
    
    # Templates to generate
    templates = [
        "6.2_rationals_ops",
        "6.4_unit_rate", 
        "6.7B_expr_vs_eq",
        "6.8B_trapezoid_area",
        "6.9A_one_step"
    ]
    
    items_per_template = 20  # Generate 20 items per template
    
    for template_id in templates:
        print(f"\nGenerating items for {template_id}...")
        items = generate_items_batch(template_id, items_per_template)
        
        # Save to file
        output_file = output_dir / f"{template_id}_items.json"
        with open(output_file, 'w') as f:
            json.dump(items, f, indent=2, default=str)
        
        print(f"Saved {len(items)} items to {output_file}")
    
    print(f"\nGenerated items saved to {output_dir}/")
    print("Total items generated:", sum(len(generate_items_batch(t, 1)) for t in templates))


if __name__ == "__main__":
    main()
