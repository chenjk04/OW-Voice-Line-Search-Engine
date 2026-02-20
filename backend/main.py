from fastapi import FastAPI, Request, HTTPException, status
from backend.schemas import PostRequest, PostResponse
app = FastAPI()

@app.post("/api/search", response_model=PostResponse)
def search(data: PostRequest):
    search_input = data.query
# search here
    return {"results": [
        {"id": 1,
        "hero": "D.Va",
        "line": "LOL",
        "score": 34,
        "audio_url": "/"}
    ]}    


