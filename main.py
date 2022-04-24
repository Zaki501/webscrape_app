from fastapi import FastAPI

import core.models as models
from api.routes import alert, auth, user
from core.database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(alert.router)


@app.get("/")
async def hello_world():
    return {"message": "Hello Application!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
