from fastapi import FastAPI, Header, Response, HTTPException
import functools
import inspect
import json
from pydantic import BaseModel
import typing

from animals import repository
from animals import config as conf
from animals.fixture import manager as fixture
from animals.repository import import_all

class StateRequest(BaseModel):
  consumer: typing.Optional[str]
  state: typing.Optional[str]

class Location(BaseModel):
  description: str
  country: str
  post_code: int

class Eligibility(BaseModel):
  available: bool
  previously_married: bool

class Animal(BaseModel):
  first_name: str
  last_name: str
  animal: str
  age: int
  available_from: str
  gender: str
  location: Location
  eligibility: Eligibility
  interests: typing.List[str]

app = FastAPI()

def assert_authorized(authorization, routne=None):
  auth_token = None
  if authorization:
    auth_parts = authorization.split(' ', 2)
    if len(auth_parts) > 1:
      auth_token = auth_parts[1]
  if (auth_token not in conf.valid_tokens):
    raise HTTPException(status_code=401, detail="Request is not authorized.")

def make_default_response(data):
  response = Response(content = json.dumps(data), media_type="application/json; charset=utf-8")
  return response

@app.post("/fixture")
async def set_state(state: StateRequest):
  message = fixture.set(state.state)
  return { 'message': message }

@app.get("/animals")
async def get_animals(response: Response):
  return make_default_response(repository.list())

@app.get("/animals/available")
async def get_available_animals(response: Response, 
      authorization: typing.Optional[str] = Header(None)):
  assert_authorized(authorization, inspect.currentframe().f_code.co_name)
  return make_default_response(repository.list_available())

@app.get("/animals/{animal_id}")
async def get_animal(response: Response, animal_id):
  data = repository.get(animal_id)
  if not data:
    raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found.")
  return make_default_response(data)

@app.post("/animals")
async def post_animal(response: Response, animal: Animal):
  return make_default_response(repository.add(animal))
