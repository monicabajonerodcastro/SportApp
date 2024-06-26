import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.asignar_servicio_deportista import AsignarServicioDeportista
from src.errores.errores import BadRequestError, InvalidAuthenticationError
from src.modelos.producto_servicio import ProductoServicio
from test.mock_session import MockSession

fake = Faker()
_ID_USUARIO = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asignar_servicio_deportista(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    (result, status_code) = AsignarServicioDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, 
                                                      servicio=mock_servicio().__dict__).execute()
    assert mock_session_instance.query.called
    assert result.get("respuesta")
    assert status_code == 200
    assert len(result["respuesta"]) > 0


@patch('test.mock_session', autospec=True)
def test_asignar_servicio_deportista_sin_autorizacion(mock_session):

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    with pytest.raises(InvalidAuthenticationError):
         AsignarServicioDeportista(session=mock_session_instance, headers={}, 
                                                      servicio=mock_servicio().__dict__).execute()
    
    assert not mock_session_instance.query.called


@patch('test.mock_session', autospec=True)
def test_asignar_servicio_deportista_ya_creado(mock_session, requests_mock):
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_servicio()

    with pytest.raises(BadRequestError):
        AsignarServicioDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, 
                                                      servicio=mock_servicio().__dict__).execute()
    

def mock_servicio():
    producto_servicio = ProductoServicio(fake.name(),fake.pyint(min_value=1000), fake.name(), fake.name(), fake.uuid4(), fake.uuid4())
    producto_servicio.id = fake.uuid4()
    return producto_servicio
