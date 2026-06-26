from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.api.deps import get_db, require_admin, require_super_admin
from app.models.user import User
from app.models.prompt import Prompt
from app.models.subscription import Subscription
from app.models.generated_content import GeneratedContent
from app.models.saved_result import SavedResult
from app.repositories.user import UserRepository
from app.repositories.generic import SubscriptionRepository, PromptRepository
from app.schemas.user import UserOut
from app.schemas.admin import UserRoleUpdate, AdminAnalyticsResponse

router = APIRouter()

@router.get("/users", response_model=List[UserOut])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(require_admin), # Implicitly checks admin status
    current_admin: User = Depends(require_admin)
):
    """Lists all users registered in the system (Admin only)."""
    user_repo = UserRepository(db)
    return await user_repo.get_multi(skip=skip, limit=limit)

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_super_admin) # Only super admin can edit roles
):
    """Updates user roles or verification status (Super Admin only)."""
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Super Admin cannot modify their own role.")

    updated_data = {"role": role_update.role, "is_verified": role_update.is_verified}
    return await user_repo.update(user, updated_data)

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_super_admin)
):
    """Deletes a user and their associated data from the system (Super Admin only)."""
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Super Admin cannot delete their own account.")

    await user_repo.remove(user_id)
    return {"detail": "User account and all associated data deleted successfully."}

@router.get("/analytics", response_model=AdminAnalyticsResponse)
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Aggregates platform statistics, including AI API usage distributions and subscription breakdowns (Admin only)."""
    # 1. Total users
    res_users = await db.execute(select(func.count(User.id)))
    total_users = res_users.scalar_one()

    # 2. Total prompts
    res_prompts = await db.execute(select(func.count(Prompt.id)))
    total_prompts = res_prompts.scalar_one()

    # 3. Total saved results
    res_saved = await db.execute(select(func.count(SavedResult.id)))
    total_saved = res_saved.scalar_one()

    # 4. Subscription counts by plan type
    sub_query = select(Subscription.plan, func.count(Subscription.id)).group_by(Subscription.plan)
    sub_results = await db.execute(sub_query)
    subscriptions_count = {row[0]: row[1] for row in sub_results.all()}
    
    # Fill defaults if missing
    for plan in ["free", "pro", "enterprise"]:
        if plan not in subscriptions_count:
            subscriptions_count[plan] = 0

    # 5. AI usage stats (Group by type and provider in generated_content logs)
    usage_query = select(GeneratedContent.provider, func.count(GeneratedContent.id)).group_by(GeneratedContent.provider)
    usage_results = await db.execute(usage_query)
    ai_usage_stats = {row[0] if row[0] else "unknown": row[1] for row in usage_results.all()}

    # 6. Recent activity logs
    recent_query = select(GeneratedContent).order_by(GeneratedContent.created_at.desc()).limit(10)
    recent_results = await db.execute(recent_query)
    recent_activities = []
    
    for act in recent_results.scalars().all():
        recent_activities.append({
            "id": act.id,
            "user_id": act.user_id,
            "type": act.type,
            "provider": act.provider,
            "created_at": act.created_at.isoformat()
        })

    return {
        "total_users": total_users,
        "total_prompts": total_prompts,
        "total_saved_results": total_saved,
        "ai_usage_stats": ai_usage_stats,
        "subscriptions_count": subscriptions_count,
        "recent_activities": recent_activities
    }
