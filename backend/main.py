from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

@app.post("/test-embedding")
def test_embedding(input: TextInput):
    embedding = model.encode(input.text, convert_to_tensor=True)
    return {
        "message": "Embedding successful",
        "vector_length": embedding.shape[0]
    }
