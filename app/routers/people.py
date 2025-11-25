from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_session
from app import models
from app.schemas.common import PersonCreate, PersonRead

router = APIRouter(prefix="/people", tags=["people"])


def _load_person(db: Session, person_id: str) -> models.Person:
    person = db.get(models.Person, person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.get("/", response_model=list[PersonRead])
def list_people(db: Session = Depends(get_session)):
    return db.execute(select(models.Person)).scalars().all()


@router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(payload: PersonCreate, db: Session = Depends(get_session)):
    person = models.Person(**payload.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.get("/{person_id}", response_model=PersonRead)
def get_person(person_id: str, db: Session = Depends(get_session)):
    return _load_person(db, person_id)


@router.put("/{person_id}", response_model=PersonRead)
def update_person(person_id: str, payload: PersonCreate, db: Session = Depends(get_session)):
    person = _load_person(db, person_id)
    for field, value in payload.dict().items():
        setattr(person, field, value)
    db.commit()
    db.refresh(person)
    return person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: str, db: Session = Depends(get_session)):
    person = _load_person(db, person_id)
    db.delete(person)
    db.commit()
    return None
