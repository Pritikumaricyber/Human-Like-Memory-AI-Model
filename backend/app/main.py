from fastapi import FastAPI

app = FastAPI(title="Human-like Memory API")


@app.get("/")
def root():
    return {
        "message": "Human-like Memory API is running!",
        "status": "success"
    }