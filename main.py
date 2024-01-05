from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.crud import get_upcoming_birthdays

app = FastAPI()

DATABASE_URL = "postgresql://postgres:admin1234@localhost/database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API routes
@app.post("/contacts/", response_model=schemas.ContactRead)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_contact(db=db, contact=contact)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts/", response_model=list[schemas.ContactRead])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_contacts(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts/{contact_id}", response_model=schemas.ContactRead)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_contact_by_id(db=db, contact_id=contact_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/contacts/{contact_id}", response_model=schemas.ContactRead)
def update_contact(contact_id: int, contact_update: schemas.ContactUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_contact(db=db, contact_id=contact_id, contact_update=contact_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/contacts/{contact_id}", response_model=schemas.ContactRead)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_contact(db=db, contact_id=contact_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts/search/", response_model=list[schemas.ContactRead])
def search_contacts(query: str, db: Session = Depends(get_db)):
    try:
        return crud.search_contacts(db=db, query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts/birthdays/upcoming/")
async def get_upcoming_birthdays_route(db: Session = Depends(get_db)):
    upcoming_birthdays = get_upcoming_birthdays(db)
    return upcoming_birthdays
