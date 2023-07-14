from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class Numbers (BaseModel):
   a : int
   b : int


@app.get("/")
def root ():
   return {"message" : "Hello World"}


# name is a path parameter
# uppercase is a query parameter (it appears only in the function's arguments) ?uppercase=
@app.get("/{name}")
def hello_name(name: str, uppercase: bool = False):
   name = name.upper() if uppercase else name
   return {"message" : "Hello " + name}

@app.post("/sum")
def sum_numbers(numbers: Numbers):
   return {"sum" : numbers.a + numbers.a}
