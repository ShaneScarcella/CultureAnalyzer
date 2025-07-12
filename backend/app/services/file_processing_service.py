from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import docx
import io

async def parse_file_text(file: UploadFile) -> str:
    """
    Parses the text from an uploaded file (PDF or DOCX).

    Args:
        file: The uploaded file object from FastAPI.

    Returns:
        A string containing the extracted text from the file.
        
    Raises:
        HTTPException: If the file type is unsupported.
    """
    # Use the file's content type to determine how to parse it
    content_type = file.content_type
    
    # Read the file content into an in-memory stream
    contents = await file.read()
    file_stream = io.BytesIO(contents)

    if content_type == "application/pdf":
        try:
            reader = PdfReader(file_stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing PDF file: {e}")

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            document = docx.Document(file_stream)
            text = "\n".join([para.text for para in document.paragraphs])
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing DOCX file: {e}")
            
    else:
        raise HTTPException(
            status_code=415, 
            detail="Unsupported file type. Please upload a PDF or DOCX file."
        )