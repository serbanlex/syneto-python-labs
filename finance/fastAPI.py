from fastapi import FastAPI
from finance_router import *

app = FastAPI(title="Syneto Labs API - YFinance", version="0.1")
# setting the router as the one in finance_router
app.include_router(router)
