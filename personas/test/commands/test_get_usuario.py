import pytest
from unittest.mock import patch
from faker import Faker

from src.commands.get_usuario import GetUsuario
from src.models.usuario import Usuario
from test.mock_session import MockSession
import random

fake = Faker()




@pytest.fixture
def mock_session():
    return MockSession()




@patch('test.mock_session', autospec=True)
def test_get_usuario(mock_session):
    user_mock = usuario_mock()


    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = user_mock
    
    service = GetUsuario(mock_session_instance,"",user_mock.email )
    result = service.execute()
    assert mock_session_instance.query.called
    assert result.email == user_mock.email



def usuario_mock():
    return Usuario(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4())


