from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .storage import save_to_blob
import datetime

app = FastAPI()

@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()
    timestamp = datetime.datetime.utcnow().isoformat()
    await save_to_blob(f"data_{timestamp}.json", data)
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/{full_path:path}")
async def serve_react_app():
    return FileResponse("app/static/index.html")