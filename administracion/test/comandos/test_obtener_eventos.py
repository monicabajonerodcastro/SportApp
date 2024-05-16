import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_eventos import ObtenerEventos, ObtenerEventosCercanos, ObtenerEventosDeportista, ObtenerNuevosEventos
from src.modelos.evento import Evento
from test.mock_session import MockSession
from src.errores.errores import InvalidAuthenticationError

fake = Faker()
_SECRET_TEST = "secret"
_ID_DEPORTE = fake.uuid4()
_ID_SOCIO = fake.uuid4()
_ID_USUARIO = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_eventos(mock_session, requests_mock, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    service = ObtenerEventos(session=mock_session_instance, headers={"Authorization": "Bearer "})
    (_, status_code) = service.execute()
    assert mock_session_instance.query.called
    assert status_code == 200

@patch('test.mock_session', autospec=True)
def test_obtener_evento_id_sin_autorizacion(mock_session, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    with pytest.raises(InvalidAuthenticationError):
        ObtenerEventos(session=mock_session_instance, headers={}).execute()
    
    assert not mock_session_instance.query.called

@patch('test.mock_session', autospec=True)
def test_obtener_eventos_cercanos(mock_session, requests_mock, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
    requests_mock.get('http://host-personas-test/personas/'+_ID_USUARIO, json={"direccion": {"ubicacion_latitud": 1, "ubicacion_longitud": 1}})
    
    service = ObtenerEventosCercanos(session=mock_session_instance, headers={"Authorization": "Bearer "}, latitud=1, longitud=1)
    (_, status_code) = service.execute()
    assert mock_session_instance.query.called
    assert status_code == 200

@patch('test.mock_session', autospec=True)
def test_obtener_eventos_cercanos_sin_autorizacion(mock_session, requests_mock, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    requests_mock.get('http://host-personas-test/personas/'+_ID_USUARIO, json={"direccion": {"ubicacion_latitud": 1, "ubicacion_longitud": 1}})
    
    with pytest.raises(InvalidAuthenticationError):
        ObtenerEventosCercanos(session=mock_session_instance, headers={}, latitud=1, longitud=1).execute()

    assert not mock_session_instance.query.called

@patch('test.mock_session', autospec=True)
def test_obtener_eventos_deportista(mock_session, requests_mock, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
    
    service = ObtenerEventosDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "})
    (_, status_code) = service.execute()
    assert mock_session_instance.query.called
    assert status_code == 200


@patch('test.mock_session', autospec=True)
def test_obtener_evento_deportista_sin_autorizacion(mock_session, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    with pytest.raises(InvalidAuthenticationError):
        ObtenerEventosDeportista(session=mock_session_instance, headers={}).execute()
    
    assert not mock_session_instance.query.called


def eventos_mock():
    return [Evento(id=fake.uuid4(), nombre=fake.name(), fecha_inicio=fake.date_time(), fecha_fin=fake.date_time(), id_deporte=_ID_DEPORTE, id_socio=_ID_SOCIO, detalle=fake.text())]

@patch('test.mock_session', autospec=True)
def test_obtener_eventos_nuevos(mock_session, requests_mock, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
    requests_mock.get('http://host-personas-test/personas/'+_ID_USUARIO, json={"direccion": {"ubicacion_latitud": 1, "ubicacion_longitud": 1}})
    
    service = ObtenerNuevosEventos(session=mock_session_instance, headers={"Authorization": "Bearer "}, latitud=1, longitud=1, fecha_ultima_conexion=1)
    (_, status_code) = service.execute()
    assert mock_session_instance.query.called
    assert status_code == 200

@patch('test.mock_session', autospec=True)
def test_obtener_eventos_nuevos_sin_autorizacion(mock_session, requests_mock, mocker):
    mock_eventos = eventos_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_eventos

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    requests_mock.get('http://host-personas-test/personas/'+_ID_USUARIO, json={"direccion": {"ubicacion_latitud": 1, "ubicacion_longitud": 1}})
    
    with pytest.raises(InvalidAuthenticationError):
        ObtenerNuevosEventos(session=mock_session_instance, headers={}, fecha_ultima_conexion=1, latitud=1, longitud=1).execute()

    assert not mock_session_instance.query.called