# app/main.py
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
import os

from . import models
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add")
def add_todo(title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title, description=description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/update/{todo_id}")
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.completed = not todo.completed
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# For health checks (Cloud Run and other platforms)
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Special route for Cloud Run
@app.get("/_ah/health")
def cloud_run_health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
