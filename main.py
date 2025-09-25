# import json

import json
from fastapi import FastAPI, Request


from fastapi.responses import StreamingResponse

app = FastAPI()

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

                yield f"data: {json.dumps(count)}\n\n"
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
        },
    )
