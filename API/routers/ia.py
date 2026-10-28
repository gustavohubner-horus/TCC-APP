from fastapi import APIRouter, UploadFile
from services import ia_service

router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/transcricao")
async def transcrever(audio: UploadFile):
    texto = ia_service.transcrever_audio(await audio.read(), audio.filename)
    return {"texto": texto}

@router.post("/imagem")
async def extrair_texto_imagem(imagem: UploadFile):
    texto = ia_service.extrair_texto_imagem(await imagem.read(), imagem.content_type)
    return {"texto": texto}