from typing import Dict, List, Any
from pydantic import BaseModel

class UserRoleUpdate(BaseModel):
    role: str # user, admin, super_admin
    is_verified: bool

class AdminAnalyticsResponse(BaseModel):
    total_users: int
    total_prompts: int
    total_saved_results: int
    ai_usage_stats: Dict[str, int] # e.g. {"openai": 45, "gemini": 30, "claude": 15}
    subscriptions_count: Dict[str, int] # e.g. {"free": 100, "pro": 15}
    recent_activities: List[Dict[str, Any]]
