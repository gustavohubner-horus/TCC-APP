from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from integrations.transcricao import transcrever
from integrations.imagem import extrair_texto
from integrations.raciocinio import interpretar
from services import categoria_service


def transcrever_audio(conteudo: bytes, nome: str) -> str:
    if len(conteudo) == 0:
        raise HTTPException(status_code=400, detail="O áudio enviado está vazio.")
    return transcrever(conteudo, nome)


def extrair_texto_imagem(conteudo: bytes, tipo: str) -> str:
    if len(conteudo) == 0:
        raise HTTPException(status_code=400, detail="A imagem enviada está vazia.")
    texto = extrair_texto(conteudo, tipo)
    if not texto or not texto.strip():
        raise HTTPException(status_code=422, detail="Não foi encontrado texto na imagem.")
    return texto


def sugerir_gasto(db: Session, usu_id: int, texto: str) -> dict:
    categorias = categoria_service.listar_categorias(db, usu_id)
    nomes = [c.cat_nome for c in categorias]
    dados = interpretar(texto, nomes, date.today().isoformat())

    cat_id = None
    nome_categoria = dados.get("categoria")
    if nome_categoria:
        for c in categorias:
            if c.cat_nome.lower() == str(nome_categoria).lower():
                cat_id = c.cat_id
                break

    return {
        "descricao": dados.get("descricao"),
        "valor": dados.get("valor"),
        "data": dados.get("data"),
        "cat_id": cat_id,
        "texto": texto,
    }
