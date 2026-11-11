import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()


def interpretar(texto, categorias, hoje):
    lista = ", ".join(categorias) if categorias else "nenhuma"
    instrucoes = (
        "Você recebe um texto que descreve um gasto e deve extrair os dados dele. "
        f"A data de hoje é {hoje}. "
        f"As categorias disponíveis são: {lista}. "
        "Responda somente em JSON com os campos: descricao (texto curto), "
        "valor (número), data (no formato AAAA-MM-DD) e categoria (uma das "
        "categorias disponíveis ou null). Se a data não for citada, use a data de hoje. "
        "Nunca crie uma categoria que não esteja na lista."
    )

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": instrucoes},
            {"role": "user", "content": texto},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)
