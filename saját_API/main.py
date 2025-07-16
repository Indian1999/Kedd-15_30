# Szerver kódja
#pip install fastapi uvicorn
#uvicorn main:app --reload
from fastapi import FastAPI

app = FastAPI()

names = ["András", "Béla", "Cecil", "Dénes", "Elemér", "Ferenc", "Géza"]

# root végpont
@app.get("/")
def root():
    return {"Hello": "World!"}

# names végpont
@app.get("/names")
def get_names():
    return names