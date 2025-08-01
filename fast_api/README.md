# _FASTAPI_ 

## Install FastAPI

### 1. Vertual Environment

create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/):

```bash
python -m venv .venv
```
activate the virtual environment:
```bash
# On Windows
source .venv/Scripts/activate
```

### 2. Install FastAPI
Install FastAPI using pip:
```bash
pip install "fastapi[standard]"
```
this install including `fastapi-cloud-cli`, which allows you to deploy to [FastAPI Cloud](https://fastapicloud.com/)

## First Steps

to run the FastAPI application, you can use the `uvicorn` server:

```bash
uvicorn main:app --reload
```
or
```bash
fastapi dev main.py
```
## Interactive API docs

### **_Swagger UI_**
Now go to [api doc](http://127.0.0.1:8000/docs). to see the API documentation (FastAPI auto-generates)

- Swagger helps you:
    - **Describe your API**: What endpoints exist, what parameters they need, what responses they return.
    - **Test your API**: Through an interactive web interface.
    - **Share your API**: Other developers can understand and use it easily.



### **_postman_**
Postman is a popular API development tool used to:

- postman helps you:
    - Send requests to APIs (GET, POST, PUT, DELETE...)
    - Test API responses interactively
    - Automate testing
    - Organize APIs into collections
    - Document APIs for sharing with teams

    - collection from top right corner
    - create a new collection  (U can Rename it)
    - on variables tab, you can add variables that can be used in your requests (put the original api URL and set the variable name to any_name)
    - from the 3 dots on the right side of the collection, add a new request
    - set the URL to {{any_name}}/welcome  || click send


---

- import FastAPI
- create a FastAPI "instance"
- operation
    - create the operation (get, post, put, delete)
    - define the path operation function ("/welcome")



## operation
### create a path operation   
"Path" here refers to the last part of the URL starting from the first `/`   
- "Operation" here refers to one of the HTTP "methods".
    - POST : to create data.
    - GET : to read data.
    - PUT : to update data.
    - DELETE : to delete data.

That @something syntax in Python is called a "decorator".

### define the path operation function
```python
@app.get("/welcome")
async def welcome():
    return {"message": "Welcome to FastAPI!"}
```
- path : `/welcome`
- operation : `GET`
- function : `below the decorator @app.get("/welcome")`

# Parameters
## Path Parameters

- Path parameters are part of the URL path.
- defined in the path operation decorator using curly braces `{}`.
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
```


## Query Parameters
- defined in the function header. added to the URL after a `?`.
```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return skip+limit
```
- `skip` and `limit` are query parameters.
- can be required if they don't have a default value.
- optional if they have a default value.