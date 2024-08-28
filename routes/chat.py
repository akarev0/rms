from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from chains.employee_match import chain as skills_extractor_chain

chat_router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@chat_router.get("/", response_class=HTMLResponse)
async def get_chat_page():
    with open("templates/chat.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@chat_router.post("/chat", response_class=JSONResponse)
async def chat(request: ChatRequest):
    results: str = skills_extractor_chain.html_builder_chain.invoke(
        {"question": request.message}
    )

    return JSONResponse(content={"reply": results})
