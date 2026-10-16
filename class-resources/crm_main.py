import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Customer Management APIs")
CUSTOMERS_FILE = Path(__file__).with_name("customers.json")


class CustomerData(BaseModel):
    fullName: str
    email: EmailStr
    phone: str | None = None


class CustomerUpdate(BaseModel):
    fullName: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


# Read customers from the JSON file.
def read_customers():
    try:
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as file:
            customers = json.load(file)
        if not isinstance(customers, list):
            raise ValueError("Expected a list of customers")
        return customers
    except FileNotFoundError:
        return []
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid customer JSON file")


# Save the updated customer list to the JSON file.
def write_customers(customers):
    with open(CUSTOMERS_FILE, "w", encoding="utf-8") as file:
        json.dump(customers, file, indent=2)


def find_customer(customers, customer_id): # Linear Search
    for customer in customers:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")


@app.get("/")
def home():
    return {"message": "Welcome to CRM APIs"}


@app.post("/customers", status_code=201)
def create_customer(data: CustomerData):
    customers = read_customers()
    customer = {"id": str(uuid4()), **data.model_dump()}
    customers.append(customer)
    write_customers(customers)
    return customer


@app.get("/customers")
def list_customer():
    return read_customers()


@app.get("/customers/{customer_id}")
def retrieve_customer(customer_id: str):
    customers = read_customers()
    return find_customer(customers, customer_id)


@app.patch("/customers/{customer_id}")
def patch_customer(customer_id: str, data: CustomerUpdate):
    customers = read_customers()
    customer = find_customer(customers, customer_id)
    customer.update(data.model_dump(exclude_none=True))
    write_customers(customers)
    return customer


@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: str):
    customers = read_customers()
    customer = find_customer(customers, customer_id)
    customers.remove(customer)
    write_customers(customers)
    return Response(status_code=204)
