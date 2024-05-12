import pytest
from unittest.mock import patch
from faker import Faker

from src.commands.ingresar_usuario import IngresarUsuario
from src.models.usuario import Usuario
from test.mock_session import MockSession
from src.errors.errors import MissingRequiredField, InvalidFormatField
import random

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_ingresar(mock_session):
    mock_usuario = usuario_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_usuario

    json_request = {
        "email": fake.safe_email(),
        "password": fake.password()
    }
    
    service = IngresarUsuario(session=mock_session_instance, json_request=json_request)
    (result, status) = service.execute()

    assert mock_session_instance.query.called
    assert status == 200
    assert result["token"]
    assert result["rol"] == "DEPORTISTA"

@patch('test.mock_session', autospec=True)
def test_ingresar_sin_campos(mock_session):
    mock_usuario = usuario_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_usuario

    with pytest.raises(MissingRequiredField):
        IngresarUsuario(session=mock_session_instance, json_request={})

@patch('test.mock_session', autospec=True)
def test_ingresar_con_correo_invalido(mock_session):
    mock_usuario = usuario_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_usuario

    json_request = {
        "email": fake.name(),
        "password": fake.password()
    }

    with pytest.raises(InvalidFormatField):
        IngresarUsuario(session=mock_session_instance, json_request=json_request)


def usuario_mock():
    return Usuario(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4(), "DEPORTISTA","","")


