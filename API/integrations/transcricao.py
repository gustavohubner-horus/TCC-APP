from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def transcrever(conteudo: bytes, nome: str) -> str:
    transcription = client.audio.transcriptions.create(
        file=(nome, conteudo),
        model="whisper-large-v3",
        temperature=0,
        response_format="verbose_json",
    )
    return transcription.text