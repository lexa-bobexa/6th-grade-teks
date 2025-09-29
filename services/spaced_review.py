from typing import Dict, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class ReviewItem:
    teks: str
    item_id: str
    due_at: datetime
    priority: int  # 1 = high, 2 = medium, 3 = low


class SpacedReviewService:
    def __init__(self):
        # Spaced repetition intervals (in days)
        self.intervals = [1, 3, 7, 21, 60]
        self.review_items: List[ReviewItem] = []
    
    def schedule_review(self, teks: str, item_id: str, mastery_score: float, 
                       last_reviewed: datetime = None) -> ReviewItem:
        """Schedule a review item based on mastery and previous reviews."""
        if last_reviewed is None:
            last_reviewed = datetime.now()
        
        # Determine interval based on mastery score
        if mastery_score >= 0.9:
            interval_days = self.intervals[-1]  # 60 days
            priority = 3
        elif mastery_score >= 0.7:
            interval_days = self.intervals[3]  # 21 days
            priority = 2
        elif mastery_score >= 0.5:
            interval_days = self.intervals[2]  # 7 days
            priority = 2
        else:
            interval_days = self.intervals[0]  # 1 day
            priority = 1
        
        due_at = last_reviewed + timedelta(days=interval_days)
        
        review_item = ReviewItem(
            teks=teks,
            item_id=item_id,
            due_at=due_at,
            priority=priority
        )
        
        self.review_items.append(review_item)
        return review_item
    
    def get_due_reviews(self, limit: int = 10) -> List[ReviewItem]:
        """Get review items that are due now."""
        now = datetime.now()
        due_items = [
            item for item in self.review_items
            if item.due_at <= now
        ]
        
        # Sort by priority (1 = high priority first)
        due_items.sort(key=lambda x: x.priority)
        
        return due_items[:limit]
    
    def get_reviews_for_skill(self, teks: str) -> List[ReviewItem]:
        """Get all review items for a specific skill."""
        return [item for item in self.review_items if item.teks == teks]
    
    def mark_reviewed(self, item_id: str, correct: bool):
        """Mark a review item as completed and reschedule if needed."""
        # Find and remove the item
        for i, item in enumerate(self.review_items):
            if item.item_id == item_id:
                del self.review_items[i]
                break
        
        # If correct, schedule next review with longer interval
        if correct:
            # This would typically reschedule with a longer interval
            pass
    
    def get_review_schedule(self) -> Dict[str, List[ReviewItem]]:
        """Get all scheduled reviews grouped by skill."""
        schedule = {}
        for item in self.review_items:
            if item.teks not in schedule:
                schedule[item.teks] = []
            schedule[item.teks].append(item)
        
        return schedule
