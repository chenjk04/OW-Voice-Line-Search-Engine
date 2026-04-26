from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

import json

def get_json(hero_name):
    input_file = f"backend/data/voicelines_json/{hero_name}_quotes.json"
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def generate_embedding(hero_name, data):
    call_input = []
    for item in data:
        call_input.append(item["line"])

    embeddings = embed_texts(call_input)
    return embeddings


def embed_texts(call_input):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = call_input
    )
    embeddings = []
    for i in response.data:
        embeddings.append(i.embedding)

    return embeddings



    





