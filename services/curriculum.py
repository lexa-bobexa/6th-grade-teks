from typing import Dict, List, Any
from services.mastery import MasteryService


class CurriculumService:
    def __init__(self, mastery_service: MasteryService):
        self.mastery_service = mastery_service
        # Define skill prerequisites and sequencing
        self.skill_dependencies = {
            "6.2": [],  # Rational numbers - no prerequisites
            "6.4": ["6.2"],  # Proportionality needs rational numbers
            "6.7B": ["6.2"],  # Expressions/equations needs rational numbers
            "6.8B": [],  # Geometry - independent
            "6.9A": ["6.2", "6.7B"],  # One-step equations needs both
        }
        
        # Define difficulty progression rules
        self.difficulty_rules = {
            "step_up_after": 3,  # Correct answers in a row
            "step_down_after": 2,  # Incorrect answers in a row
            "max_difficulty": 5,
            "min_difficulty": 1
        }
    
    def get_next_skill(self, user_skills: List[str]) -> str | None:
        """Determine the next skill to practice based on mastery and prerequisites."""
        # Get all available skills
        all_skills = list(self.skill_dependencies.keys())
        
        # Find skills that are unlocked (prerequisites met)
        unlocked_skills = []
        for skill in all_skills:
            if self._is_skill_unlocked(skill, user_skills):
                unlocked_skills.append(skill)
        
        if not unlocked_skills:
            return "6.2"  # Start with rational numbers
        
        # Prioritize skills that need work
        for skill in unlocked_skills:
            mastery = self.mastery_service.get_mastery(skill)
            if not mastery or mastery.score < 0.7:  # Not yet proficient
                return skill
        
        # If all skills are proficient, return the first one for review
        return unlocked_skills[0]
    
    def get_difficulty(self, teks: str, recent_performance: List[bool]) -> int:
        """Determine difficulty level based on recent performance."""
        if not recent_performance:
            return 2  # Start at medium difficulty
        
        # Count consecutive correct/incorrect
        last_result = recent_performance[-1]
        consecutive = 1
        
        for i in range(len(recent_performance) - 2, -1, -1):
            if recent_performance[i] == last_result:
                consecutive += 1
            else:
                break
        
        # Get current difficulty (simplified - would need to track this)
        current_difficulty = 2
        
        # Step up if enough consecutive correct
        if last_result and consecutive >= self.difficulty_rules["step_up_after"]:
            return min(current_difficulty + 1, self.difficulty_rules["max_difficulty"])
        
        # Step down if enough consecutive incorrect
        if not last_result and consecutive >= self.difficulty_rules["step_down_after"]:
            return max(current_difficulty - 1, self.difficulty_rules["min_difficulty"])
        
        return current_difficulty
    
    def _is_skill_unlocked(self, skill: str, user_skills: List[str]) -> bool:
        """Check if a skill is unlocked based on prerequisites."""
        prerequisites = self.skill_dependencies.get(skill, [])
        
        for prereq in prerequisites:
            if prereq not in user_skills:
                return False
            
            # Check if prerequisite is mastered
            mastery = self.mastery_service.get_mastery(prereq)
            if not mastery or mastery.score < 0.7:
                return False
        
        return True
    
    def get_skill_sequence(self) -> List[str]:
        """Get the recommended sequence of skills."""
        # This is a simplified topological sort
        sequence = []
        remaining = set(self.skill_dependencies.keys())
        
        while remaining:
            # Find skills with no unmet prerequisites
            ready = []
            for skill in remaining:
                prereqs = self.skill_dependencies.get(skill, [])
                if all(prereq in sequence for prereq in prereqs):
                    ready.append(skill)
            
            if not ready:
                # Fallback: add remaining skills in arbitrary order
                sequence.extend(remaining)
                break
            
            # Add the first ready skill
            next_skill = ready[0]
            sequence.append(next_skill)
            remaining.remove(next_skill)
        
        return sequence
