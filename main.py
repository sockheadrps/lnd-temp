from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


app = FastAPI()
app.mount(
    "/static/", StaticFiles(directory="static"),
    name="static"
)


app.mount(
    "/templates/", StaticFiles(directory="templates"),
    name="templates"
)


origins = ["*"]

# cors bullshit for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO:
# def execute_command(command):
#     """Executes a shell command and returns the output."""
#     try:
#         result = subprocess.run(shlex.split(command), capture_output=True, text=True)
#         output = result.stdout if result.stdout else result.stderr
#     except Exception as e:
#         output = str(e)
#     return Response(output, mimetype='text/plain')


@app.get("/favicon.ico")
async def favicon() -> None:
    # No current FavIcon - fix later
    raise HTTPException(status_code=403, detail="No favicon")


# serve initial client files
@app.get("/")
async def root():
    return FileResponse("templates/index.html")


# WS endpoint
@app.websocket("/ws")
async def websocket_endpoint(client_websocket: WebSocket) -> None:
    await client_websocket.accept()

    data = await client_websocket.receive()

    # Confirm initial connection with client
    # TODO: should store the WS object to gracefully disconnect when possible
    if data.get("event") == "CONNECT":
        await client_websocket.send_json({"event": "CONNECTED"})


    while True:
        data = await client_websocket.receive()
        print(data)

        # TODO: Handle incoming data from the client, listen for Start/Stop/info events, would call execute_command on the events from the client

        # TODO: If the client disconnects, remove the client from the list
        if data.get("type") == "websocket.disconnect" or data.get("event") == "DISCONNECT":
            data = {
                "event": "DISCONNECT",
            }


if __name__ == "__main__":
    uvicorn.run(app, port=8081, host="localhost")
