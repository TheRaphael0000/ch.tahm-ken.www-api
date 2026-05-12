from fastapi import FastAPI, Request, Response
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .challenges import challenges_player_data
from .decay_calendar import decay_calendar

app = FastAPI()
limiter = Limiter(key_func=get_remote_address, storage_uri=f"redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/n")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def root():
    return {"version": os.getenv("VERSION")}

@app.get("/player_data/{region}/{gameNamesTags}")
@limiter.limit("15/minute")
def challenges_player_data_route(request: Request, region:str, gameNamesTags: str):
    return challenges_player_data(region, gameNamesTags)

@app.get("/decay_calendar/{region}/{gameNameTag}")
def decay_calendar_route(request: Request, region:str, gameNameTag: str):
    ics_content = decay_calendar(region, gameNameTag)
    return Response(content=ics_content, media_type="text/calendar")