from typing import Union
import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"status_code": 200, "detail": "ok", "result": "working"}

if __name__ == "__main__":
    uvicorn.run('main:app', host=os.getenv('API_HOST'), port=int(os.getenv('API_PORT')), log_level="info", reload=os.getenv("DEBUG", 'False').lower() in ('true', '1', 't'))