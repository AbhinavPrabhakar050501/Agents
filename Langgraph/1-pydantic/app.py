#pydantic is basically a datatype validation technique, where the annotations actually
# work unlike using @dataclasses


from pydantic import BaseModel,Field
from typing import Optional,List
class Person(BaseModel):
    name:str
    age:int
    city:str
    where:Optional[float]

person = Person(name="sa",age=24, city="f")

class New(BaseModel):
    name: str = Field(default="lol", description="")