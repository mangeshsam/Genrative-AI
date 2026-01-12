from fastapi import FastAPI, HTTPException
# from pymongo import MongoClient
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient   # motor = driver is created by mongo db driver created for high traffic api 
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
 
# connection with mongoDB 
MONGO_URI = "mongodb+srv://Mangesh_Sam_1998:sambaremangesh1234@cluster0.pk8aw0f.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
 
db = client["euron_mongoDB"]
euron_data = db["euron_Mangesh"]
 
app = FastAPI()

class eurondata(BaseModel):
    name: str
    phone: int
    city: str
    course: str
    
@app.post("/data/insert")
async def euron_data_insert_helper(data: eurondata):      # async = Non blocking function 
    try:
        result = await euron_data.insert_one(data.dict())  # wait for api system
        return str(result.inserted_id)
    except Exception as e:
        # return a helpful HTTP error if DB insert fails
        raise HTTPException(status_code=500, detail=f"DB insert failed: {e}")


def euron_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc
    

@app.get("/Extract_data/getdata")
async def get_euron_data():
    items = []
    cursor = euron_data.find({})
    async for document in cursor:
        items.append(euron_helper(document))
    return items

"""
# -----------------------------
# FASTAPI CORE
# -----------------------------
from fastapi import FastAPI, HTTPException
# FastAPI        → Framework to create APIs quickly and efficiently
# HTTPException  → Used to return proper HTTP errors (400, 404, 500, etc.)

# -----------------------------
# DATA VALIDATION
# -----------------------------
from pydantic import BaseModel
# BaseModel → Validates request/response data automatically
# Ensures correct data types and structure

# -----------------------------
# MONGODB (ASYNC DRIVER)
# -----------------------------
from motor.motor_asyncio import AsyncIOMotorClient
# AsyncIOMotorClient → Async MongoDB client
# Used for high-traffic, non-blocking APIs (best for FastAPI)

from bson import ObjectId
# ObjectId → Handles MongoDB "_id" field
# Converts MongoDB IDs to/from strings

# -----------------------------
# ENVIRONMENT & SECURITY
# -----------------------------
import os
# os → Access environment variables securely
# Used for secrets like MongoDB URI, API keys

from dotenv import load_dotenv
# load_dotenv → Loads environment variables from .env file (local development)

load_dotenv()  # Reads .env and loads values into os.environ

# -----------------------------
# APPLICATION SETUP
# -----------------------------
app = FastAPI()
# Creates FastAPI application instance

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
MONGO_URI = os.getenv("MONGO_URI")
# Reads MongoDB connection string securely from environment

client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    serverSelectionTimeoutMS=30000
)
# Creates async MongoDB client with TLS security

db = client["my_database"]
collection = db["my_collection"]

# -----------------------------
# DATA MODEL
# -----------------------------
class Student(BaseModel):
    name: str
    age: int
    course: str
# Defines request body structure and validation

# -----------------------------
# API ENDPOINT
# -----------------------------
@app.get("/Extract_data/getdata")
async def get_data():
    try:
        data = []
        cursor = collection.find({})

        async for document in cursor:
            document["_id"] = str(document["_id"])  # Convert ObjectId → string
            data.append(document)

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""