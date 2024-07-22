import threading
from importlib import resources
from pathlib import Path

import cv2
import ffmpegio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from tqdm import tqdm

app = FastAPI()


def record():
    clips = Path('clips')
    clips.mkdir(exist_ok=True, parents=True)
    clip = clips / 'output.mp4'
    clip = str(clip)

    FPS = 30
    SEC = 5
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
async def start():
    threading.Thread(target=record).start()
    return {'message': 'Recording started'}


@app.get('/', response_class=HTMLResponse)
async def home():
    import drowsy_recorder.build as build
    with resources.files(build).joinpath('index.html').open() as f:
        return f.read()


def main():
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
