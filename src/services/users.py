from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    user_name: str
    real_name: str
    role : str
