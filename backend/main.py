from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from contextlib import asynccontextmanager
from schemas import PostRequest, PostResponse
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from hero_list import HERO_LIST, safe_name
load_dotenv()
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi.middleware.cors import CORSMiddleware



ALL_LINE_DATA = []  # list of line obj
ALL_LINE_EMBEDDING = None  # nparray of embeddings
ALL_LINE_BY_ID = {}  # dict of {ID: line obj}
LINES_BY_HERO = {}  # dict of {hero: [list of line obj]}
EMBEDDINGS_BY_HERO = {}  # dict of {hero: nparray of embeddings}

@asynccontextmanager
async def static_emb_extraction(app: FastAPI):
    global ALL_LINE_DATA 
    global ALL_LINE_EMBEDDING 
    global ALL_LINE_BY_ID 
    global LINES_BY_HERO 
    global EMBEDDINGS_BY_HERO 
    data = []
    lines_by_hero = {}
    embeddings_by_hero = {}
    for hero in HERO_LIST:
        with open(f"backend/data/embedded_voicelines_json/{safe_name(hero)}_quotes.json", "r", encoding="utf-8") as f:
            hero_data = json.load(f)
            data.extend(hero_data)
            lines_by_hero[hero] = hero_data
            embeddings_by_hero[hero] = np.array([line["embedding"] for line in hero_data])
    
    ALL_LINE_DATA = data
    ALL_LINE_EMBEDDING = np.array([line["embedding"] for line in ALL_LINE_DATA])
    ALL_LINE_BY_ID = {line["ID"]: line for line in ALL_LINE_DATA}
    LINES_BY_HERO = lines_by_hero
    EMBEDDINGS_BY_HERO = embeddings_by_hero

    yield


app = FastAPI(lifespan= static_emb_extraction)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenAI()


@app.post("/api/search", response_model=PostResponse)
def search(data: PostRequest):
    search_input = data.query
    embedding_input = np.array(emb(search_input)[0].embedding)

    if data.hero:
        if data.hero not in HERO_LIST:
            raise HTTPException(status_code=400, detail="Invalid hero")

        result = search_result(EMBEDDINGS_BY_HERO[data.hero], LINES_BY_HERO[data.hero], embedding_input)
        return {"results": result}

    result = search_result(ALL_LINE_EMBEDDING, ALL_LINE_DATA, embedding_input)
    return {"results": result}
        

@app.get("/api/audio/{line_ID}")
def get_audio(line_ID: str):
    line = ALL_LINE_BY_ID.get(line_ID)
    if line is None:
        raise HTTPException(status_code=404, detail="Voice line not found")

    audio_url = line.get("audio_url")
    if audio_url is None:
        raise HTTPException(status_code=404, detail="Audio not available")

    request = Request(
        audio_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://overwatch.fandom.com/",
        },
    )

    try:
        with urlopen(request, timeout=10) as audio_response:
            audio = audio_response.read()
            content_type = audio_response.headers.get("Content-Type", "audio/ogg")
    except HTTPError as e:
        raise HTTPException(status_code=e.code, detail="Audio source unavailable")
    except URLError:
        raise HTTPException(status_code=502, detail="Audio source unreachable")

    return Response(
        content=audio,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )


def search_result(embeddings, lines, embedding_input):
    cosine_sim_scores = np.dot(embeddings, embedding_input)
    top_indices = np.argsort(cosine_sim_scores)[-12:][::-1]
    result = []
    for index in top_indices:
        top_line = lines[index].copy()
        del top_line["embedding"]
        top_line["score"] = float(cosine_sim_scores[index])
        result.append(top_line)

    return result

def emb(s):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input = s
        )

        return response.data
    
    except Exception as e:
        print("Embedding Error", e)
        raise
