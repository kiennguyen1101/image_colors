from typing import List

from fastapi import FastAPI, HTTPException
import requests
import os
import time

from pydantic import BaseModel

from color_detect import get_dominant_colors, rgb_list_to_hex

app = FastAPI()


def is_image(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'image' not in content_type:
        return False
    return True


def download_image(url: str) -> str:
    r = requests.get(url, allow_redirects=True)
    if r.content is None:
        return ''
    filename = str(time.time())
    open(filename, 'wb').write(r.content)
    return filename


@app.get("/")
async def home_res():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


class ColorResponseModel(BaseModel):
    status: str = 'success'
    data: List[str] = []


@app.get("/colors", response_model=ColorResponseModel)
def image_colors(image_url: str, num_suggestions: int = 4):
    if not is_image(image_url):
        raise HTTPException(status_code=400, detail='URL provided is not an image')
    filename = download_image(image_url)
    if not filename:
        raise HTTPException(status_code=400, detail='Could not download image from provided url')
    colors = get_dominant_colors(filename, num_suggestions)
    colors = rgb_list_to_hex(colors)
    os.remove(filename)
    return ColorResponseModel(data=colors)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9001, reload=False)
