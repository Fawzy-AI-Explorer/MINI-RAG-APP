from fastapi import FastAPI

app = FastAPI()

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

@app.get("/welcome") # decorator to define a route when put /welcome after the base URL call this function
# API routes (GET, POST, PUT, DELETE...)
def welocome():
    return{
    "message": "Welcome to the FastAPI application!"
    }


# uvicorn main:app --reload --port 5000

# reload to see changes without restarting the server
# host to make it accessible from any IP address
# port to specify the port number (default is 8000, but here we set it to 5000)
