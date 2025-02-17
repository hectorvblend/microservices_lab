import os
import uvicorn
from src.main import app
from src.settings import HOST, PORT, ENVIRONMENT
from src.connectors.create_schemas import create_all_schemas


if __name__ == "__main__":
    create_all_schemas()
    uvicorn.run(
        app,
        host=HOST,
        port=int(PORT),
        reload=True if ENVIRONMENT =='develop' else False
        )