import threading
from importlib import resources
from pathlib import Path

import cv2
import ffmpegio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from tqdm import tqdm

app = FastAPI()


class Info(BaseModel):
    ldap: str
    drowsy: str


def rnd_str(n=8):
    import random
    import string
    return ''.join(random.choices(string.ascii_letters, k=n))


def record(info: Info):
    clips = Path('clips')
    clips.mkdir(exist_ok=True, parents=True)
    clip = clips / f'{rnd_str()}_{info.drowsy}_{info.ldap}.mp4'
    clip = str(clip)

    FPS = 30
    SEC = 75
    cap = cv2.VideoCapture(0)
    print('Starting recording', clip)
    with ffmpegio.open(clip, 'wv', rate_in=FPS, y=None) as out:
        for _ in tqdm(range(FPS * SEC)):
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)  # type: ignore

    cap.release()


@app.options('/start')
async def start_options():
    return {'message': 'Recording started'}


@app.post('/start')
async def start(info: Info):
    threading.Thread(target=record, args=[info]).start()


@app.get('/', response_class=HTMLResponse)
async def home():
    import drowsy_recorder.build as build
    with resources.files(build).joinpath('index.html').open() as f:
        return f.read()


def main():
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
