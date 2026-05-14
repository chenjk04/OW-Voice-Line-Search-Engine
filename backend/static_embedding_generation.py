from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

import json
from pathlib import Path

from hero_list import HERO_LIST, safe_name

BASE_DIR = Path(__file__).parent
VOICE_LINES_DIR = BASE_DIR / "data" / "voicelines_json"
EMBEDDED_VOICE_LINES_DIR = BASE_DIR / "data" / "embedded_voicelines_json"

def get_json(hero_name):
    input_file = VOICE_LINES_DIR / f"{safe_name(hero_name)}_quotes.json"
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def generate_embedding(data):
    call_input = []
    for item in data:
        call_input.append(item["line"])

    embeddings = embed_texts(call_input)
    return embeddings


def embed_texts(call_input):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input = call_input
        )
        embeddings = []
        for i in response.data:
            embeddings.append(i.embedding)

        return embeddings
    
    except Exception as e:
        print("Embedding Error", e)
        raise


def append_embedding(data, embeddings):
    for i in range(len(data)):
        data[i]["embedding"] = embeddings[i]
    
    return data


def output(hero_name, data):
    output_file = EMBEDDED_VOICE_LINES_DIR / f"{safe_name(hero_name)}_quotes.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return


def main():
    for hero in HERO_LIST:
        raw_data = get_json(hero)
        embeddings = generate_embedding(raw_data)
        emb_data = append_embedding(raw_data, embeddings)
        output(hero, emb_data)

    return

if (__name__ == "__main__"):
    main()
