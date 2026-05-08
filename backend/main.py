from fastapi import FastAPI
from contextlib import asynccontextmanager
from schemas import PostRequest, PostResponse
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from hero_list import HERO_LIST, safe_name
load_dotenv()
import json

from fastapi.middleware.cors import CORSMiddleware



ALL_LINE_DATA = []
ALL_LINE_EMBEDDING = None

@asynccontextmanager
async def static_emb_extraction(app: FastAPI):
    global ALL_LINE_DATA
    global ALL_LINE_EMBEDDING
    data = []
    for hero in HERO_LIST:
        with open(f"backend/data/embedded_voicelines_json/{safe_name(hero)}_quotes.json", "r", encoding="utf-8") as f:
            hero_data = json.load(f)
            data.extend(hero_data)
    
    ALL_LINE_DATA = data
    ALL_LINE_EMBEDDING = np.array([line["embedding"] for line in ALL_LINE_DATA])

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
    cosine_sim_scores = np.dot(ALL_LINE_EMBEDDING, embedding_input)
    
    top_indices = np.argsort(cosine_sim_scores)[-10:][::-1]
    result = []
    for index in top_indices:
        top_line = ALL_LINE_DATA[index].copy()
        del top_line["embedding"]
        top_line["score"] = float(cosine_sim_scores[index])
        result.append(top_line)

    return {"results": result}
        


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
