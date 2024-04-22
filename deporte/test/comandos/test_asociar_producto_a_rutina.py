import pytest
from unittest.mock import patch
from faker import Faker

from src.modelos.producto_rutina import ProductoRutina
from src.errores.errores import BadRequestError, InvalidAuthenticationError, NotFoundError
from src.modelos.rutina_alimenticia import RutinaAlimenticia
from src.comandos.asociar_producto_a_rutina import AsociarProductoARutina
from test.mock_session import MockSession

fake = Faker()
_TOKEN = fake.uuid4()
_ID_RUTINA_ALIMENTICIA = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina(mock_session, requests_mock):
    rutina_alimenticia_mock = mock_rutina_alimenticia()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_first = mock_filter.first

    mock_first.side_effect = [rutina_alimenticia_mock, None]

    (result, status_code) = AsociarProductoARutina(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA, json_request=body_data()).execute()
    
    assert status_code == 200
    assert result.get("respuesta")
    assert result.get("token")
    assert result["respuesta"] == "Producto asociado a rutina alimenticia exitosamente"
    assert result["token"] == _TOKEN


@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina_no_existente(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        AsociarProductoARutina(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA, json_request=body_data()).execute()
    
    assert exc_info.value.code == 404
    assert exc_info.value.description == f"No existe la rutina alimenticia con id [{_ID_RUTINA_ALIMENTICIA}]"

@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina_ya_asociado(mock_session, requests_mock):
    rutina_alimenticia_mock = mock_rutina_alimenticia()
    producto_rutina_mock = mock_producto_rutina()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_first = mock_filter.first

    mock_first.side_effect = [rutina_alimenticia_mock, producto_rutina_mock]

    with pytest.raises(BadRequestError) as exc_info:
        AsociarProductoARutina(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA, json_request=body_data()).execute()
    
    assert exc_info.value.code == 400
    assert exc_info.value.description == "El producto ya se encuentra en la rutina alimenticia"

@patch('test.mock_session', autospec=True)
def test_asociar_producto_a_rutina_sin_autorizacion(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    with pytest.raises(InvalidAuthenticationError) as exc_info:
        AsociarProductoARutina(session=mock_session_instance, headers={}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA, json_request=body_data()).execute()
    
    assert exc_info.value.code == 403


def body_data():
    return {"dosis": fake.text(), "producto_id": fake.uuid4()}

def mock_rutina_alimenticia():
    return RutinaAlimenticia(nombre=fake.name(), descripcion=fake.text())

def mock_producto_rutina():
    return ProductoRutina(producto_id=fake.uuid4(), dosis=fake.text(), rutina_alimenticia=_ID_RUTINA_ALIMENTICIA)
