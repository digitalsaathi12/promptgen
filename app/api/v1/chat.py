import json
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.generated_content import GeneratedContent
from app.repositories.generic import GeneratedContentRepository
from app.services.ai_orchestrator import ai_orchestrator
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse

router = APIRouter()

@router.post("/", response_model=ChatMessageResponse)
async def chat_message(
    req: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sends a chat message to a selected AI provider, loading recent exchange context for conversation memory."""
    history_repo = GeneratedContentRepository(db)

    # 1. Fetch recent chat history turns to construct conversational memory
    recent_exchanges = await history_repo.get_user_history(
        user_id=current_user.id,
        content_type="chat",
        limit=10
    )

    # Reconstruct messages context array in ascending chronological order
    history_context = []
    for exchange in reversed(recent_exchanges):
        history_context.append({"role": "user", "content": exchange.input})
        try:
            out_data = json.loads(exchange.output)
            ans = out_data.get("response", exchange.output)
        except Exception:
            ans = exchange.output
        history_context.append({"role": "assistant", "content": ans})

    # 2. Call AI Router
    payload = {
        "message": req.message,
        "provider": req.provider,
        "history": history_context
    }
    result = await ai_orchestrator.route_request("chat", payload)
    response_text = result.get("response", "")

    # 3. Save exchange turn to GeneratedContent database (user history)
    chat_log = GeneratedContent(
        user_id=current_user.id,
        input=req.message,
        output=json.dumps({"response": response_text}),
        type="chat",
        provider=req.provider
    )
    await history_repo.create(chat_log)

    return {"response": response_text}

@router.get("/history", response_model=List[dict])
async def get_chat_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves user's recent chat logs."""
    history_repo = GeneratedContentRepository(db)
    exchanges = await history_repo.get_user_history(
        user_id=current_user.id,
        content_type="chat",
        limit=50
    )
    
    return [
        {
            "id": item.id,
            "user_message": item.input,
            "assistant_response": json.loads(item.output).get("response", item.output) if item.output.startswith("{") else item.output,
            "provider": item.provider,
            "created_at": item.created_at
        }
        for item in exchanges
    ]
