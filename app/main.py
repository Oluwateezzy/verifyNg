from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth


app = FastAPI(title="VerifyNG API", version="1.0.0")

Base.metadata.create_all(bind=engine)

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def home():
    return {"message": "Welcome to The VerifyNG API!"}
