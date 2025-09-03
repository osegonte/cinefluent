from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import movies, segments, lessons, users  # Make sure users is imported
from app.core.config import settings

app = FastAPI(
    title="Cinefluent API",
    description="Language learning through movies",
    version="0.1.0",
)

# Configure CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes - MAKE SURE users is included
app.include_router(movies.router, prefix="/api/v1")
app.include_router(segments.router, prefix="/api/v1")
app.include_router(lessons.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")  # This line is crucial


@app.get("/")
async def root():
    return {"message": "Cinefluent API", "environment": settings.APP_ENV}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Debug route to see all available routes
@app.get("/debug/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods)
            })
    return {"routes": routes}