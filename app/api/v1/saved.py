from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.saved_result import SavedResult
from app.repositories.generic import SavedResultRepository
from app.schemas.saved import SavedResultCreate, SavedResultOut

router = APIRouter()

@router.post("/", response_model=SavedResultOut, status_code=status.HTTP_201_CREATED)
async def create_saved_result(
    result_in: SavedResultCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Saves a generated prompt, script, hook list, or competitor analysis result to user favorites list."""
    saved_repo = SavedResultRepository(db)
    saved_item = SavedResult(
        user_id=current_user.id,
        title=result_in.title,
        content=result_in.content,
        type=result_in.type
    )
    return await saved_repo.create(saved_item)

@router.get("/", response_model=List[SavedResultOut])
async def list_saved_results(
    type: Optional[str] = Query(None, description="Filter saved results by type (prompt, script, hook, analysis)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists saved results for the logged-in user, filtered optionally by type."""
    saved_repo = SavedResultRepository(db)
    return await saved_repo.get_user_saved(user_id=current_user.id, result_type=type, skip=skip, limit=limit)

@router.delete("/{saved_id}", status_code=status.HTTP_200_OK)
async def delete_saved_result(
    saved_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes an item from the user's saved results list."""
    saved_repo = SavedResultRepository(db)
    saved_item = await saved_repo.get(saved_id)
    if not saved_item or saved_item.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Saved result item not found or unauthorized access."
        )
    await saved_repo.remove(saved_id)
    return {"detail": "Saved result deleted successfully."}
