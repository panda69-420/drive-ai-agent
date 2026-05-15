from fastapi import FastAPI
from agent import generate_drive_query
from drive_search import search_drive

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Drive AI Agent Backend Running"}


@app.get("/chat")
def chat(user_input: str):

    drive_query = generate_drive_query(user_input)

    results = search_drive(drive_query)

    return {
        "user_input": user_input,
        "generated_query": drive_query,
        "results": results
    }