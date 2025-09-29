"""
LLM decorator service for generating educational content from templates.
This is a simplified version that generates content without actual LLM calls.
"""

from typing import Dict, Any, List
import json
import random


class DecoratorLLM:
    def __init__(self):
        # Simple content templates for different item types
        self.context_templates = {
            "6.8B": [
                "A garden bed is shaped like a trapezoid.",
                "A playground has a trapezoid-shaped sandbox.",
                "A classroom has a trapezoid-shaped desk."
            ],
            "6.4": [
                "A car travels at a constant speed.",
                "A store sells items at a fixed rate.",
                "A factory produces items at a steady pace."
            ],
            "6.2": [
                "Calculate the following expression.",
                "Solve this math problem.",
                "Find the value of the expression."
            ],
            "6.7B": [
                "Look at the following mathematical expressions.",
                "Consider these algebraic statements.",
                "Examine the mathematical forms below."
            ],
            "6.9A": [
                "Solve for the unknown variable.",
                "Find the value of x.",
                "Determine the solution to the equation."
            ]
        }
        
        self.hint_templates = {
            "6.8B": [
                "Area of a trapezoid is (b1+b2)/2 × h.",
                "Add the bases first, then divide by 2.",
                "Remember: area = average of bases × height."
            ],
            "6.4": [
                "Divide total by the number of units.",
                "Unit rate means per 1 unit.",
                "Divide the total amount by the number of units."
            ],
            "6.2": [
                "Follow the order of operations.",
                "Be careful with positive and negative numbers.",
                "Double-check your arithmetic."
            ],
            "6.7B": [
                "An equation has an equals sign (=).",
                "An expression does not have an equals sign.",
                "Look for the = symbol to identify equations."
            ],
            "6.9A": [
                "Isolate the variable on one side.",
                "Use inverse operations to solve.",
                "Do the same operation to both sides."
            ]
        }
    
    def decorate_item(self, template: Dict[str, Any], params: Dict[str, Any], 
                     answer: Any) -> Dict[str, Any]:
        """Decorate a template with generated content."""
        teks = template["teks"]
        item_type = template["type"]
        
        # Generate context
        context = self._generate_context(teks, params)
        
        # Generate prompt
        prompt = self._generate_prompt(template, params)
        
        # Generate hints
        hints = self._generate_hints(teks, params)
        
        # Generate explanation
        explanation = self._generate_explanation(template, params, answer)
        
        # Generate distractors for MC items
        distractors = []
        if item_type == "mc":
            distractors = self._generate_distractors(template, params, answer)
        
        return {
            "context": context,
            "prompt": prompt,
            "hints": hints,
            "explanation": explanation,
            "distractors": distractors
        }
    
    def _generate_context(self, teks: str, params: Dict[str, Any]) -> str:
        """Generate a school-appropriate context sentence."""
        templates = self.context_templates.get(teks, ["A math problem:"])
        context = random.choice(templates)
        
        # Add specific details based on parameters
        if teks == "6.8B" and "b1" in params:
            context += f" The trapezoid has bases of {params['b1']} and {params['b2']} {params.get('units', 'units')}, and height {params['h']} {params.get('units', 'units')}."
        elif teks == "6.4" and "x" in params and "y" in params:
            context += f" The total is {params['y']} {params.get('units_y', 'units')} in {params['x']} {params.get('units_x', 'units')}."
        
        return context
    
    def _generate_prompt(self, template: Dict[str, Any], params: Dict[str, Any]) -> str:
        """Generate the student-facing prompt."""
        teks = template["teks"]
        
        if teks == "6.8B":
            units = params.get("units", "units")
            return f"Find the area of the trapezoid in square {units}."
        elif teks == "6.4":
            units_y = params.get("units_y", "units")
            units_x = params.get("units_x", "units")
            return f"What is the unit rate in {units_y} per {units_x}?"
        elif teks == "6.7B":
            return "Select all that are equations."
        elif teks == "6.9A":
            return "Solve for x."
        else:
            return template["presentation"].get("ask", "Answer the question.")
    
    def _generate_hints(self, teks: str, params: Dict[str, Any]) -> List[str]:
        """Generate hints for the item."""
        templates = self.hint_templates.get(teks, ["Think step by step."])
        return random.sample(templates, min(3, len(templates)))
    
    def _generate_explanation(self, template: Dict[str, Any], params: Dict[str, Any], 
                            answer: Any) -> str:
        """Generate explanation for the correct answer."""
        teks = template["teks"]
        
        if teks == "6.8B":
            b1, b2, h = params["b1"], params["b2"], params["h"]
            units = params.get("units", "units")
            return f"First add the bases: {b1}+{b2}={b1+b2}. Half is {(b1+b2)//2}. Multiply by height {h} to get {answer} {units}²."
        elif teks == "6.4":
            x, y = params.get("x", 1), params.get("y", 1)
            return f"Unit rate is per 1 unit: {y}/{x} = {y/x}."
        elif teks == "6.9A":
            return f"The solution is x = {answer}."
        else:
            return f"The answer is {answer}."
    
    def _generate_distractors(self, template: Dict[str, Any], params: Dict[str, Any], 
                            answer: Any) -> List[Dict[str, Any]]:
        """Generate distractors for multiple choice items."""
        if template["teks"] == "6.7B":
            forms = params.get("forms", [])
            distractors = []
            for form in forms:
                is_equation = "=" in form
                distractors.append({
                    "value": form,
                    "correct": is_equation,
                    "why": "This is an equation because it has an equals sign." if is_equation else "This is an expression, not an equation."
                })
            return distractors
        return []
    
    def cross_check_answer(self, item: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        """Cross-check an answer (simplified version)."""
        # In a real implementation, this would use a different model or method
        # to verify the answer independently
        
        correct_answer = item.get("answer")
        
        # Simple comparison
        if isinstance(user_answer, (int, float)) and isinstance(correct_answer, (int, float)):
            agree = abs(user_answer - correct_answer) < 0.001
        else:
            agree = str(user_answer) == str(correct_answer)
        
        return {
            "agree": agree,
            "answer": correct_answer,
            "reason": "Answer matches" if agree else "Answer does not match"
        }
