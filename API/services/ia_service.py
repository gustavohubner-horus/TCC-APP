from fastapi import HTTPException
from integrations.transcricao import transcrever
from integrations.imagem import extrair_texto

def transcrever_audio(conteudo: bytes, nome: str) -> str:
    if len(conteudo) == 0:
       raise HTTPException(status_code=400, detail="Faz o L vagabundo.")

    texto = transcrever(conteudo, nome)
    return texto

def extrair_texto_imagem(conteudo: bytes, tipo: str) -> str:
    if len(conteudo) == 0:
        raise HTTPException(status_code=400, detail="A imagem enviada está vazia.")

    texto = extrair_texto(conteudo, tipo)
    if not texto or not texto.strip():
        raise HTTPException(status_code=422, detail="Não foi encontrado texto na imagem.")
    return texto