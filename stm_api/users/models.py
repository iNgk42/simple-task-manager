from datetime import datetime
from pydantic import BaseModel, EmailStr
from stm_api.utils import hash_password

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDb(UserBase):
    id: int
    created_at: datetime = datetime.now().isoformat(timespec='seconds')
    passwordhash: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class UserUpdate(UserCreate):
    pass
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str