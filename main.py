from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from typing import Optional

app = FastAPI(
    title="Gemini API",
    description="API para interactuar con Google Gemini",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Configuración de la API
GOOGLE_API_KEY = "AIzaSyBw73_JQKl8tzyx8Cp7Ikmpoj75YIFZ3Ho"
genai.configure(api_key=GOOGLE_API_KEY)

# Verificar modelos disponibles e inicializar
try:
    # Listar modelos disponibles
    for m in genai.list_models():
        print(m.name)
    
    # Usar gemini-1.0-pro en lugar de gemini-pro
    MODEL_NAME = "gemini-2.0-flash"
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Error al inicializar el modelo: {str(e)}")

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    response: str
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gemini", "status": "active"}

@app.post("/ask", response_model=Answer)
async def ask_gemini(question: Question):
    try:
        if not question.text.strip():
            raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
        
        response = model.generate_content(question.text)
        
        if response.text:
            return Answer(response=response.text)
        else:
            return Answer(response="Lo siento, no pude generar una respuesta", error="Respuesta vacía")
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error en la generación: {error_msg}")
        return Answer(response="", error=error_msg)

# Solo usar esto para desarrollo local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
