import pytest, random
from unittest.mock import patch
from faker import Faker

from src.commands.get_perfil_deportivo_por_usuario import GetPerfilDeportivoPorUsuario
from src.models.perfil_deportivo import PerfilDeportivo
from src.commands.get_usuario_por_id import GetUsuarioPorId
from test.mock_session import MockSession
from src.errors.errors import InvalidAuthentication

fake = Faker()

_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_perfil_deportivo_usuario_id(mock_session, mocker):
    mock_perfil_deportivo = perfil_deportivo_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_perfil_deportivo

    funcion_auth = mocker.patch("src.services.servicio_token.validar_token")
    funcion_auth.return_value = {"token": _TOKEN}, 200
    
    service = GetPerfilDeportivoPorUsuario(session=mock_session_instance, headers={"Authorization": f"Bearer {_TOKEN}"}, id_usuario=fake.uuid4())
    (result, _) = service.execute()
    assert mock_session_instance.query.called

@patch('test.mock_session', autospec=True)
def test_obtener_perfil_deportivo_usuario_id_sin_autorizacion(mock_session):
    mock_perfil_deportivo = perfil_deportivo_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_perfil_deportivo

    with pytest.raises(InvalidAuthentication):
        GetPerfilDeportivoPorUsuario(session=mock_session_instance, headers={}, id_usuario=fake.uuid4()).execute()
    
    assert not mock_session_instance.query.called

def perfil_deportivo_mock():
    return PerfilDeportivo( fake.uuid4(),random.choice(['F', 'M', 'O']), fake.pyint(min_value=15), fake.pyint(), fake.pyint(max_value=250), fake.country(), fake.city(),fake.country(), fake.city(),fake.pyint(),fake.pyfloat(max_value=100,right_digits=2),fake.pyint(),fake.pyfloat(right_digits=2),"","","","","","",fake.name(),fake.name(), fake.word())
