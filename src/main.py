from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from pydantic.fields import ModelField
from typing import Type
import inspect
from fastapi import Form
from fastapi.staticfiles import StaticFiles


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
             inspect.Parameter(
                 model_field.alias,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(...) if model_field.required else Form(model_field.default),
                 annotation=model_field.outer_type_,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@as_form
class Employee(BaseModel):
    employeeId : int
    firstName : str
    firstName : str
    lastName : str
    employeePhone: str
    employeeEmail : str


employee_data = [
    {
        "employeeId": 1,
        "firstName": "Richard",
        "lastName": "Hendricks",
        "employeePhone": "(158) 389-2794",
        "employeeEmail": "richard@piedpiper.com",
    },
    {
        "employeeId": 2,
        "firstName": "Jared",
        "lastName": "Dunn",
        "employeePhone": "(518) 390-2749",
        "employeeEmail": "jared@piedpiper.com",
    },
    {
        "employeeId": 3,
        "firstName": "Erlich",
        "lastName": "Bachman",
        "employeePhone": "(815) 391-2974",
        "employeeEmail": "erlich.bachman@piedpiper.com",
    },
]

employee_data = [Employee(**item) for item in employee_data]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/employees")
async def list_employees():
    return ORJSONResponse(jsonable_encoder(employee_data))

@app.post("/add_employee")
async def add_employee(employee: Employee):
    employee_data.append(employee)

    return 200