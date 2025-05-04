from fastapi import FastAPI,HTTPException
from typing import Optional,List, Dict, Any
from pydantic import BaseModel,Field
from enum import IntEnum
from fastapi.middleware.cors import CORSMiddleware



api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Priority(IntEnum):
    low = 1
    medium = 2
    high = 3
    
class TodoBase(BaseModel):
    todo_name: str = Field(..., title="The name of the todo item",max_length=50, min_length=3)
    todo_description: str = Field(..., title="The description of the todo item")
    priority: Optional[Priority] = Field(title="The priority of the todo item",default=Priority.low)
    completed: bool = Field(False, title="Whether the todo item is completed or not")    
    
class Todo(TodoBase):
    todo_id: int = Field(..., title="The ID of the todo item", minimum=1)
    

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, title="The name of the todo item",max_length=50, min_length=3)
    todo_description: Optional[str] = Field(None, title="The description of the todo item")
    priority: Optional[Priority] = Field( title="The priority of the todo item",default=Priority.low)
    completed: Optional[bool] = Field(False, title="Whether the todo item is completed or not")
    
class TodoCreate(BaseModel):
    todo_name: str = Field(..., title="The name of the todo item",max_length=50, min_length=3)
    todo_description: str = Field(..., title="The description of the todo item")
    priority: Optional[Priority] = Field( title="The priority of the todo item",default=Priority.low)
    completed: bool = Field(False, title="Whether the todo item is completed or not")           

class TodoDelete(TodoBase):
    todo_id: int = Field(..., title="The ID of the todo item", minimum=1)

all_todeos = [
    Todo(todo_id=1, todo_name='flutter', todo_description='Learn flutter for all', priority=Priority.high, completed=False),
    Todo(todo_id=2, todo_name='Apis', todo_description='Learn fastApis', priority=Priority.medium, completed=False),  
    Todo(todo_id=3, todo_name='Alx', todo_description='Complete the ALX milestones', priority=Priority.low, completed=False),
    Todo(todo_id=4, todo_name='walk', todo_description='Go for a walk before late ', priority=Priority.medium, completed=False),
    Todo(todo_id=5, todo_name='make phone call', todo_description='Call mum before noon', priority=Priority.high, completed=False),  
   

]

@api.get("/todo/all")
def get_all_tasks():
    return all_todeos


@api.get("/todo")
def get_task(task_name: str):
    for todo in all_todeos:
        if todo['todo_name'] == task_name:
            return todo
    raise HTTPException(status_code=404, detail="Task not found")


@api.post("/todo", response_model=Todo)
def create_task(todo: TodoCreate):
    for existing_todo in all_todeos:
        if existing_todo.todo_name == todo.todo_name:
            raise HTTPException(status_code=400, detail="Task already exists")

    todo_id = all_todeos[-1].todo_id + 1 if all_todeos else 1
    new_todo = Todo(todo_id=todo_id, **todo.dict())
    all_todeos.append(new_todo)
    return new_todo


@api.put("/todo/{todo_id}", response_model=Todo)
def update_task(todo_id: int, todo: TodoUpdate):
    for idx, existing_todo in enumerate(all_todeos):
        if existing_todo.todo_id == todo_id:
            updated_data = existing_todo.dict()
            updates = todo.dict(exclude_unset=True)
            updated_data.update(updates)
            updated_todo = Todo(**updated_data)
            all_todeos[idx] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Task not found")


@api.delete("/todo/{todo_id}")
def delete_task(todo_id: int):
    for existing_todo in all_todeos:
        if existing_todo.todo_id == todo_id:
            all_todeos.remove(existing_todo)
            return {"detail": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

