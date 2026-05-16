from fastapi import FastAPI
from drive_search import search_drive
from agent import generate_drive_query

app = FastAPI()

@app.get("/chat")
def chat(user_input: str):

    try:

        drive_query = generate_drive_query(user_input)

        results = search_drive(drive_query)

        return {
            "success": True,
            "user_input": user_input,
            "generated_query": drive_query,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }