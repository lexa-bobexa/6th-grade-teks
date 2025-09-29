from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class MasteryRecord:
    teks: str
    score: float  # 0.0 to 1.0
    attempts: int
    last_seen_at: datetime
    due_review_at: datetime | None = None


class MasteryService:
    def __init__(self, alpha: float = 0.2, threshold: float = 0.83, min_items: int = 15):
        self.alpha = alpha  # EWMA smoothing factor
        self.threshold = threshold  # Mastery threshold
        self.min_items = min_items  # Minimum items before mastery
        self.mastery_records: Dict[str, MasteryRecord] = {}
    
    def update_mastery(self, teks: str, correct: bool, difficulty: int = 2) -> Dict[str, Any]:
        """Update mastery score using EWMA and return mastery info."""
        if teks not in self.mastery_records:
            self.mastery_records[teks] = MasteryRecord(
                teks=teks,
                score=0.0,
                attempts=0,
                last_seen_at=datetime.now()
            )
        
        record = self.mastery_records[teks]
        record.attempts += 1
        record.last_seen_at = datetime.now()
        
        # EWMA update: new_score = alpha * observation + (1 - alpha) * old_score
        observation = 1.0 if correct else 0.0
        record.score = self.alpha * observation + (1 - self.alpha) * record.score
        
        # Calculate mastery delta
        old_score = record.score - (self.alpha * observation - self.alpha * record.score)
        mastery_delta = record.score - old_score
        
        # Set review date if not mastered
        if record.score < self.threshold:
            record.due_review_at = datetime.now() + timedelta(days=1)
        else:
            record.due_review_at = None
        
        return {
            "score": record.score,
            "attempts": record.attempts,
            "mastery_delta": mastery_delta,
            "is_mastered": record.score >= self.threshold and record.attempts >= self.min_items,
            "due_review_at": record.due_review_at
        }
    
    def get_mastery(self, teks: str) -> MasteryRecord | None:
        """Get mastery record for a TEKS."""
        return self.mastery_records.get(teks)
    
    def get_all_mastery(self) -> List[MasteryRecord]:
        """Get all mastery records."""
        return list(self.mastery_records.values())
    
    def get_skills_needing_review(self) -> List[str]:
        """Get TEKS codes that are due for review."""
        now = datetime.now()
        return [
            record.teks for record in self.mastery_records.values()
            if record.due_review_at and record.due_review_at <= now
        ]
    
    def get_mastery_level(self, teks: str) -> str:
        """Get human-readable mastery level."""
        record = self.get_mastery(teks)
        if not record:
            return "not_started"
        
        if record.score >= self.threshold and record.attempts >= self.min_items:
            return "mastered"
        elif record.score >= 0.6:
            return "developing"
        elif record.score >= 0.3:
            return "beginning"
        else:
            return "struggling"
    
    def reset_mastery(self, teks: str):
        """Reset mastery for a TEKS (for testing)."""
        if teks in self.mastery_records:
            del self.mastery_records[teks]
