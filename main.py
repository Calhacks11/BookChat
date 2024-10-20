from fastapi import FastAPI, File, UploadFile
import shutil
from epub_parser.epub_to_text import epub_to_chapters, get_chapter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
from llm.gemini import query_prompt

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LLMQuery(BaseModel):
    query: Union[str, None] = None



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadbook")
async def create_upload_file(file: UploadFile = File(...)):
    # Specify the path to save the file
    save_path = f'./data/{file.filename}'

    # Write the uploaded file to the local disk
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    epub_to_chapters(file.filename)
    return {"filename": file.filename, "status": "File uploaded successfully"}

@app.get("/book/{bookname}/chapter/{ch_no}")
async def read_chapter(bookname: str, ch_no: int):
    content = get_chapter(bookname, ch_no)
    return {
        "bookname": bookname,
        "ch_no": ch_no,
        "content": content
    }

@app.post("/llm-query")
async def llm_query(llm_query: LLMQuery):
    llm_response = query_prompt(llm_query.query)
    return {
        "response": llm_response
    }



