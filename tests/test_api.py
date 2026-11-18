def test_raiz(client):
    resposta = client.get("/")
    assert resposta.status_code == 200


def test_listar_tarefas(client):
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_buscar_tarefa_que_nao_existe(client):
    resposta = client.get("/tarefas/999")
    assert resposta.status_code == 404


def test_criar_tarefa_sem_token(client):
    resposta = client.post("/tarefas", json={"titulo": "Estudar"})
    assert resposta.status_code == 401


def test_criar_usuario(client):
    resposta = client.post(
        "/usuarios", json={"email": "novo@email.com", "senha": "123456"}
    )
    assert resposta.status_code == 201
    assert "senha" not in resposta.json()


def test_login_com_senha_errada(client):
    client.post("/usuarios", json={"email": "teste@email.com", "senha": "123456"})
    resposta = client.post(
        "/login", data={"username": "teste@email.com", "password": "errada"}
    )
    assert resposta.status_code == 401


def test_criar_tarefa_com_token(client, headers):
    resposta = client.post("/tarefas", json={"titulo": "Estudar pytest"}, headers=headers)
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "Estudar pytest"


def test_apagar_tarefa(client, headers):
    client.post("/tarefas", json={"titulo": "Tarefa antiga"}, headers=headers)

    resposta = client.delete("/tarefas/1", headers=headers)
    assert resposta.status_code == 204

    resposta = client.get("/tarefas/1")
    assert resposta.status_code == 404