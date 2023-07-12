from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Employee(BaseModel):
    employeeId : int
    firstName : str
    firstName : str
    lastName : str
    employeeEmail : str


employee_data = [
    {
        "employeeId": "1",
        "firstName": "Richard",
        "lastName": "Hendricks",
        "employeePhone": "(158) 389-2794",
        "employeeEmail": "richard@piedpiper.com",
    },
    {
        "employeeId": "2",
        "firstName": "Jared",
        "lastName": "Dunn",
        "employeePhone": "(518) 390-2749",
        "employeeEmail": "jared@piedpiper.com",
    },
    {
        "employeeId": "3",
        "firstName": "Erlich",
        "lastName": "Bachman",
        "employeePhone": "(815) 391-2974",
        "employeeEmail": "erlich.bachman@piedpiper.com",
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/employees")
async def list_employees():
    return ORJSONResponse(employee_data)

@app.post("/add_employee")
async def add_employee(employee: Employee):
    print(employee.__dict__)
    return 200