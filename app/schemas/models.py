from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True
        
    def __str__(self):
        name = self.__class__.__name__
        str_dict = self.model_dump()
        try:
            content = ",\n".join(
                [
                    f"  {k}={'exists' if isinstance(v, (bytes)) and v else v}"
                    for k, v in str_dict.items()
                ]
            )
        except Exception as e:
            content = str_dict
            print(e)
        return f"{name}(\n{content}\n)"

    def __repr__(self):
        return self.__str__()    
    

# Base model for common attributes (optional)
class TimestampedBaseModel(CustomBaseModel):
    created_at: datetime
    
# User Models
class UserBase(CustomBaseModel):
    # is_active: Optional[bool] = True
    pass


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    pass


class UserResponse(TimestampedBaseModel):
    id: int
    username: str
