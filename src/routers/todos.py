from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth_utility import decode_access_token
from src.db.database import get_db
from src.db.models import Todo, User
from src.schemas.todos import TodoCreate, TodoOut, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/", response_model=TodoOut, status_code=201)
def create_todo(
    todo: TodoCreate = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_todo = Todo(**todo.model_dump(), owner_id=user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.get("/", response_model=list[TodoOut])
def list_todos(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    completed: bool | None = Query(None),
):
    q = db.query(Todo).filter(Todo.owner_id == user.id)
    if completed is not None:
        q = q.filter(Todo.completed == completed)
    return q.all()


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(
    todo_id: int = Path(..., description="ID of the todo"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.owner_id == user.id, Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: int = Path(...),
    todo_update: TodoUpdate = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.owner_id == user.id, Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.completed = todo_update.completed
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int = Path(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.owner_id == user.id, Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Deleted"}


@router.post("/{todo_id}/attachment")
def attach_file(
    todo_id: int = Path(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.owner_id == user.id, Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    # Not actually saving the file!
    return {"filename": file.filename, "msg": "File received"}
