from dotenv import load_dotenv
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

import core.models as models
from api.routes import alert, auth, user
from core.database import engine
from limiter import limiter

load_dotenv()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Routes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(alert.router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def hello_world():
    return {"message": "Hello Application!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")
