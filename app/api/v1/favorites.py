from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.favorite import Favorite
from app.models.prompt_history import PromptHistory

router = APIRouter()

@router.post("/{prompt_history_id}", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    prompt_history_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bookmarks a prompt history log as a favorite."""
    # Check if history exists and belongs to user
    history = await db.get(PromptHistory, prompt_history_id)
    if not history or history.user_id != current_user.id:
        raise HTTPException(
            status_code=404, 
            detail="Prompt history log not found or unauthorized access."
        )

    # Check if already favorited
    query = select(Favorite).where(
        Favorite.user_id == current_user.id,
        Favorite.prompt_history_id == prompt_history_id
    )
    res = await db.execute(query)
    if res.scalars().first():
        return {"detail": "Already bookmarked as favorite."}

    fav = Favorite(
        user_id=current_user.id,
        prompt_history_id=prompt_history_id
    )
    db.add(fav)
    await db.commit()
    return {"detail": "Added to favorites."}

@router.delete("/{favorite_id}", status_code=status.HTTP_200_OK)
async def remove_favorite(
    favorite_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Removes a bookmark from favorites."""
    fav = await db.get(Favorite, favorite_id)
    if not fav or fav.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Favorite entry not found.")

    await db.delete(fav)
    await db.commit()
    return {"detail": "Removed from favorites."}

@router.get("/", response_model=List[dict])
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all favorites bookmarks for the logged-in user."""
    query = select(Favorite).where(Favorite.user_id == current_user.id).order_by(Favorite.created_at.desc())
    res = await db.execute(query)
    favs = res.scalars().all()

    out = []
    for f in favs:
        # Resolve history data
        h = await db.get(PromptHistory, f.prompt_history_id)
        if h:
            out.append({
                "id": f.id,
                "prompt_history_id": f.prompt_history_id,
                "generator_id": h.generator_id,
                "input_payload": h.input_payload,
                "constructed_prompt": h.constructed_prompt,
                "ai_model_used": h.ai_model_used,
                "output": h.output,
                "created_at": f.created_at
            })
    return out
