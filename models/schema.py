from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from fastapi import File

T = TypeVar('T')

class gptModel(BaseModel):
    question: str
        
class RequestSchema(BaseModel):
    question: str
    file: bytes = File(default=None)
    

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
