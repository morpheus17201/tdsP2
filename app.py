# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "fastapi",
#   "uvicorn",
#   "requests",
#   "python-dateutil",
#   "numpy",
#   "pandas",
#   "markdown",
#   "python-multipart",
#   "bs4"
# ]
# ///

import httpx
from typing import Dict, Any
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os
import json
from typing import List
from io import BytesIO, TextIOWrapper


from base_logger import logger

# from a1 import run_datagen_script
# from a2 import format_file_with_prettier
# from a3 import count_given_weekday_in_dates
# from a4 import sort_contacts_file
# from a5 import write_most_recent_log_first_lines
# from a6 import extract_titles_from_markdown_files
# from a7 import extract_sender_email
# from a9 import get_similar_comments
# from a8 import extract_numbers_from_image
# from a10 import calculate_ticket_sales


# from tools_a import tools

from ga1 import tools, output_of_code_s

from query_gpt import query_gpt
from query_gpt import OPENAI_API_URL, OPENAI_API_KEY


now = datetime.datetime.now()


# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.post("/api/")
async def handle_request(question: str = Form(...), files: List[UploadFile] = File([])):

    print(" " * 80)
    print("=" * 80)
    print(" " * 80)

    logger.info(f"[{now}]Question received:{question}")

    file_contents = []

    if len(files) != 0:
        logger.info(f"Files received: {[file.filename for file in files]}")
        # logger.info(f"[{now}]Files received: {files}")
        try:
            for file in files:
                # Read the content of each file in memory
                file_content = await file.read()
                file_contents.append(file_content)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        logger.info(f"No files received")

    try:
        response = await query_gpt(
            question,
            tools,
            OPENAI_API_KEY=OPENAI_API_KEY,
            OPENAI_API_URL=OPENAI_API_URL + r"chat/completions",
        )

    except Exception as e:
        logger.error(f"Error occurred while querying GPT: {e}")
        raise HTTPException(status_code=404, detail="Error occurred while querying GPT")

    fname = response["name"]
    arguments = response["arguments"]
    arg_dict = json.loads(arguments)

    arg_dict_str = ", ".join([f"{k}='{v}'" for k, v in arg_dict.items()])
    print("-" * 80)
    logger.info(f"Calling function: {fname}({arg_dict_str})")

    try:
        fun = globals()[fname]
        answer = await fun(**arg_dict)
    except Exception as e:
        logger.error(
            f"Error occurred while calling the function {fname}. Error is: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Error occurred while running called the function",
        )
    print("-" * 80)

    # return JSONResponse(content={"answer": answer})
    return {"answer": answer}


from fastapi.responses import PlainTextResponse
from fastapi import Query


@app.get("/wiki")
async def wiki_entrypoint(
    country: str = Query(..., title="Country"), response_class=PlainTextResponse
):
    print("Inside wiki_entrypoint")
    from ga4 import generate_markdown_outline

    outline = await generate_markdown_outline(country)
    return outline


if __name__ == "__main__":
    import uvicorn

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    # logger.basicConfig(level="INFO", format="%(message)s\n")
    logger.debug(f"{OPENAI_API_KEY=}")

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
