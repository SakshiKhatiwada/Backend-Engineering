from fastapi import FastAPI, Depends
from fastapi.responses import Response
from utils import find_customer, write_customers, read_customers, update_customer, remove_customer
from schema import CustomerData, CustomerUpdate

from dependencies import create_db_and_tables, get_session
from sqlmodel import Session

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/",status_code=200)
def home_page():
    return {"message": "home page is ready to use."}

@app.post("/customers", status_code=201) # 201 created
def add_customers(data: CustomerData, session: Session = Depends(get_session)):
    # customers = read_customers()
    # customer = {"id": str(uuid4()), **data.model_dump()}
    # customers.append(customer)
    customers = write_customers(data, session)
    return customers

@app.get("/customers", status_code=200)
def list_customers(session: Session = Depends(get_session)):
    customers = read_customers(session)
    return customers

@app.get("/customers/{customer_id}", status_code=200)
def retrieve_customer(customer_id:str, session: Session = Depends(get_session)): # type hinting here because esle frontend bata data paauxa
    # customers = read_customers(session)
    return find_customer(customer_id, session)

@app.patch("/customers/{customer_id}", status_code=200) # 200 ok
def patch_customer(customer_id: str, data: CustomerUpdate, session: Session = Depends(get_session)):
    # customers = read_customers(session)
    # customer = find_customer(customer_id, session)
    # customer.update(data.model_dump(exclude_none=True))
    customer = update_customer(customer_id, data, session)
    return customer

# @app.delete("/customers/{customer_id}")
@app.delete("/customers/{customer_id}", status_code=204) # 204 no content
# status code explicitly lekhe swagger docs maa response body ko laagi thaau nai naaaune raixa.
def delete_customer(customer_id, session: Session = Depends(get_session)):
    # customers = read_customers(session)
    # customer = find_customer(customers, customer_id)
    # customers.remove(customer)
    # write_customers(customers, session)
    # customer["message"] = "Customer deleted successfully"
    # # return customer
    # return Response(status_code=204)
    
    #new logic, with sqlmodel
    remove_customer(customer_id, session)