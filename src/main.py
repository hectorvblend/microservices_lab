import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.api.application_apis import router as application_apis
from src.settings import (
    ENVIRONMENT,
    HOST,
    PORT)


description = f'''<a href="https://github.com/.../">
    <img width=10% src="https://raw.githubusercontent.com/.../docs/assets/octocat.gif"/> Follow the repository...</a>'''

app = FastAPI(
    title="Blend L&L example API service docs page",
    description=description,
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(application_apis)

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=HOST,
        port=PORT,
        reload=True if ENVIRONMENT =='develop' else False
        )
