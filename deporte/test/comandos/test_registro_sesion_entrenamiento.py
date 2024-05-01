import pytest
from unittest.mock import patch
from faker import Faker

from src.errores.errores import NotFoundError
from src.modelos.sesion_entrenamiento import SesionEntrenamiento
from src.comandos.registrar_sesion_entrenamiento import IniciarSesionEntrenamiento, FinalizarSesionEntrenamiento
from test.mock_session import MockSession

fake = Faker()
_TOKEN = fake.uuid4()
_ID_USUARIO = fake.uuid4()
_ID_SESION_ENTRENAMIENTO = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


@patch('test.mock_session', autospec=True)
def test_iniciar_sesion_entrenamiento(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    (result, status_code) = IniciarSesionEntrenamiento(session=mock_session_instance, headers={"Authorization": "Bearer "}).execute()

    assert status_code == 201
    assert result["token"] == _TOKEN
    assert result["respuesta"] == "Sesión de entrenamiento iniciada exitosamente"


@patch('test.mock_session', autospec=True)
def test_finalizar_sesion_entrenamiento(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_sesion_entrenamiento()

    (result, status_code) = FinalizarSesionEntrenamiento(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_sesion_entrenamiento=_ID_SESION_ENTRENAMIENTO).execute()

    assert status_code == 200
    assert result["token"] == _TOKEN
    assert result["respuesta"] == "Sesión de entrenamiento finalizada exitosamente"


@patch('test.mock_session', autospec=True)
def test_finalizar_sesion_entrenamiento_no_existente(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        FinalizarSesionEntrenamiento(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_sesion_entrenamiento=_ID_SESION_ENTRENAMIENTO).execute()
    
    assert exc_info.value.code == 404
    assert exc_info.value.description == "No se ha iniciado la sesión de entrenamiento " + _ID_SESION_ENTRENAMIENTO

def mock_sesion_entrenamiento():
    return SesionEntrenamiento(id_deportista=_ID_USUARIO)