import numpy as np
import json
import os
import requests
from dataset import vocab, answer_map

CACHE_FILE = "cache.json"

# Load or create cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

def fetch_definition(word):
    """Fetch definition from dictionary API (with caching)."""
    word_lower = word.lower()
    if word_lower in cache:
        return cache[word_lower]
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_lower}"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if isinstance(data, list) and "meanings" in data[0]:
            meanings = data[0]["meanings"]
            if meanings and "definitions" in meanings[0]:
                defs = meanings[0]["definitions"]
                if defs:
                    definition = defs[0].get("definition")
                    cache[word_lower] = definition
                    with open(CACHE_FILE, "w") as f:
                        json.dump(cache, f, indent=2)
                    return definition
        return None
    except:
        return None

def encode_question(question):
    """Convert a question into a bag-of-words vector with dictionary lookup for unknown words."""
    vector = np.zeros(len(vocab))
    words = question.lower().split()
    for i, v in enumerate(vocab):
        if v in words:
            vector[i] = 1

    # For words not in vocab, fetch definitions and encode
    for w in words:
        if w not in vocab:
            definition = fetch_definition(w)
            if definition:
                for dw in definition.lower().split():
                    if dw in vocab:
                        vector[vocab.index(dw)] = 1
    return vector

def decode_answer(class_index):
    return answer_map.get(class_index, "I don't know the answer.")
