import json
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.location_search import LocationSearch
from app.repositories.generic import LocationSearchRepository
from app.services.ai_orchestrator import ai_orchestrator
from app.schemas.location import LocationSearchRequest, LocationSearchResponse

router = APIRouter()

@router.post("/search", response_model=List[LocationSearchResponse])
async def search_locations(
    req: LocationSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Searches for locations and POIs using Nominatim OSM. Logs query inside user history."""
    payload = {"query": req.query}
    results = await ai_orchestrator.route_request("location", payload)

    # Save to user search history database
    loc_repo = LocationSearchRepository(db)
    loc_search = LocationSearch(
        user_id=current_user.id,
        query=req.query,
        result=json.dumps(results)
    )
    await loc_repo.create(loc_search)

    return results

@router.get("/history", response_model=List[dict])
async def get_search_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves user's previous location search queries and results."""
    loc_repo = LocationSearchRepository(db)
    searches = await loc_repo.get_user_history(user_id=current_user.id)
    
    return [
        {
            "id": search.id,
            "query": search.query,
            "result": json.loads(search.result),
            "created_at": search.created_at
        }
        for search in searches
    ]
