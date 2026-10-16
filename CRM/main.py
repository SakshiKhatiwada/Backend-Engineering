from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from utils import find_customer, write_customers, read_customers
from schema import CustomerData, CustomerUpdate
from uuid import uuid4

app = FastAPI()

@app.get("/",status_code=200)
def home_page():
    return {"message": "home page is ready to use."}

@app.post("/customers", status_code=201) # 201 created
def add_customers(data: CustomerData):
    customers = read_customers()
    customer = {"id": str(uuid4()), **data.model_dump()}
    customers.append(customer)
    write_customers(customers)
    return customer

@app.get("/customers", status_code=200)
def list_customers():
    customers = read_customers()
    return customers

@app.get("/customers/{customer_id}", status_code=200)
def retrieve_customer(customer_id:str): # type hinting here because esle frontend bata data paauxa
    customers = read_customers()
    return find_customer(customers, customer_id)

@app.patch("/customers/{customer_id}", status_code=200) # 200 ok
def update_customer(customer_id: str, data: CustomerUpdate):
    customers = read_customers()
    customer = find_customer(customers, customer_id)
    customer.update(data.model_dump(exclude_none=True))
    write_customers(customers)
    return customer

# @app.delete("/customers/{customer_id}")
@app.delete("/customers/{customer_id}", status_code=204) # 204 no content
# status code explicitly lekhe swagger docs maa response body ko laagi thaau nai naaaune raixa.
def delete_customer(customer_id):
    customers = read_customers()
    customer = find_customer(customers, customer_id)
    customers.remove(customer)
    write_customers(customers)
    customer["message"] = "Customer deleted successfully"
    # return customer
    return Response(status_code=204)