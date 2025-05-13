from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # ← 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/auth/login")
def login():
    return {"message": "Login endpoint"}

@app.post("/journal")
def create_journal_entry():
    return {"message": "Create journal entry endpoint"}