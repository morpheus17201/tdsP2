# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "fastapi",
#   "uvicorn",
#   "requests",
#   "python-dateutil",
#   "numpy",
#   "markdown",
#   "python-multipart",
# ]
# ///

import httpx
from fastapi import HTTPException
import requests

url = "http://127.0.0.1:8000/api/"

async def ga1_q01():
    response = requests.post(url, 
        # headers={
        #          "Content-Type": "multipart/form-data",
        #      },
             data={"question":"Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below."}
             )
    
    return response
    
    
    # async with httpx.AsyncClient() as client:
    #     response = client.post(
    #         "http://127.0.0.1:8000/api/",
    #         headers={
    #             "Content-Type": "multipart/form-data",
    #         },
    #         data={"question=Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below."},
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         raise HTTPException(status_code=response.status_code, detail=response.text)
        
if __name__ == "__main__":
    import asyncio
    result =  asyncio.run(ga1_q01())
    import json
    result = json.loads(result.text)['answer']
    print(f"{type(result)=}")
    print(result)