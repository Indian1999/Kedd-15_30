from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import hashlib


def code_timestamp(timestamp):
    hash_object = hashlib.sha256(str(timestamp).encode())
    return hash_object.hexdigest()

ROOT_PATH = os.path.dirname(__file__)

with open(os.path.join(ROOT_PATH, "highscores.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
    
highscores = list(data.items())

"""
Ezzel rendeztük a json-t pontok szerint csökkenő sorrendbe, már nem kell
# ("sadashfkhg", {"scores": 10, "name": "asd", "timestamp": 3768358})
highscores = sorted(highscores, key=lambda x: x[1]["score"], reverse=True)

with open(os.path.join(ROOT_PATH, "highscores.json"), "w", encoding="utf-8") as f:
    json.dump(dict(highscores), f, indent=4)
"""
class HighscoreData(BaseModel):
    score: int
    username: str
    timestamp: float
    
class HighscoreEntry(BaseModel):
    entry_id: str
    data: HighscoreData
    
def save_highscore_entry(entry, highscores):
    i = 0
    while i < len(highscores):
        if highscores[i][1]["score"] < entry[1]["score"]:
            break
        i += 1
    highscores.insert(i, entry)
    
app = FastAPI()

@app.get("/")
def root():
    return dict(highscores)

@app.post("/new_highscore")
def create_new_entry(entry: HighscoreEntry, code:str):
    print(code)
    print(entry)
    server_side_code = code_timestamp(entry.data.timestamp)
    print(server_side_code)
    if code != server_side_code:
        return "Invalid hash code!"
    entry = (entry.entry_id, 
             {"score": entry.data.score, 
              "username": entry.data.username,
              "timestamp": entry.data.timestamp})
    save_highscore_entry(entry, highscores)
    with open(os.path.join(ROOT_PATH, "highscores.json"), "w", encoding="utf-8") as f:
        json.dump(dict(highscores), f, indent=4)
    return "Highscore saved!"
        
@app.get("/top{x}")
def get_top_x_scores(x: int):
    return dict(highscores[:x])