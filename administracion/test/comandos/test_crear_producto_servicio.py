import pytest
from unittest.mock import MagicMock, patch
from faker import Faker

from src.errores.errores import MissingRequiredField,BadRequestError,NotFoundError
from src.comandos.crear_producto_servicio import CrearProductoServicio
from src.modelos.producto_servicio import ProductoServicio
from test.mock_session import MockSession

import random

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_producto_servicio(session, headers, producto_servicio_mock):
    return CrearProductoServicio(session, headers,
                        {
                        "nombre": producto_servicio_mock.nombre,
                        "valor": producto_servicio_mock.valor,
                        "detalle": producto_servicio_mock.detalle,
                        "descripcion": producto_servicio_mock.descripcion,
                        "id_deporte": producto_servicio_mock.id_deporte,
                        "id_socio": producto_servicio_mock.id_socio
                        }
                    )


def producto_servicio_mock():
    return ProductoServicio(fake.name(),fake.pyint(min_value=1000), fake.name(), fake.name(), fake.uuid4(),fake.uuid4())

@patch('test.mock_session', autospec=True)
def test_crear_producto_servicio(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    productoUsuario= crear_producto_servicio(mock_session_instance, {"Authorization": "Bearer"}, my_producto_servicio_mock)
    result = productoUsuario.execute()
    assert result['description'] == "Producto o Servicio Registrado con exito"

@patch('test.mock_session', autospec=True)
def test_crear_producto_servicio_missing_requiredfield(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    my_producto_servicio_mock.nombre=''
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={})

    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_producto_servicio(mock_session_instance, {"Authorization": "Bearer"}, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 404
    assert exc_info.value.description.__contains__("No se encontró el parámetro")

@patch('test.mock_session', autospec=True)
def ttest_crear_producto_servicio_invalid_deporte_formatfield(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    my_producto_servicio_mock.id_deporte='asasasasasa'
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={})

    with pytest.raises(BadRequestError) as exc_info:
        service = crear_producto_servicio(mock_session_instance,{"Authorization": "Bearer"}, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "El identificador del Deporte no es válido"

@patch('test.mock_session', autospec=True)
def test_crear_producto_servicio_invalid_socio_formatfield(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    my_producto_servicio_mock.id_socio='asasasasasa'
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={})

    with pytest.raises(BadRequestError) as exc_info:
        service = crear_producto_servicio(mock_session_instance,{"Authorization": "Bearer"}, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "El identificador del Socio no es válido"

@patch('test.mock_session', autospec=True)
def test_crear_producto_servicio_deporte_none(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    query = MagicMock()
    query.filter.return_value.first.return_value = None
    mock_session_instance.query.return_value = query


    with pytest.raises(NotFoundError) as exc_info:
        service = crear_producto_servicio(mock_session_instance, {"Authorization": "Bearer"},my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 404
    assert exc_info.value.description.__contains__("No se encontró un Deporte con el id")

@patch('test.mock_session', autospec=True)
def test_crear_producto_servicio_socio_none(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    query = MagicMock()
    query.filter.return_value.first.return_value = None
    mock_session_instance.query.return_value = query


    with pytest.raises(NotFoundError) as exc_info:
        service = crear_producto_servicio(mock_session_instance, {"Authorization": "Bearer"},my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 404
    assert exc_info.value.description.__contains__("No se encontró un Deporte con el id")