from motor.motor_asyncio import AsyncIOMotorClient
import os


mongo_url = os.getenv('MONGO_URL')

# Create MongoDB client
client = AsyncIOMotorClient(mongo_url)

# Select the database
db = client['projects']