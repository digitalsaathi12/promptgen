from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.location_search import LocationSearch
from app.services.location_service import location_service
from app.schemas.location import LocationSearchRequest, LocationSearchResponse

router = APIRouter()

@router.post("/search", response_model=List[LocationSearchResponse])
async def search_locations(
    req: LocationSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Searches for businesses in a specific area and logs results under location queries history."""
    try:
        leads = await location_service.get_leads(
            country=req.country,
            state=req.state,
            city=req.city,
            area=req.area,
            category=req.category,
            radius=req.radius or 1000,
            limit=req.limit or 5
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Location intelligence lookup failed: {str(e)}"
        )

    # Persist log to location_searches DB table
    search_record = LocationSearch(
        user_id=current_user.id,
        country=req.country,
        state=req.state,
        city=req.city,
        area=req.area,
        category=req.category,
        radius=req.radius or 1000,
        results_json=leads
    )
    db.add(search_record)
    await db.commit()

    return leads

@router.get("/history", response_model=List[dict])
async def list_searches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists location intelligence query searches performed by the logged-in user."""
    query = select(LocationSearch).where(LocationSearch.user_id == current_user.id).order_by(LocationSearch.created_at.desc())
    res = await db.execute(query)
    searches = res.scalars().all()
    
    return [
        {
            "id": s.id,
            "country": s.country,
            "state": s.state,
            "city": s.city,
            "area": s.area,
            "category": s.category,
            "radius": s.radius,
            "results": s.results_json,
            "created_at": s.created_at
        }
        for s in searches
    ]
