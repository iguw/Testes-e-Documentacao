# Testes e Documentação

Atividade da disciplina de APIs e Microsserviços. API de tarefas feita com FastAPI, SQLAlchemy e SQLite, com login por JWT, Swagger documentado e testes automatizados com Pytest. As rotas GET são públicas e as de escrita (POST, PUT e DELETE) exigem token.

## Como rodar

1. Baixe o projeto:
   ```
   git clone https://github.com/iguw/Testes-e-Documentacao.git
   cd Testes-e-Documentacao
   ```

2. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Crie o banco com a migração:
   ```
   alembic upgrade head
   ```

5. Rode a API:
   ```
   uvicorn main:app --reload
   ```

6. Abra a documentação em http://127.0.0.1:8000/docs

## Como rodar os testes

```
pytest
```

Os testes usam um banco temporário na memória, então não mexem no `tarefas.db`.

## Como usar o login

1. Crie um usuário em `POST /usuarios`.
2. Clique em **Authorize** no Swagger e entre com o e-mail (no campo username) e a senha.
3. Agora o POST, PUT e DELETE de `/tarefas` funcionam. Sem o token, retornam 401.

## Autor

Guilherme Alves - [@iguw](https://github.com/iguw)