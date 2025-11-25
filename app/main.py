from fastapi import FastAPI

from app.db.session import Base, engine
from app.routers import rooms, people

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Occupancy & Face Management")

app.include_router(rooms.router)
app.include_router(people.router)


@app.get("/")
def read_root():
    return {"message": "Surveillance system API is running."}
