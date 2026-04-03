import logging
import uvicorn
import sys

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.responses import HTMLResponse

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_connector
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.images import router as images_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    logging.info("FastAPI Cache initialized")
    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(images_router)

#Обработчик для перехвата 422 статус-кода (Ошибка валидации Pydantic)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content="Проверьте правильность вводимого email-адреса"
    )


@app.get("/", response_class=HTMLResponse, tags=["Главная страница документации"])
def home():
    return """
    <h1>Выберите тип документации</h1>
    <h2><a href="https://booking-fastapi-project.ru/docs">Swagger UI</a><br></h2>
    <h2><a href="https://booking-fastapi-project.ru/redoc">ReDoc</a></h2>
    """

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
