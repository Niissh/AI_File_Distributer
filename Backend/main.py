from fastapi import FastAPI
from app.routers import user

app = FastAPI(title="Ai File Management")

app.include_router(user.router)

@app.on_event("startup")
def startup():
    from app.core.database import Base, engine
    Base.metadata.create_all(bind=engine)
