from fastapi import FastAPI
from nasa_router import *

app = FastAPI(title="Syneto Labs API", version="0.1")
app.include_router(router)
