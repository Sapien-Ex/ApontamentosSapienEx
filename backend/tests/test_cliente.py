from http import HTTPStatus
from uuid import UUID


def test_criar_cliente_retorna_201_com_dados(client):
    payload = {
        "razao_social": "Empresa Teste LTDA",
        "nome_fantasia": "Empresa Teste",
        "cnpj": "12345678000199",
    }

    response = client.post("/clientes/", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["razao_social"] == payload["razao_social"]
    assert data["nome_fantasia"] == payload["nome_fantasia"]
    assert data["cnpj"] == payload["cnpj"]
    assert data["ativo"] is True
    assert UUID(data["id"])
    assert "created_at" in data


def test_listar_clientes(client):
    payload = {
        "razao_social": "Empresa Teste 2 LTDA",
        "nome_fantasia": "Empresa Teste 2",
        "cnpj": "12345678000122",
    }

    client.post("/clientes/", json=payload)

    response = client.get("/clientes/")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["razao_social"] == payload["razao_social"]
    assert data[0]["nome_fantasia"] == payload["nome_fantasia"]
    assert data[0]["cnpj"] == payload["cnpj"]
    assert data[0]["ativo"] is True


def test_listar_clientes_vazio(client):

    response = client.get("/clientes/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_atualizar_cliente(client):
    payload = {
        "razao_social": "Empresa Teste 000 LTDA",
        "nome_fantasia": "Empresa Teste 0",
        "cnpj": "00000000000000",
    }

    cliente_id = client.post("/clientes/", json=payload).json()["id"]

    payload2 = {
        "razao_social": "Empresa Teste 999 LTDA",
    }

    response = client.patch(f"/clientes/{cliente_id}", json=payload2)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["razao_social"] == payload2["razao_social"]
    assert data["nome_fantasia"] == payload["nome_fantasia"]
    assert data["cnpj"] == payload["cnpj"]
    assert data["ativo"] is True


def test_desativar_cliente(client):
    payload = {
        "razao_social": "Empresa Teste LTDA",
        "nome_fantasia": "Empresa Teste",
        "cnpj": "12345678000199",
    }

    cliente_id = client.post("/clientes/", json=payload).json()["id"]

    response = client.delete(f"/clientes/{cliente_id}")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["razao_social"] == payload["razao_social"]
    assert data["nome_fantasia"] == payload["nome_fantasia"]
    assert data["cnpj"] == payload["cnpj"]
    assert data["ativo"] is False
    assert UUID(data["id"])
    assert "created_at" in data


def test_listar_clientes_filtra_inativos(client):
    client.post(
        "/clientes/",
        json={
            "razao_social": "Teste Empresa LTDA ativo",
            "nome_fantasia": "Empresa teste",
            "cnpj": "19394050192846",
        },
    ).json()

    inativo = client.post(
        "/clientes/",
        json={
            "razao_social": "Teste Empresa LTDA inativo",
            "nome_fantasia": "Empresa inativa",
            "cnpj": "59483716485960",
        },
    ).json()

    client.delete(f"/clientes/{inativo['id']}")

    response = client.get("/clientes/", params={"ativo": False})

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == inativo["id"]


def test_obter_cliente_inexistente_retorna_404(client):
    payload = {
        "razao_social": "Empresa Testeee LTDA",
        "nome_fantasia": "Empresa Testeee",
        "cnpj": "12345678000122",
    }

    client.post("/clientes/", json=payload)

    cliente_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/clientes/{cliente_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_criar_cliente_com_cnpj_repetido_retorna_409(client):
    payload = {
        "razao_social": "Empresa Teste LTDA",
        "nome_fantasia": "Empresa Teste",
        "cnpj": "12345678000199",
    }

    client.post("/clientes/", json=payload)

    payload2 = {
        "razao_social": "Empresa Teste 2 LTDA",
        "nome_fantasia": "Empresa Teste 2",
        "cnpj": "12345678000199",
    }

    response = client.post("/clientes/", json=payload2)

    assert response.status_code == HTTPStatus.CONFLICT
