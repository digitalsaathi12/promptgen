import json
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.competitor_report import CompetitorReport
from app.repositories.generic import CompetitorReportRepository
from app.services.ai_orchestrator import ai_orchestrator
from app.schemas.competitor import CompetitorAnalysisRequest, CompetitorAnalysisResponse

router = APIRouter()

@router.post("/analyze", response_model=CompetitorAnalysisResponse)
async def analyze_competitor(
    req: CompetitorAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crawls and evaluates a competitor website URL for SEO scores, metadata keywords, social channels, and opportunities."""
    payload = {"website": req.website}
    result = await ai_orchestrator.route_request("competitor", payload)

    # Save competitor report inside database
    report_repo = CompetitorReportRepository(db)
    report_item = CompetitorReport(
        user_id=current_user.id,
        website=req.website,
        report=json.dumps(result)
    )
    await report_repo.create(report_item)

    return result

@router.get("/history", response_model=List[dict])
async def get_analysis_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves previous website competitor reports compiled by the user."""
    report_repo = CompetitorReportRepository(db)
    reports = await report_repo.get_user_reports(user_id=current_user.id)

    return [
        {
            "id": report.id,
            "website": report.website,
            "report": json.loads(report.report),
            "created_at": report.created_at
        }
        for report in reports
    ]
