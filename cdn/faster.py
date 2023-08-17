from fastapi import FastAPI, HTTPException, Header
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from urllib.parse import quote
import urllib.request
from functools import partial
import os

import termcolor

green = partial(termcolor.colored, color='green', attrs=('bold',))
yellow = partial(termcolor.colored, color='yellow', attrs=('bold',))
blue = partial(termcolor.colored, color='blue', attrs=('bold',))
red = partial(termcolor.colored, color='red', attrs=('bold',))


app = FastAPI()


@app.get("/{filename:path}")
async def serve_file(filename: str, origin: str = Header(None)):
    # if filename.endswith('.map'):
    #     raise HTTPException(status_code=404, detail="File not found")

    cdn_url = "https://cdn.jsdelivr.net/" + filename
    local_filename = quote(cdn_url, safe="")
    filepath = os.path.abspath(os.path.join("static", local_filename))

    if not os.path.exists(filepath):
        print(yellow(f'Caching file {filename!r}'))
        try:
            cdn_response = urllib.request.urlopen(cdn_url)
        except Exception:
            print(red(f'Failed to cache file {filename}'))
            raise HTTPException(status_code=404, detail="File not found")

        content = cdn_response.read()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(content)

    response = FileResponse(filepath)
    if origin and origin == "http://localhost:8000":
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:8000"
        response.headers["Content-Type"] = "text/javascript"

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
