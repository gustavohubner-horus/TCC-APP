from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_i18n import PydanticI18n

from routers import ia, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tradução das mensagen do Pydantic
MSG_PT = {
    "Field required": "campo obrigatório.",
    "String should have at least {} characters": "deve ter no mínimo {} caracteres.",
    "String should have at most {} characters": "deve ter no máximo {} caracteres.",
    "value is not a valid email address: {}": "formato inválido.",
    "Input should be a valid date or datetime, {}": "data inválida.",
}
ROTULOS = {
    "nome": "Nome",
    "login": "Login",
    "email": "E-mail",
    "senha": "Senha",
    "data_nascimento": "Data de nascimento",
}

traducao = PydanticI18n({"en_US": {k: k for k in MSG_PT}, "pt_BR": MSG_PT})

@app.exception_handler(RequestValidationError)
async def erros_validacao(request: Request, exc: RequestValidationError):
    traduzidos = traducao.translate(exc.errors(), locale="pt_BR")
    erros = []
    for e in traduzidos:
        campo = e["loc"][-1]
        rotulo = ROTULOS.get(campo, campo)
        erros.append({"campo": campo, "msg": f"{rotulo}: {e['msg']}"})
    return JSONResponse(status_code=422, content={"detail": erros})

app.include_router(ia.router)
app.include_router(auth.router)