from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from routers import ecg, auth, admin

app = FastAPI()

app.include_router(ecg.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Return validation errors as plain text."""
    return PlainTextResponse(str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/health")
async def health() -> bool:
    return True
