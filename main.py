from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import time

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

FREE_ID = 1


@app.get('/')
async def root():
    return "Server is working"


@app.post('/post')
async def post():
    global FREE_ID
    FREE_ID += 1
    return Timestamp(id=FREE_ID, timestamp=int(time.time()))


# бросит 422 если строка на входе не в енуме
@app.get("/dog")
async def get_dog(kind: DogType):
    ans = []
    for index, dog in dogs_db.items():
        if dog.kind == kind:
            ans.append(dog)
    return ans


@app.post("/dog")
async def post_dog(dog: Dog):
    dogs_db[len(dogs_db)] = dog
    return dog


@app.get("/dog/{pk}")
async def get_dog_pk(pk: int):
    for index, dog in dogs_db.items():
        if dog.pk == pk:
            return dog
    return {}


@app.get("/dogs")
async def get_dogs():
    ans = []
    for index, dog in dogs_db.items():
        ans.append(dog)
    return ans


@app.patch("/dog/{pk}")
async def get_dog_pk(pk: int, new_dog: Dog):
    for index, dog in dogs_db.items():
        if dog.pk == pk:
            dogs_db[index] = new_dog
            return new_dog
    return {}
