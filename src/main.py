#!/usr/bin/env python3
'''
This script is used to configure and start the API service.
'''

__author__ = "Hector Vergara"
__email__ = "hector.vergara@blend360.com"
__version__ = "1.0"

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.services.ds_scripts.ds_model import load_model
from src.controllers.api.application_apis import router as application_apis
from src.settings import (
    ENVIRONMENT,
    HOST,
    PORT)

# 📌 Global variables for the application
DS_MODEL = None

description = f'''<a href="https://github.com/hectorvblend/microservices_lab">
    <img width=10% src="https://github.com/hectorvblend/microservices_lab/blob/main/docs/assets/octocat.gif?raw=true"/> Follow the repository...</a>'''

# 📌 Fast API init
app = FastAPI(
    title="Blend L&L example API service docs page",
    description=description,
)

# 📌 Middlewares:
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Add routers:
app.include_router(application_apis)

# 📌 Error Handler:
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": "Bad request", "detail": str(exc)},
    )

app.add_exception_handler(Exception, global_exception_handler)


@app.on_event("startup")
async def startup_event():
    global DS_MODEL
    print("🔥 Executing initialization routine...")
    DS_MODEL = await load_model()
    print("🔥 All set!")


if __name__ == "__main__":
    # 📌 Server initialization.
    uvicorn.run(
        'main:app',
        host=HOST,
        port=PORT,
        reload=True if ENVIRONMENT =='develop' else False
        )
