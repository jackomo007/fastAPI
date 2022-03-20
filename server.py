from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

tasks = {
    1: {
        "title": "read doc",
        "description": "read fastAPI documentation",
    }
}

class Task(BaseModel):
    title: str
    description: str

class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

@app.get('/')
def index():
    return {"title": "Welcome to my taks list, go to /docs to see the magic."}

@app.get('/tasks')
def get_tasks():
    return tasks

@app.get('/task/{id}')
def get_task_by_id(id: int = Path(None, description='ID of the task', gt=0)):
    return tasks[id]

@app.get('/tasks/by-title/{task_id}')
def get_task_by_title(*, task_id: int, title: Optional[str] = None, test : int):
    for task_id in tasks:
        if tasks[task_id]['title'] == title:
            return tasks[task_id]
    return {"Data": "Task not found, try another title."}

@app.post('/tasks/{task_id}')
def create_task(task_id: int, task: Task):
    if task_id in tasks:
        return {'Error': 'Task already exists'}

    tasks[task_id] = task
    return tasks[task_id]

@app.put('/tasks/{task_id}')
def update_task(task_id: int, task: UpdateTask):
    if task_id not in tasks:
        return {'Error': 'Task does not exist'}
    
    if task.title != None:
        tasks[task_id].title = task.title

    if task.description != None:
        tasks[task_id].description = task.description

    return tasks[task_id]

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    if task_id not in tasks:
        return {'Error': 'Task does not exist'}
    
    del tasks[task_id]
    return {'Message': 'Task deleted successfully'}