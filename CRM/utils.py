from fastapi import HTTPException
from schema import CustomerData
import json
from uuid import uuid4
from pathlib import Path

CUSTOMERS_FILE = Path(__file__).with_name("customers.json")

def find_customer(customers, customer_id):
    # Search- Linear
    for customer in customers:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer Not Found") # 404 not found

def write_customers(customers):
    with open(CUSTOMERS_FILE, "w", encoding='utf-8') as file:
        json.dump(customers, file, indent=2)
        
def read_customers():
    try:
        with open(CUSTOMERS_FILE, "r", encoding='utf-8') as file:
            customers = json.load(file)
        if not isinstance(customers, list):
            raise ValueError("Expected a list")
        return customers
    
    except FileNotFoundError:
        return []
    
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid customer JSON file") # 500 Internal Server Error