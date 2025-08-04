# from fastapi import FastAPI

# app = FastAPI()

# ============================== Swagger ==============================
# http://127.0.0.1:8000/docs || to see the API documentation (FastAPI auto-generates)

# When you create an API, Swagger helps you:
# Describe your API: What endpoints exist, what parameters they need, what responses they return.
# Test your API: Through an interactive web interface.
# Share your API: Other developers can understand and use it easily.
#================================================================================================================

# ============================== postman ==============================
# Postman is a popular API development tool used to:

# Send requests to APIs (GET, POST, PUT, DELETE...)
# Test API responses interactively
# Automate testing
# Organize APIs into collections
# Document APIs for sharing with teams
# Mock servers, generate code snippets, etc.

# collection from top right corner
# create a new collection  (U can Rename it)
# on variables tab, you can add variables that can be used in your requests (put the original api URL and set the variable name to any_name)
# from the 3 dots on the right side of the collection, add a new request
# set the URL to {{any_name}}/welcome  || click send

# @app.get("/welcome") # decorator to define a route when put /welcome after the base URL call this function
# # API routes (GET, POST, PUT, DELETE...)
# def welocome():
#     return{
#     "message": "Wel ome to the FastAPI application!"
#     }




# from dotenv import load_dotenv
# load_dotenv(".env") # this loading should ba done befor importing any other modules that use environment variables

# from src.routes.base import base_router
# from src.routes import base


# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI
from src.routes.base import base_router
from src.routes.data import data_router

app = FastAPI()

app.include_router(data_router)
app.include_router(base_router)


print("✅ Routes:")
for route in app.routes:
    print(route.path, route.name)





# uvicorn main:app --reload
