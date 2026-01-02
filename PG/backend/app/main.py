from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.database import engine, Base
from app.routers.users import router as users_router
from app.routers.complaints import router as complaints_router
from app.routers.foodmenu import router as foodmenu_router
from app.routers.payments import router as payments_router

app = FastAPI(title="Smart PG Living API")

# Create tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(users_router)
app.include_router(complaints_router)
app.include_router(foodmenu_router)
app.include_router(payments_router)

# ✅ Swagger Bearer JWT configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Smart PG Living API",
        version="1.0.0",
        description="API for PG Owners and Residents",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Smart PG Backend Running"}
