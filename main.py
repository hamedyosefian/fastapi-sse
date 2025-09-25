# import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

########################################################################
#
#
############################# FastAPI Sample ################################
#
#
########################################################################


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())


########################################################################
#
#
############################# SAMPLE - 2 ################################
#
#
########################################################################


@app.get("/counter")
async def get_messages(request: Request) -> StreamingResponse:
    import asyncio

    async def event_stream():
        count = 18
        try:
            while True:
                if await request.is_disconnected():
                    break

                # Send proper SSE format with explicit encoding
                data = f"data: {count}\n\n"
                yield data.encode("utf-8")
                count += 1

                await asyncio.sleep(3)
        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control",
            "Content-Type": "text/event-stream; charset=utf-8",
        },
    )


@app.get("/test-sse")
async def test_sse(request: Request) -> StreamingResponse:
    """Simple SSE endpoint for testing with Postman"""
    import asyncio

    async def event_stream():
        count = 1
        try:
            # Send initial connection message
            yield "data: Connected to SSE stream\n\n".encode("utf-8")

            while True:
                if await request.is_disconnected():
                    break

                # Send data with proper SSE format
                message = f"Message number: {count}"
                yield f"data: {message}\n\n".encode("utf-8")
                count += 1

                # Wait 2 seconds between messages
                await asyncio.sleep(2)

                # Stop after 10 messages for testing
                if count > 10:
                    yield "data: Stream ended\n\n".encode("utf-8")
                    break

        except asyncio.CancelledError:
            yield "data: Stream cancelled\n\n".encode("utf-8")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Content-Type": "text/event-stream; charset=utf-8",
        },
    )
