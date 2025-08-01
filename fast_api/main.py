from fastapi import FastAPI # import FastAPI
app = FastAPI() # create a FastAPI "instance"


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Path parameters =====================================================

@app.get("/items/{item_id}")   # http://127.0.0.1:8000/items/5
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/say/{skip}") # /say/50  || required  , ?limit=20 || optional
async def say(skip: int , limit: int = 10):
    return skip+limit

@app.get("/say2/{skip}") # /say/50 , ?limit=20 || required
async def say(skip:int, limit: int):
    return skip+limit


@app.get("/items1/{item_id}")  # items1/5 (item_id is a path parameter || required)
async def read_user_item(item_id: str, needy: str): ## items1/5?needy=hello || needy is a query parameter || required
    item = {"item_id": item_id, "needy": needy}
    return item




@app.get("/items2/{item_id}") # items2/5 (item_id is a path parameter || required)
async def read_item2(item_id: str, q: str | None = None, short: bool = False): # items2/5?q=hello&short=0 || q, short are query parameters || optional
    item = {"item_idddd": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# http://127.0.0.1:8000/items2/5?short=0





# you want the possible valid path parameter values to be predefined =========================================
from enum import Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")  
async def get_model(model_name: ModelName):
    # if model_name is ModelName.lenet:
    # if model_name == ModelName.lenet:
    # if model_name.value == "lenet":
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning"}
    if model_name == ModelName.resnet:
        return {"model_name": model_name, "message": "Computer Vision"}
    return {"model_name": model_name, "message": "Image Processing"}



# uvicorn main:app --reload






