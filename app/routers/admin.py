from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_session
from app import models

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def admin_home():
    return RedirectResponse(url="/admin/rooms", status_code=status.HTTP_302_FOUND)


@router.get("/rooms")
def rooms_list(request: Request, db: Session = Depends(get_session)):
    rooms = db.execute(select(models.Room)).scalars().all()
    return templates.TemplateResponse("rooms_list.html", {"request": request, "rooms": rooms})


@router.get("/rooms/new")
def rooms_new(request: Request):
    return templates.TemplateResponse("rooms_form.html", {"request": request, "room": None})


@router.post("/rooms")
def rooms_create(
    name: str = Form(...),
    capacity: int = Form(...),
    remark: str | None = Form(None),
    initial_count: int | None = Form(0),
    night_period: str | None = Form(None),
    db: Session = Depends(get_session),
):
    room = models.Room(
        name=name,
        capacity=capacity,
        remark=remark,
        initial_count=initial_count,
        night_period=night_period,
    )
    db.add(room)
    db.commit()
    return RedirectResponse(url="/admin/rooms", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/rooms/{room_id}/edit")
def rooms_edit(room_id: str, request: Request, db: Session = Depends(get_session)):
    room = db.get(models.Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return templates.TemplateResponse("rooms_form.html", {"request": request, "room": room})


@router.post("/rooms/{room_id}")
def rooms_update(
    room_id: str,
    name: str = Form(...),
    capacity: int = Form(...),
    remark: str | None = Form(None),
    initial_count: int | None = Form(0),
    night_period: str | None = Form(None),
    db: Session = Depends(get_session),
):
    room = db.get(models.Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    room.name = name
    room.capacity = capacity
    room.remark = remark
    room.initial_count = initial_count
    room.night_period = night_period
    db.commit()
    return RedirectResponse(url="/admin/rooms", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/rooms/{room_id}/delete")
def rooms_delete(room_id: str, db: Session = Depends(get_session)):
    room = db.get(models.Room, room_id)
    if room:
        db.delete(room)
        db.commit()
    return RedirectResponse(url="/admin/rooms", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/people")
def people_list(request: Request, db: Session = Depends(get_session)):
    people = db.execute(select(models.Person)).scalars().all()
    return templates.TemplateResponse("people_list.html", {"request": request, "people": people})


@router.get("/people/new")
def people_new(request: Request):
    return templates.TemplateResponse("people_form.html", {"request": request, "person": None})


@router.get("/people/{person_id}/edit")
def people_edit(person_id: str, request: Request, db: Session = Depends(get_session)):
    person = db.get(models.Person, person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return templates.TemplateResponse("people_form.html", {"request": request, "person": person})


@router.post("/people")
def people_create(
    name: str = Form(...),
    remark: str | None = Form(None),
    db: Session = Depends(get_session),
):
    person = models.Person(name=name, remark=remark)
    db.add(person)
    db.commit()
    return RedirectResponse(url="/admin/people", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/people/{person_id}")
def people_update(
    person_id: str,
    name: str = Form(...),
    remark: str | None = Form(None),
    db: Session = Depends(get_session),
):
    person = db.get(models.Person, person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    person.name = name
    person.remark = remark
    db.commit()
    return RedirectResponse(url="/admin/people", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/people/{person_id}/delete")
def people_delete(person_id: str, db: Session = Depends(get_session)):
    person = db.get(models.Person, person_id)
    if person:
        db.delete(person)
        db.commit()
    return RedirectResponse(url="/admin/people", status_code=status.HTTP_303_SEE_OTHER)
