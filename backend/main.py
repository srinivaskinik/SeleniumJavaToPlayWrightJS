from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add parent directory to path to import tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.converter import SeleniumToPlaywrightConverter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConversionRequest(BaseModel):
    input_code: str
    target_language: str = "typescript"

converter = SeleniumToPlaywrightConverter()

@app.get("/")
def read_root():
    return {"status": "alive"}

@app.post("/convert")
def convert_code(request: ConversionRequest):
    try:
        converted_code = converter.convert(request.input_code)
        return {
            "success": True, 
            "converted_code": converted_code,
            "logs": converter.logs
        }
    except Exception as e:
        return {
            "success": False,
            "converted_code": "",
            "logs": [{"level": "error", "message": str(e)}]
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

