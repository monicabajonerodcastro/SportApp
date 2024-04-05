import pytest, random
from unittest.mock import patch
from faker import Faker

from src.commands.get_usuario_por_id import GetUsuarioPorId
from src.models.usuario import Usuario
from test.mock_session import MockSession
from src.errors.errors import InvalidAuthentication

fake = Faker()

_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_usuario_id(mock_session, requests_mock, mocker):
    mock_usuario = usuario_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_usuario

    funcion_auth = mocker.patch("src.services.servicio_token.validar_token")
    funcion_auth.return_value = "", 200
    
    service = GetUsuarioPorId(session=mock_session_instance, headers={"Authorization": f"Bearer {_TOKEN}"}, id_usuario=fake.uuid4())
    (result, _) = service.execute()
    assert mock_session_instance.query.called
    assert result["email"] == mock_usuario.email

@patch('test.mock_session', autospec=True)
def test_obtener_plan_id_sin_autorizacion(mock_session, mocker):
    mock_usuario = usuario_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_usuario

    with pytest.raises(InvalidAuthentication):
        GetUsuarioPorId(session=mock_session_instance, headers={}, id_usuario=fake.uuid4()).execute()
    
    assert not mock_session_instance.query.called

def usuario_mock():
    return Usuario(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4())
