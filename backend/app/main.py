from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routes import auth

app = FastAPI()
app.include_router(auth.router)


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# @app.post("/auth/login")
# def login():
#     return {"message": "Login endpoint"}

# @app.post("/auth/register")
# def register():
#     return {"message": "Register endpoint"}

# @app.post("/journal")
# def create_journal_entry():
#     return {"message": "Create journal entry endpoint"}