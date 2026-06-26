from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, require_admin
from app.models.user import User
from app.models.ai_model import AIModel
from app.schemas.model import AIModelCreate, AIModelOut

router = APIRouter()

@router.get("/", response_model=List[AIModelOut])
async def list_models(db: AsyncSession = Depends(get_db)):
    """Retrieves all active registered AI models from the catalog."""
    query = select(AIModel).where(AIModel.is_active == True)
    res = await db.execute(query)
    return list(res.scalars().all())

@router.post("/", response_model=AIModelOut, status_code=status.HTTP_201_CREATED)
async def register_model(
    model_in: AIModelCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Registers a new model in the catalog. (Admin only)"""
    query = select(AIModel).where(AIModel.name == model_in.name)
    res = await db.execute(query)
    if res.scalars().first():
        raise HTTPException(status_code=400, detail="A model with this name already exists.")

    model = AIModel(
        name=model_in.name,
        provider=model_in.provider,
        is_local=model_in.is_local,
        is_active=model_in.is_active,
        default_for=model_in.default_for
    )
    db.add(model)
    await db.commit()
    return model

@router.delete("/{model_id}", status_code=status.HTTP_200_OK)
async def delete_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Deletes a model from the catalog. (Admin only)"""
    model = await db.get(AIModel, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="AI Model not found.")
    await db.delete(model)
    await db.commit()
    return {"detail": "Model deleted successfully."}
