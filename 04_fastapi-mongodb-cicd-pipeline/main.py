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