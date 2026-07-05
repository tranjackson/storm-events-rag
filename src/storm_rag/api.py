from fastapi import FastAPI
from pydantic import BaseModel
from storm_rag.geo import load_all_events

app = FastAPI(title="Storm Events API")
_EVENTS = load_all_events()  # load once at startup

class Event(BaseModel):
       event_type: str
       damage_property_usd: float
       begin_dt: str | None

@app.get("/health")
def health() -> dict: return {"status": "ok"}

@app.get("/top-events", response_model=list[Event])
def top_events(state: str, year: int, limit: int = 5) -> list[Event]:
       df = _EVENTS
       df = df[(df["STATE"].str.upper() == state.upper()) & (df["YEAR"] == year)]
       df = df.nlargest(limit, "damage_property_usd")
       return [Event(event_type=r.event_type,
                     damage_property_usd=r.damage_property_usd,
                     begin_dt=str(r.begin_dt)) for r in df.itertuples()]