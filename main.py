from typing import List

from fastapi import FastAPI, HTTPException, Query
import requests
import os
import time

from pydantic import BaseModel, HttpUrl

from color_detect import get_dominant_colors, rgb_list_to_hex

app = FastAPI(title=os.getenv('APP_NAME', 'Detect Image Color'))


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


@app.get("/color_suggestions", response_model=ColorResponseModel)
def color_suggestions(image_url: HttpUrl, num_suggestions: int = Query(4, gt=0, lt=9)):
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
    port = os.getenv('PORT', 9001)
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
