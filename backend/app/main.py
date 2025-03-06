from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, questions, responses, admin

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["authentication"])
app.include_router(questions.router, prefix=settings.API_V1_STR, tags=["questions"])
app.include_router(responses.router, prefix=settings.API_V1_STR, tags=["responses"])
app.include_router(admin.router, prefix=settings.API_V1_STR, tags=["admin"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Learning Profile Assessment API"} 