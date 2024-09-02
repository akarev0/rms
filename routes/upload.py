import shutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.database import get_db
from common.enums import EmployeeEnglishLevel, EmployeeLevel, Position
from models.models import Employee
import pdfplumber
import pandas as pd

upload_router = APIRouter()


@upload_router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save the uploaded file
        file_location = f"files/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract data from the PDF
        data = pd.read_excel(file_location)

        # Save data to the database
        save_data_to_db(data, db)

        return {"message": "File processed and data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def save_data_to_db(df: pd.DataFrame, db: Session) -> None:
    df = df.fillna("")  # Forward fill to fill missing values
    for _, row in df.iterrows():

        try:
            db_item = Employee(
                name=row.f,
                position=Position(row.Position),
                level=EmployeeLevel(row.Level),
                english_level=EmployeeEnglishLevel(row.English),
                sales_campaign=row["Sales Campaign"],
                other_skills=row["Other skills"],
                attendance_link=row.Attendance,
            )
            db.add(db_item)
            db.flush()
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            db.close()


def extract_data_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # Parse the text to extract the required data
            parsed_data = parse_text(text)
            data.extend(parsed_data)  # Extend the list with parsed data from each page
    # Convert the list of parsed data to a DataFrame
    df = pd.DataFrame(data, columns=["content"])
    return df


def parse_text(text: str):
    # Implement your parsing logic here
    # For example, split text by lines and extract relevant information
    lines = text.split("\n")
    parsed_data = []
    for line in lines:
        # Extract relevant information from each line
        parsed_data.append([line])
    return parsed_data
