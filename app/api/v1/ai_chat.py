import json
import asyncio
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.prompt_history import PromptHistory
from app.ai_providers import router as ai_router
from app.schemas.chat import ChatMessageRequest

router = APIRouter()

async def stream_chat_response(message: str, provider: str, language: str, history_context: list):
    """Async generator to stream response text word by word using Server-Sent Events."""
    # Build a chat instructions prompt
    system_prompt = (
        f"You are Digital Saathi (डिजिटल साथी), a helpful AI assistant. "
        f"Respond in language format: {language}. "
    )
    if history_context:
        system_prompt += f"Recent context turns: {json.dumps(history_context)}. "
    
    full_prompt = f"{system_prompt}\nUser Message: {message}"

    try:
        # Resolve response
        ai_resp = await ai_router.route(prompt=full_prompt, model_name=provider)
        response_text = ai_resp.text
    except Exception as e:
        response_text = f"Connection error: {str(e)}"

    # Yield words sequentially to simulate real streaming
    words = response_text.split(" ")
    for idx, word in enumerate(words):
        chunk = f" {word}" if idx > 0 else word
        data = {
            "chunk": chunk,
            "provider": provider,
            "done": idx == len(words) - 1
        }
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0.04) # brief sleep for smooth stream feel

@router.post("/stream")
async def chat_message_stream(
    req: ChatMessageRequest,
    language: str = Query("English", description="English, Hindi, Hinglish"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Starts a Server-Sent Events chat response stream. Logs turn under user history."""
    # 1. Fetch history
    query = select(PromptHistory).where(
        PromptHistory.user_id == current_user.id,
        PromptHistory.generator_id == "ai_chat"
    ).order_by(PromptHistory.created_at.desc()).limit(5)
    res = await db.execute(query)
    exchanges = res.scalars().all()
    
    history_context = []
    for ex in reversed(exchanges):
        history_context.append({"user": ex.input_payload.get("message"), "assistant": ex.output.get("response")})

    # Save prompt history asynchronously after resolving stream
    # (We log it inside database to maintain audits)
    history_item = PromptHistory(
        user_id=current_user.id,
        generator_id="ai_chat",
        input_payload={"message": req.message, "language": language},
        constructed_prompt=req.message,
        ai_model_used=req.provider or "auto",
        output={"response": "Streaming completed."}
    )
    db.add(history_item)
    await db.commit()

    return StreamingResponse(
        stream_chat_response(req.message, req.provider or "auto", language, history_context),
        media_type="text/event-stream"
    )

@router.post("/", status_code=status.HTTP_200_OK)
async def chat_message_json(
    req: ChatMessageRequest,
    language: str = Query("English"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Standard JSON chat endpoint."""
    system_prompt = f"You are Digital Saathi (डिजिटल साथी). Respond in language: {language}."
    full_prompt = f"{system_prompt}\nUser Message: {req.message}"

    ai_resp = await ai_router.route(prompt=full_prompt, model_name=req.provider or "auto")
    
    # Save history
    history_item = PromptHistory(
        user_id=current_user.id,
        generator_id="ai_chat",
        input_payload={"message": req.message, "language": language},
        constructed_prompt=full_prompt,
        ai_model_used=ai_resp.model,
        output={"response": ai_resp.text}
    )
    db.add(history_item)
    await db.commit()

    return {"response": ai_resp.text}
