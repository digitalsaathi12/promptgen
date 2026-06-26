from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, require_admin
from app.models.user import User
from app.models.prompt_template import PromptTemplate
from app.schemas.prompt import PromptCreate, PromptOut, PromptUpdate

router = APIRouter()

@router.get("/", response_model=List[PromptOut])
async def list_templates(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Lists all configured prompt templates. (Admin only)"""
    query = select(PromptTemplate)
    res = await db.execute(query)
    return list(res.scalars().all())

@router.get("/{template_id}", response_model=PromptOut)
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Retrieves details of a specific prompt template. (Admin only)"""
    template = await db.get(PromptTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Prompt template not found.")
    return template

@router.post("/", response_model=PromptOut, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_in: PromptCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Creates a new prompt template. (Admin only)"""
    template = PromptTemplate(
        generator_id=template_in.category, # maps category field as generator_id slug
        name=template_in.title,
        role_text="Expert AI Assistant",
        objective_text=template_in.description or "Help users",
        constraints=template_in.tags or "",
        body_template=template_in.prompt_text
    )
    db.add(template)
    await db.commit()
    return template

@router.delete("/{template_id}", status_code=status.HTTP_200_OK)
async def delete_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Deletes a prompt template. (Admin only)"""
    template = await db.get(PromptTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Prompt template not found.")
    await db.delete(template)
    await db.commit()
    return {"detail": "Prompt template deleted successfully."}
