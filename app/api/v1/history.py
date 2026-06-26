from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.prompt_history import PromptHistory

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_history(
    generator_id: Optional[str] = Query(None, description="Filter history by generator slug"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves paginated prompt generation history logs for the logged-in user."""
    query = select(PromptHistory).where(PromptHistory.user_id == current_user.id)
    if generator_id:
        query = query.where(PromptHistory.generator_id == generator_id)
        
    query = query.order_by(PromptHistory.created_at.desc()).offset(skip).limit(limit)
    res = await db.execute(query)
    histories = res.scalars().all()

    return [
        {
            "id": h.id,
            "generator_id": h.generator_id,
            "input_payload": h.input_payload,
            "constructed_prompt": h.constructed_prompt,
            "ai_model_used": h.ai_model_used,
            "output": h.output,
            "created_at": h.created_at
        }
        for h in histories
    ]

@router.get("/{history_id}", response_model=dict)
async def get_history_detail(
    history_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves details of a specific generation history log."""
    history = await db.get(PromptHistory, history_id)
    if not history or history.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Prompt history log not found.")
        
    return {
        "id": history.id,
        "generator_id": history.generator_id,
        "input_payload": history.input_payload,
        "constructed_prompt": history.constructed_prompt,
        "ai_model_used": history.ai_model_used,
        "output": history.output,
        "created_at": history.created_at
    }
