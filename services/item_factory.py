import json
import random
from typing import Dict, Any, List
from pathlib import Path

from engines.solver import eval_compute
from engines.validators import moderate, check_trapezoid, check_distractors


class ItemFactory:
    def __init__(self, templates_dir: str = "content/templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_cache = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all JSON templates from the templates directory."""
        for template_file in self.templates_dir.glob("*.json"):
            with open(template_file, 'r') as f:
                template = json.load(f)
                self.templates_cache[template['id']] = template
    
    def generate_item(self, template_id: str, seed: int = None) -> Dict[str, Any]:
        """Generate a live item from a template with random parameters."""
        if template_id not in self.templates_cache:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates_cache[template_id]
        if seed is not None:
            random.seed(seed)
        
        # Generate parameters based on template constraints
        params = self._generate_params(template)
        
        # Compute the answer
        answer, meta = eval_compute(template, params)
        
        # Create the live item
        item = {
            "id": f"itm_{template['teks']}_{template_id}_{seed or random.randint(1000, 9999)}",
            "teks": template["teks"],
            "type": template["type"],
            "seed": seed or random.randint(1000, 9999),
            "params": params,
            "stimulus": self._create_stimulus(template, params),
            "prompt": self._create_prompt(template, params),
            "options": None,
            "answer": answer,
            "answer_equivalents": [float(answer) if isinstance(answer, (int, float)) else answer],
            "answer_format": template["answer_format"],
            "hints": self._create_hints(template, params),
            "explanation": self._create_explanation(template, params, answer),
            "difficulty": template["difficulty"],
            "tags": self._extract_tags(template),
            "safety": {"moderation_passed": True}
        }
        
        # Add options for multiple choice
        if template["type"] == "mc":
            item["options"] = self._create_mc_options(template, params, answer)
        
        # Validate the generated item
        if not self._validate_item(item, template):
            raise ValueError("Generated item failed validation")
        
        return item
    
    def _generate_params(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Generate random parameters based on template constraints."""
        params = {}
        template_params = template.get("params", {})
        
        for key, value in template_params.items():
            if isinstance(value, dict):
                if "min" in value and "max" in value:
                    params[key] = random.randint(value["min"], value["max"])
                elif "choices" in value:
                    params[key] = random.choice(value["choices"])
            elif isinstance(value, list):
                params[key] = random.choice(value)
            else:
                params[key] = value
        
        # Special handling for trapezoid constraints
        if template["teks"] == "6.8B":
            b1 = params.get("b1_min", 4)
            b2 = params.get("b2_min", 6) 
            h = params.get("h_min", 3)
            params["b1"] = random.randint(b1, params.get("b1_max", 14))
            params["b2"] = random.randint(b2, params.get("b2_max", 18))
            params["h"] = random.randint(h, params.get("h_max", 9))
            params["units"] = random.choice(params.get("units", ["cm", "m"]))
        
        return params
    
    def _create_stimulus(self, template: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Create the stimulus (diagram, context) for the item."""
        stimulus = {}
        
        if template["teks"] == "6.8B":  # Trapezoid
            from engines.svg_renderers import render_trapezoid
            stimulus["diagram"] = {
                "shape": "trapezoid",
                "b1": params["b1"],
                "b2": params["b2"], 
                "h": params["h"],
                "units": params["units"],
                "svg": render_trapezoid(params["b1"], params["b2"], params["h"], params["units"])
            }
            stimulus["context"] = f"A garden bed is shaped like a trapezoid with bases {params['b1']} and {params['b2']} {params['units']}, and height {params['h']} {params['units']}."
        
        return stimulus
    
    def _create_prompt(self, template: Dict[str, Any], params: Dict[str, Any]) -> str:
        """Create the student-facing prompt."""
        if template["teks"] == "6.8B":
            return f"Find the area of the trapezoid in square {params['units']}."
        elif template["teks"] == "6.4":
            return f"What is the unit rate in {params.get('units_y', 'units')} per {params.get('units_x', 'unit')}?"
        elif template["teks"] == "6.7B":
            return "Select all that are equations."
        elif template["teks"] == "6.9A":
            return "Solve for x."
        else:
            return template["presentation"].get("ask", "Answer the question.")
    
    def _create_hints(self, template: Dict[str, Any], params: Dict[str, Any]) -> List[str]:
        """Create hints for the item."""
        if template["teks"] == "6.8B":
            return [
                "Area of a trapezoid is (b1+b2)/2 × h.",
                "Add the bases first, then divide by 2.",
                f"Bases are {params['b1']} and {params['b2']}, height is {params['h']}."
            ]
        elif template["teks"] == "6.4":
            return [
                "Divide total by the number of units.",
                f"Divide {params.get('y', 'total')} by {params.get('x', 'units')}."
            ]
        else:
            return ["Think step by step.", "Check your work."]
    
    def _create_explanation(self, template: Dict[str, Any], params: Dict[str, Any], answer: Any) -> str:
        """Create the explanation for the correct answer."""
        if template["teks"] == "6.8B":
            b1, b2, h = params["b1"], params["b2"], params["h"]
            return f"First add the bases: {b1}+{b2}={b1+b2}. Half is {(b1+b2)//2}. Multiply by height {h} to get {answer} {params['units']}²."
        elif template["teks"] == "6.4":
            x, y = params.get("x", 1), params.get("y", 1)
            return f"Unit rate is per 1 unit: {y}/{x} = {y/x}."
        else:
            return f"The answer is {answer}."
    
    def _extract_tags(self, template: Dict[str, Any]) -> List[str]:
        """Extract tags based on the template."""
        tags = []
        if template["teks"] == "6.8B":
            tags = ["area", "trapezoid", "formulas"]
        elif template["teks"] == "6.4":
            tags = ["proportionality", "unit_rate"]
        elif template["teks"] == "6.7B":
            tags = ["expressions", "equations"]
        elif template["teks"] == "6.9A":
            tags = ["equations", "solving"]
        return tags
    
    def _create_mc_options(self, template: Dict[str, Any], params: Dict[str, Any], answer: Any) -> List[Dict[str, Any]]:
        """Create multiple choice options for MC items."""
        if template["teks"] == "6.7B":
            forms = params.get("forms", [])
            # This is a simplified version - in reality would need proper classification
            options = []
            for form in forms:
                is_equation = "=" in form
                options.append({
                    "value": form,
                    "correct": is_equation,
                    "label": "equation" if is_equation else "expression"
                })
            return options
        return []
    
    def _validate_item(self, item: Dict[str, Any], template: Dict[str, Any]) -> bool:
        """Validate the generated item."""
        # Check moderation
        texts_to_check = [item.get("prompt", ""), item.get("explanation", "")]
        if not moderate(texts_to_check):
            return False
        
        # Check trapezoid constraints
        if template["teks"] == "6.8B":
            if not check_trapezoid(item["params"]):
                return False
        
        # Check answer format
        if template["answer_format"]["form"] == "int":
            if not isinstance(item["answer"], int):
                return False
        
        return True
