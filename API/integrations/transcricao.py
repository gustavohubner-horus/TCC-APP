from groq import Groq
from dotenv import load_dotenv

# Carrega a variavei GROQ_API_KEY
load_dotenv()
client = Groq()

def transcrever(conteudo: bytes, nome: str) -> str:
    transcription = client.audio.transcriptions.create(
        file=(nome, conteudo),
        model="whisper-large-v3",
        temperature=0,
        response_format="json",
    )
    return transcription.text