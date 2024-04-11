import pytest
from unittest.mock import MagicMock
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


def crear_producto_servicio(session, producto_servicio_mock):
    return CrearProductoServicio(session,
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


def test_crear_producto_servicio():
    my_producto_servicio_mock = producto_servicio_mock()
    session = MagicMock()
    productoUsuario= crear_producto_servicio(session, my_producto_servicio_mock)
    result = productoUsuario.execute()
    assert result['description'] == "Producto o Servicio Registrado con exito"

def test_crear_producto_servicio_missing_requiredfield():
    my_producto_servicio_mock = producto_servicio_mock()
    my_producto_servicio_mock.nombre=''
    session = MagicMock()

    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_producto_servicio(session, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 404
    assert exc_info.value.description.__contains__("No se encontró el parámetro")


def ttest_crear_producto_servicio_invalid_deporte_formatfield():
    my_producto_servicio_mock = producto_servicio_mock()
    my_producto_servicio_mock.id_deporte='asasasasasa'
    session = MagicMock()

    with pytest.raises(BadRequestError) as exc_info:
        service = crear_producto_servicio(session, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "El identificador del Deporte no es válido"

def test_crear_producto_servicio_invalid_socio_formatfield():
    my_producto_servicio_mock = producto_servicio_mock()
    my_producto_servicio_mock.id_socio='asasasasasa'
    session = MagicMock()

    with pytest.raises(BadRequestError) as exc_info:
        service = crear_producto_servicio(session, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "El identificador del Socio no es válido"


def test_crear_producto_servicio_deporte_none():
    my_producto_servicio_mock = producto_servicio_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = None
    session.query.return_value = query


    with pytest.raises(NotFoundError) as exc_info:
        service = crear_producto_servicio(session, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 404
    assert exc_info.value.description.__contains__("No se encontró un Deporte con el id")


def test_crear_producto_servicio_socio_none():
    my_producto_servicio_mock = producto_servicio_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = None
    session.query.return_value = query


    with pytest.raises(NotFoundError) as exc_info:
        service = crear_producto_servicio(session, my_producto_servicio_mock)
        service.execute()


    assert exc_info.value.code == 404
    assert exc_info.value.description.__contains__("No se encontró un Deporte con el id")