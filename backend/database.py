import motor.motor_asyncio
from decouple import config
from bson.objectid import ObjectId

MONGO_DETAILS = config('mongoURI')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.Series
basic_collection = db.get_collection("basicDetails")

# helper functions
def series_helper(series)->dict:
    return {
        "id": str(series["_id"]),
        "name": series["name"],
        "source": series["source"],
        "link": series["link"],
    }

# CRUD Operations
async def getSeries():
    students = []
    async for student in basic_collection.find():
        students.append(series_helper(student))
    return students
    
async def addSeries(seriesData: dict)->dict:
    series = await basic_collection.insert_one(seriesData)
    newSeries = await basic_collection.find_one({"_id": series.inserted_id})
    return series_helper(newSeries)