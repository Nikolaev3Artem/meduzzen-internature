from typing import Union
import uvicorn
from fastapi import FastAPI
import os
from routers import healthcheck

app = FastAPI()

app.include_router(healthcheck.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host=os.getenv('API_HOST'), port=int(os.getenv('API_PORT')), log_level="info", reload=os.getenv("DEBUG", 'False').lower() in ('true', '1', 't'))