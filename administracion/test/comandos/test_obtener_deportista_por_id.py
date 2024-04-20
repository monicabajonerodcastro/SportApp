import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_deportista_por_id import ObtenerDeportistaId
from test.mock_session import MockSession
from src.errores.errores import NotFoundError

fake = Faker()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

def test_obtener_deportista_id(requests_mock):

    deportista_mock = mock_deportista()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": deportista_mock["id"]})
    requests_mock.get(f'http://host-personas-test/personas/{deportista_mock["id"]}', json=deportista_mock)

    (result, _) = ObtenerDeportistaId(headers={"Authorization": "Bearer "}, id_deportista=deportista_mock["id"]).execute()
    assert result["id"] == deportista_mock["id"]

def test_obtener_deportista_no_exsite(requests_mock):

    deportista_mock = mock_deportista()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": deportista_mock["id"]})
    requests_mock.get(f'http://host-personas-test/personas/{deportista_mock["id"]}', status_code=400)

    with pytest.raises(NotFoundError):
        ObtenerDeportistaId(headers={"Authorization": "Bearer "}, id_deportista=deportista_mock["id"]).execute()

def mock_deportista():
    return {"apellido":fake.name(), "email": fake.email(), "id": fake.uuid4(), "nombre": fake.name(), "numero_identificacion": fake.pyint(min_value=1000),
        "password": fake.word(),  "rol": "DEPORTISTA", "suscripcion": fake.uuid4(), "tipo_id": "CC", "username": fake.name()}
    