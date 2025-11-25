from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.session import Base, engine
from app.routers import rooms, people
from app.routers import admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Occupancy & Face Management")

app.include_router(rooms.router)
app.include_router(people.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {"message": "Surveillance system API is running."}


app.mount("/static", StaticFiles(directory="app/static"), name="static")
