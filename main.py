from fastapi import FastAPI, Form
from pydantic import BaseModel
from pyback import run_search
from fastapi import Request, Response
import json

from fastapi.staticfiles import StaticFiles

app = FastAPI()


class Item(BaseModel):
    sign_text: str
    lat: int
    lon: int
    time: int


@app.post("/runsearch")
async def run_search_post(request: Request):
    jj = await request.json()
    ddd = run_search(jj["sign_text"])
    return Response(content=ddd, media_type="application/json")


app.mount("/", StaticFiles(directory="webdata", html=True), name="static")
