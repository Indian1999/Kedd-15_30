# Szerver kódja
#pip install fastapi uvicorn
#uvicorn main:app --reload
#http://127.0.0.1:8000/docs#/ # Swagger dokumentáció
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    person: str = None
    description: str = None
    payout: int = None
    is_done: bool = False
    
tasks = [
    Task(person="Sanyi", description="WC pucolás", payout=100, is_done=False),
    Task(person="Gábor", description="Mosogatás", payout=50, is_done=False)
]
items = ["Tányér", "Fakanál", "Csempe"]
names = ["András", "Béla", "Cecil", "Dénes", "Elemér", "Ferenc", "Géza"]

# root végpont
@app.get("/")
def root():
    return {"Hello": "World!"}

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks")
def get_tasks():
    return tasks

@app.patch("/tasks/{person}/done")
def finish_task(person: str, is_done: bool):
    for task in tasks:
        if task.person == person:
            task.is_done = is_done
            break
    return True

# names végpont
@app.get("/names")
def get_names():
    return names

@app.get("/items")
def get_items():
    return items

@app.get("/items/{item_id}")
def get_item_by_id(id: int):
    if id < 0 or id >= len(items):
        raise HTTPException(status_code=404, detail="Item index does not exist!")
    else:
        return items[id]
    

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return item

@app.delete("/items/{id}")
def delete_item(id: int):
    if id < 0 or id >= len(items):
        raise HTTPException(status_code=404, detail="Item id does not exist!")
    else:
        item = items.pop(id)
        return {"message": f"Item {id} ({item}) deleted."}
    
@app.put("/items/{id}")
def add_item(id: int, item: str):
    items.insert(id, item)
    return {id: item}