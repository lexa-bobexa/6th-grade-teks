#!/usr/bin/env python3
"""
Demo script to show how math problems are generated from templates.
Run: python demo_problems.py
"""

import json
from services.item_factory import ItemFactory

def main():
    print("=" * 70)
    print("🎓 TEKS Grade 6 Math Tutor - Problem Generation Demo")
    print("=" * 70)
    print()
    
    # Initialize the factory
    factory = ItemFactory()
    
    templates = [
        ("6.9A_one_step", "One-Step Equations"),
        ("6.8B_trapezoid_area", "Area of Trapezoid"),
        ("6.7B_expr_vs_eq", "Expressions vs Equations"),
        ("6.4_unit_rate", "Unit Rate"),
        ("6.2_rationals_ops", "Rational Number Operations"),
    ]
    
    for template_id, title in templates:
        try:
            print(f"📝 {title} ({template_id})")
            print("-" * 70)
            
            # Generate 3 problems from each template
            for i in range(1, 4):
                seed = 1000 + i
                item = factory.generate_item(template_id, seed=seed)
                
                print(f"\n  Problem {i} (seed: {seed}):")
                print(f"  Prompt: {item['prompt']}")
                print(f"  Answer: {item['answer']}")
                if item.get('stimulus'):
                    print(f"  Stimulus: {item['stimulus']}")
                
            print()
            print("=" * 70)
            print()
            
        except Exception as e:
            print(f"  ❌ Error generating {template_id}: {e}")
            print()
    
    print("\n✅ Demo complete! These problems are generated on-the-fly from templates.")
    print("💡 Each time you request a problem, the ItemFactory picks random values")
    print("   within the constraints defined in the template JSON files.")

if __name__ == "__main__":
    main()
