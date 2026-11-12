from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from services import ia_service
from services.auth_service import get_usuario_logado

router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/transcricao")
async def transcrever(audio: UploadFile):
    texto = ia_service.transcrever_audio(await audio.read(), audio.filename)
    return {"texto": texto}

@router.post("/imagem")
async def extrair_texto_imagem(imagem: UploadFile):
    texto = ia_service.extrair_texto_imagem(await imagem.read(), imagem.content_type)
    return {"texto": texto}


@router.post("/gasto-voz")
async def gasto_voz(
    audio: UploadFile,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    texto = ia_service.transcrever_audio(await audio.read(), audio.filename)
    return ia_service.sugerir_gasto(db, usuario.usu_id, texto)


@router.post("/gasto-foto")
async def gasto_foto(
    imagem: UploadFile,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    texto = ia_service.extrair_texto_imagem(await imagem.read(), imagem.content_type)
    return ia_service.sugerir_gasto(db, usuario.usu_id, texto)
