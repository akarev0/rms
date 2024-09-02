from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from chains.employee_match.v2.chains import full_chain


chat_router_v2 = APIRouter()


@chat_router_v2.get("/v2", response_class=HTMLResponse)
async def get_chat_page():
    with open("templates/chat_v2.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


class ChatRequest(BaseModel):
    message: str


@chat_router_v2.post("/chat-v2", response_class=JSONResponse)
def chat(request: ChatRequest):
    results = full_chain.invoke({"question": request.message})

    return JSONResponse(content={"reply": results})
