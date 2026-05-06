from fastapi import FastAPI, Request, HTTPException, status
from backend.schemas import PostRequest, PostResponse
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()
import numpy as np
app = FastAPI()
from hero_list import HERO_LIST, safe_name
import json


@app.post("/api/search", response_model=PostResponse)
def search(data: PostRequest):
    search_input = data.query
    embedding_input = emb(search_input)
    data = []
    for hero in HERO_LIST:
        with open(f"backend/data/embedded_voicelines_json/{safe_name(hero)}_quotes.json", "r", encoding="utf-8") as f:
            hero_data = json.load(f)
            data.extend(hero_data)

    embeddings_data = np.array([line["embedding"] for line in data])
    cosine_sim_scores = np.dot(embeddings_data, embedding_input)
    
    top_indices = np.argsort(cosine_sim_scores)[-10:][::-1]
    result = []
    for index in top_indices:
        top_line = data[index].copy()
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
