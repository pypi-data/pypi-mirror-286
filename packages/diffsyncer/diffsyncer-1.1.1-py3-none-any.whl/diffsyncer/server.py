import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from diffsyncer import apis

# add api prefix /api
app = FastAPI()


# enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# static files
default_static_dir = os.path.join(os.path.dirname(__file__), "static")

# support custom static directory, default is ./static
# you can set STATIC_DIR environment variable to change the directory
static_dir = os.getenv("STATIC_DIR", default_static_dir)
app.mount(
    "/static",
    StaticFiles(directory=static_dir, check_dir=True, html=True),
    name="static",
)

index_dir = os.path.join(os.path.dirname(__file__), "static")
templates = Jinja2Templates(directory=index_dir)


# index page
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# add api router
app.include_router(apis.apis, prefix="/api/v1")
