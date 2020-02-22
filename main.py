from fastapi import FastAPI, HTTPException
import requests
import os
import re
import time
from color_detect import get_dominant_colors


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


@app.get("/colors")
def image_colors(image_url: str, num_suggestions: int = 4, ignore: list = ['#ffffff']):
    if not is_image(image_url):
        raise HTTPException(status_code=400, detail='URL provided is not an image')
    filename = download_image(image_url)
    if not filename:
        raise HTTPException(status_code=400, detail='Could not download image from provided url')
    colors = get_dominant_colors(filename, num_suggestions)
    for color in ignore:
        try:
            colors.remove(color)
        except ValueError:
            pass
    os.remove(filename)
    return {'status': 'ok', 'colors': colors}