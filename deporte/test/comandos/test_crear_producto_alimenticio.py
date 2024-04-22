import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.crear_producto_alimenticio import CrearProductoAlimenticio
from src.errores.errores import InvalidAuthenticationError, MissingRequiredField
from test.mock_session import MockSession

fake = Faker()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina(mock_session, requests_mock):

    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    (result, status_code) = CrearProductoAlimenticio(session=mock_session_instance, headers={"Authorization": "Bearer "}, json_request=body_data()).execute()

    assert status_code == 201
    assert result.get("respuesta")
    assert result.get("token")
    assert result["token"] == _TOKEN
    assert result["respuesta"] == "Producto alimenticio creado exitosamente"


@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina_sin_nombre(mock_session, requests_mock):

    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    body = body_data()
    body["nombre"] = ""

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearProductoAlimenticio(session=mock_session_instance, headers={"Authorization": "Bearer "}, json_request=body).execute()
    
    assert exc_info.value.code == 404
    assert exc_info.value.description == "No se encontró el parámetro [nombre]"


@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina_sin_valor(mock_session, requests_mock):

    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    body = body_data()
    body["valor"] = ""

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearProductoAlimenticio(session=mock_session_instance, headers={"Authorization": "Bearer "}, json_request=body).execute()
    
    assert exc_info.value.code == 404
    assert exc_info.value.description == "No se encontró el parámetro [valor]"

@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina_sin_autorizacion(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    with pytest.raises(InvalidAuthenticationError) as exc_info:
        CrearProductoAlimenticio(session=mock_session_instance, headers={}, json_request=body_data()).execute()
    
    assert exc_info.value.code == 403

def body_data():
    return {"nombre": fake.name(), "valor": fake.pyint(min_value=1000)}