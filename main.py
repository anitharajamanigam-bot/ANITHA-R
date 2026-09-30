from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": None,
            "selected_task": "qa"
        }
    )


@app.post("/process", response_class=HTMLResponse)
async def process(
    request: Request,
    task: str = Form(...),
    user_input: str = Form(...)
):

    user_input = user_input.strip()

    if not user_input:
        result = "Please enter your question or text."

    else:

        try:

            if task == "qa":
                result = answer_question(user_input)

            elif task == "explain":
                result = explain_topic(user_input)

            elif task == "quiz":
                result = generate_quiz(user_input)

            elif task == "summarize":
                result = summarize_text(user_input)

            elif task == "learn":
                result = get_learning_recommendations(user_input)

            else:
                result = "Invalid task selected."

        except Exception as error:
            result = f"Error: {error}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result,
            "selected_task": task
        }
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "EduGenie"
    }