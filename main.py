# fastapi_app.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import MongoClient
from routes import router  # Assuming this is where your routes are defined
from fastapi.middleware.cors import CORSMiddleware


# Initialize the FastAPI app
app = FastAPI()

# CORS middleware to allow requests from any origin
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection function
async def connectToDatabase(npk):
    db = MongoClient("mongodb+srv://jittecprojects:farmy123@cluster0.iucdg.mongodb.net/npk."+npk)
    return db

# Lifespan to manage MongoDB connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    dbHost = await connectToDatabase("users")
    app.db = dbHost.npk  # Assign the database
    app.users = app.db["users"]  # Assign the users collection
    print("startup has begun!!")
    yield
    print("shutdown has begun!!")

# Create FastAPI instance and include the router with routes
app = FastAPI(lifespan=lifespan)
app.include_router(router)  # Assuming `router` is defined in the `routes` module

# If running the FastAPI app directly, use the following block (otherwise, run via Uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)




