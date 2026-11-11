from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")  
def hello_func():  
  return "Hello World"  
  
@app.get("/data")  
def get_data():  
  return {"data": "This is important data"} 