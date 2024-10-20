from fastapi import FastAPI, File, UploadFile
import shutil
from epub_parser.epub_to_text import epub_to_text
from fastapi.middleware.cors import CORSMiddleware

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

    return {"filename": file.filename, "status": "File uploaded successfully"}