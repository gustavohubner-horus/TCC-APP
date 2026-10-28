import base64
from groq import Groq
from dotenv import load_dotenv

# Carrega a variavel GROQ_API_KEY
load_dotenv()
client = Groq()

prompt = ("Transcreva todo o texto da imamge, exatamente como esta escrito, não resuma nada, não adicione nada. "
    "Se não tiver texto na imagem, não reotrne NADA.")


def extrair_texto (conteudo: bytes, tipo: str) -> str:
    #converte a imagem pra base 64
    img_64 = base64.b64encode(conteudo).decode()  

    completion = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{
          "role": "user",
          "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{tipo};base64,{img_64}"}},],}],
        temperature= 0,
        reasoning_effort = "none"
    )
    return completion.choices[0].message.content

