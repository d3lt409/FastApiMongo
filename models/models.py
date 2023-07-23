from pydantic import Field, BaseModel
from typing import Optional, Union
from bson.objectid import ObjectId

class PyObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not cls.is_valid(v):
            raise ValueError(f"{v} is not a valid ObjectId")
        else:
            return str(v)
        
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Task(BaseModel):
    id:Union[PyObjectId, str, ObjectId] = Field(...,alias="_id", default_factory=PyObjectId)
    title:str
    description:Optional[str] = None
    done:bool = False

    class Config:
        
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed=True
    
class UpdateTask(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
    done:bool = False

    class Config:
        
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed=True