from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the todo item")
    description: str = Field("", max_length=500, description="Description of the todo item")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    completed: bool


class TodoOut(TodoBase):
    id: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)
