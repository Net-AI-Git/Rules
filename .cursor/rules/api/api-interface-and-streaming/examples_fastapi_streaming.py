"""
Minimal FastAPI app with SSE streaming and rate limiting.
Reference: RULE.mdc api-interface-and-streaming.
Run: uvicorn examples_fastapi_streaming:app --reload

Recommended: install uvicorn[standard] for best performance and reload (see @uvicorn-asgi-server).
"""
from __future__ import annotations

import asyncio
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Rate limiting: use slowapi or fastapi-limiter in real projects.
# This example shows the pattern; add: pip install slowapi
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    HAS_SLOWAPI = True
except ImportError:
    HAS_SLOWAPI = False

app = FastAPI(title="Agent API", description="Example with SSE and rate limiting")

if HAS_SLOWAPI:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ChatRequest(BaseModel):
    """Request body for chat endpoint (Pydantic model)."""
    message: str
    max_tokens: int = 256


async def stream_tokens(message: str) -> AsyncIterator[str]:
    """Simulate token streaming (SSE-style chunks)."""
    for word in message.split():
        yield f"event: token\ndata: {word}\n\n"
        await asyncio.sleep(0.05)
    yield "event: done\ndata: {}\n\n"


@app.post("/chat/stream")
async def chat_stream(
    body: ChatRequest,
    # Per-endpoint rate limit when slowapi is available:
    # _: None = Depends(limiter.limit("10/minute")),
) -> StreamingResponse:
    """Stream response using SSE-style events. Uses Pydantic for request validation."""
    return StreamingResponse(
        stream_tokens(body.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/health/live")
async def health_live() -> dict[str, str]:
    """Liveness probe: service is running."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("examples_fastapi_streaming:app", host="0.0.0.0", port=8000, reload=True)
