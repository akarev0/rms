import uvicorn

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from routes.employees import employee_router
from routes.faker import fake_router
from routes.recourses import resource_router
from routes.teams import team_router
from routes.upload import upload_router
from routes.users import user_router
from routes.chat import chat_router
from routes.chat_v2 import chat_router_v2

app = FastAPI()
app.include_router(user_router)
app.include_router(resource_router)
app.include_router(employee_router)
app.include_router(team_router)
app.include_router(fake_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(chat_router_v2)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(app)
