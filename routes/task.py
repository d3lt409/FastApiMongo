from fastapi import APIRouter, HTTPException
from database import get_task_id, get_all_tasks, create_new_task, get_task_title, delete_task_id, update_task_id
from models.models import Task, UpdateTask

from typing import List

task = APIRouter()

@task.get("/api/v1/tasks", response_model=List[Task])
async def get_tasks() -> Task:
    tasks = await get_all_tasks()
    return tasks

@task.post("/api/v1/tasks", response_model=Task)
async def create_task(task:Task):
    
    old_task = await get_task_title(task.title)
    if old_task:
        raise HTTPException(409,'Task already exists')
    
    new_task = await create_new_task(task.model_dump())
    if new_task :
        return new_task
    raise HTTPException(400,'Something went wrong')

@task.get("/api/v1/tasks/{id}", response_model=Task)
async def get_task(id:str):
    task = await get_task_id(id)
    if task:
        return task
    raise HTTPException(404, f'Task with id {id} does not exist')

@task.put("/api/v1/tasks/{id}", response_model=Task)
async def update_task(id:str, task:UpdateTask):
    print(task)
    task_updated = await update_task_id(id, task.model_dump())
    if task_updated:
        return task_updated
    raise HTTPException(404, f'Task with id {id} does not exist')

@task.delete("/api/v1/tasks/{id}")
async def delete_task(id):
    response = await delete_task_id(id)
    if response:
        return {'message': 'Task deleted successfully'}
    raise HTTPException(404, f'Task with id {id} does not exist')
