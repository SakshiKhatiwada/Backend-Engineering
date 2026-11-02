from fastapi import HTTPException
from schema import CustomerUpdate
import json
# from uuid import uuid4
from pathlib import Path

from sqlmodel import Session, select
from schema import Customers

CUSTOMERS_FILE = Path(__file__).with_name("customers.json")

def find_customer(customer_id, session: Session):
    # # Search- Linear
    # for customer in customers:
    #     if customer["id"] == customer_id:
    #         return customer
    # raise HTTPException(status_code=404, detail="Customer Not Found") # 404 not found
    # customer = customers.get(customer_id)
    return session.exec(
    select(Customers).where(Customers.id == customer_id)
    ).all()

def write_customers(customers, session: Session):
    # with open(CUSTOMERS_FILE, "w", encoding='utf-8') as file:
    #     json.dump(customers, file, indent=2)
    
    db_customer = Customers.model_validate(customers)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer
        
def read_customers(session: Session):
    try:
        # with open(CUSTOMERS_FILE, "r", encoding='utf-8') as file:
        #     customers = json.load(file)
        # if not isinstance(customers, list):
        #     raise ValueError("Expected a list")
        # return customers
        customers = session.exec(select(Customers)).all()
        return customers 
    
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid customer JSON file") # 500 Internal Server Error
    
def update_customer(customer_id, customer_info: CustomerUpdate, session: Session):
    statement = select(Customers).where(Customers.id == customer_id)
    results = session.exec(statement)
    try:
        customer = results.one_or_none()
    except HTTPException:
        raise HTTPException(status_code=404, detail="customer not found")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # get through the available values and update corresponding values
    update_data = customer_info.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(customer, key, value)
        
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

def remove_customer(customer_id, session:Session):
    statement = select(Customers).where(Customers.id == customer_id)
    try:
        customer = session.exec(statement).one_or_none()
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    session.delete(customer)
    session.commit()