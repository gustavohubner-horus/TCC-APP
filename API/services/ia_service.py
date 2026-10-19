from integrations.transcricao import transcrever

def transcrever_audio(conteudo: bytes, nome: str) -> str:
    texto = transcrever(conteudo, nome)
    return texto