import pytest
from unittest.mock import MagicMock
from faker import Faker

from src.commands.crear_usuario import CrearUsuario
from src.models.usuario import Usuario
from test.mock_session import MockSession
from src.errors.errors import MissingRequiredField,InvalidFormatField
import random

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_usuario(session, usuario_mock):
    return CrearUsuario(session,
                        {"email": usuario_mock.email,
                        "nombre": usuario_mock.nombre,
                        "apellido": usuario_mock.apellido,
                        "tipo_identificacion": usuario_mock.tipo_id,
                        "numero_identificacion": usuario_mock.numero_identificacion,
                        "username": usuario_mock.username,
                        "password": usuario_mock.password,
                        "suscripcion": usuario_mock.suscripcion}
                        
                     )


def usuario_mock():
    return Usuario(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4(), "DEPORTISTA")


def test_crear_usuario():
    my_usuario_mock = usuario_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_usuario_mock
    session.query.return_value = query
    crearUsuario = crear_usuario(session, my_usuario_mock)
    result = crearUsuario.execute()
    assert result["description"] == "Usuario Registrado con exito"

def test_crear_usuario_missing_requiredfield():
    my_usuario_mock = usuario_mock()
    my_usuario_mock.nombre=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_usuario_mock
    session.query.return_value = query


    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_usuario(session, my_usuario_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "Parámetros requeridos"


def test_crear_usuario_invalid_formatfield():
    my_usuario_mock = usuario_mock()
    my_usuario_mock.email="uno@uno."
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_usuario_mock
    session.query.return_value = query


    with pytest.raises(InvalidFormatField) as exc_info:
        service = crear_usuario(session, my_usuario_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "Parámeto(s) con formato inválido"
