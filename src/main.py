from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path
from fastapi.responses import HTMLResponse
sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2><a href="http://127.0.0.1:8000/docs">Documentation</a><br></h2>
    <h2><a href="http://127.0.0.1:8000/redoc">ReDoc</a></h2>
    """



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)