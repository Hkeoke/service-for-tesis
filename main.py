from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Importa el middleware de CORS
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permite todas las origins (puedes especificar dominios específicos)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

GOOGLE_API_KEY = "AIzaSyBNUvWgase8MvyckY8sronDMsWY1kzwLPc"
genai.configure(api_key=GOOGLE_API_KEY)


class Question(BaseModel):
    text: str


class Answer(BaseModel):
    response: str


@app.post("/ask", response_model=Answer)
async def ask_gemini(question: Question):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question.text)
        return Answer(response=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
