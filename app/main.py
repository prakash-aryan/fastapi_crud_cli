from fastapi import FastAPI
import os
from dotenv import load_dotenv

from app.database import engine
from app.models.item import Item
import app.routes.item as item_routes

# Create tables in the database
from app.database import Base
Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="FastAPI CRUD App with MySQL")

# Include routers
app.include_router(item_routes.router)

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI CRUD App with MySQL"}

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run("app.main:app", host=host, port=port, reload=True)