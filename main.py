from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os
from routes.nutrition_routes import router as nutrition_router

load_dotenv()

SSL_KEYFILE = os.getenv("SSL_KEYFILE")
if not SSL_KEYFILE:
    raise ValueError("SSL_KEYFILE environment variable is not set!")

SSL_CERTFILE = os.getenv("SSL_CERTFILE")
if not SSL_CERTFILE:
    raise ValueError("SSL_CERTFILE environment variable is not set!")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include nutrition routes
app.include_router(nutrition_router)

# Run the app with SSL
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8443,       
        ssl_keyfile=SSL_KEYFILE,
        ssl_certfile=SSL_CERTFILE,
        reload=True      
    )