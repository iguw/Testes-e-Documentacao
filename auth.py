from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel

SECRET_KEY = "3a21c6f7bb74e48fe56649f14cb9e8709dcc25d6f19f5c355752f30f0611edcc"
ALGORITHM = "HS256"
MINUTOS_PARA_EXPIRAR = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#o swagger usa isso para mostrar o botao authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)


def criar_token(email: str):
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_PARA_EXPIRAR)
    dados = {"sub": email, "exp": expira}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


#usada nas rotas protegidas: le o token do header e devolve o usuario
def usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    erro = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = dados.get("sub")
    except InvalidTokenError:
        raise erro

    if email is None:
        raise erro

    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    if usuario is None:
        raise erro

    return usuario