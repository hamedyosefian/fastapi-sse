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
            # Send initial heartbeat
            yield ": heartbeat\n\n".encode("utf-8")

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
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Proxy-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control",
            "Content-Type": "text/event-stream; charset=utf-8",
            "Transfer-Encoding": "chunked",
        },
    )


@app.get("/test-sse")
async def test_sse(request: Request) -> StreamingResponse:
    """Simple SSE endpoint for testing with Postman"""
    import asyncio

    async def event_stream():
        count = 1
        try:
            # Send initial heartbeat to establish connection
            yield ": heartbeat\n\n".encode("utf-8")

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
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Proxy-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Content-Type": "text/event-stream; charset=utf-8",
            "Transfer-Encoding": "chunked",
        },
    )


@app.get("/postman-test")
async def postman_sse_test(request: Request) -> StreamingResponse:
    """SSE endpoint specifically optimized for Postman"""
    import asyncio

    async def event_stream():
        count = 1
        try:
            # Send multiple initial chunks to force Postman to start displaying
            yield "data: Starting SSE stream...\n\n".encode("utf-8")
            yield "data: This is designed for Postman\n\n".encode("utf-8")
            yield "data: Connection established\n\n".encode("utf-8")

            # Force a small delay then send padding to trigger display
            await asyncio.sleep(0.1)
            yield "data: Ready to stream data\n\n".encode("utf-8")

            while True:
                if await request.is_disconnected():
                    break

                # Create a larger chunk to force buffer flush
                data_chunk = f'data: {{"message": "Counter: {count}", "timestamp": "{asyncio.get_event_loop().time()}"}}\n\n'
                yield data_chunk.encode("utf-8")

                # Force flush by sending padding
                padding = "data: " + "." * 50 + "\n\n"
                yield padding.encode("utf-8")

                count += 1
                await asyncio.sleep(2)

                # Stop after 15 messages for testing
                if count > 15:
                    yield "data: Stream completed!\n\n".encode("utf-8")
                    break

        except asyncio.CancelledError:
            yield "data: Stream was cancelled\n\n".encode("utf-8")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, private",
            "Pragma": "no-cache",
            "Expires": "0",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Proxy-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Content-Type": "text/event-stream; charset=utf-8",
            "Content-Encoding": "identity",
        },
    )
