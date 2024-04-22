import pytest
from unittest.mock import patch
from faker import Faker

from src.errores.errores import BadRequestError, NotFoundError
from src.comandos.enviar_productos_rutina_alimenticia import EnviarProductosRutinaAlimenticia
from src.modelos.rutina_alimenticia import RutinaAlimenticia
from test.mock_session import MockSession


fake = Faker()
_TOKEN = fake.uuid4()
_ID_USUARIO = fake.uuid4()
_ID_RUTINA_ALIMENTICIA = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_enviar_productos_rutina_alimenticia(mock_session, requests_mock):

    rutina_alimenticia_mock = mock_rutina_alimenticia()
    deportista_mock = mock_deportista()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
    requests_mock.get(f'http://host-personas-test/personas/{_ID_USUARIO}', json=deportista_mock)
    requests_mock.get(f'http://host-personas-test/personas/perfildeportivo/{_ID_USUARIO}', json=perfil_deportivo_mock())

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = rutina_alimenticia_mock
    
    (result, status_code) = EnviarProductosRutinaAlimenticia(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA).execute()

    assert status_code == 200
    assert result.get("respuesta")
    assert result["respuesta"] == "Solicitud de productos enviada exitosamente. De 5 a 8 días recibirá sus productos"


    assert status_code == 200


@patch('test.mock_session', autospec=True)
def test_enviar_productos_rutina_alimenticia_no_respuesta_usuario(mock_session, requests_mock):

    rutina_alimenticia_mock = mock_rutina_alimenticia()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
    requests_mock.get(f'http://host-personas-test/personas/{_ID_USUARIO}', json={"description":"BadRequestError"}, status_code=400)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = rutina_alimenticia_mock

    with pytest.raises(BadRequestError) as exc_info:
        EnviarProductosRutinaAlimenticia(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA).execute()

    assert exc_info.value.code == 400


@patch('test.mock_session', autospec=True)
def test_enviar_productos_rutina_alimenticia_no_existente(mock_session, requests_mock):

    deportista_mock = mock_deportista()

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
    requests_mock.get(f'http://host-personas-test/personas/{_ID_USUARIO}', json=deportista_mock)
    requests_mock.get(f'http://host-personas-test/personas/perfildeportivo/{_ID_USUARIO}', json=perfil_deportivo_mock())

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None
    
    with pytest.raises(NotFoundError) as exc_info:
        EnviarProductosRutinaAlimenticia(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_rutina_alimenticia=_ID_RUTINA_ALIMENTICIA).execute()

    assert exc_info.value.code == 404

def mock_deportista():
    return {"apellido":fake.name(), "email": fake.email(), "id": fake.uuid4(), "nombre": fake.name(), "numero_identificacion": fake.pyint(min_value=1000),
        "password": fake.word(),  "rol": "DEPORTISTA", "suscripcion": fake.uuid4(), "tipo_id": "CC", "username": fake.name(), "direccion" : "Calle 123"}


def mock_rutina_alimenticia():
    return RutinaAlimenticia(nombre=fake.name(), descripcion=fake.text())

def perfil_deportivo_mock():
    return {"alergias": fake.word(), "altura": fake.pyint(min_value=100), "antiguedad_residencia": fake.pyint(min_value=1),
    "ciudad_nacimiento": fake.word(), "ciudad_residencia": fake.word(), "deporte": fake.word(), "direccion": fake.word(),
    "edad": fake.pyint(), "ftp": fake.pyint(), "genero": fake.word(), "horas_semanal": fake.pyint(), "id": fake.uuid4(),
    "id_usuario": fake.uuid4(), "imc":fake.pyint(), "pais_nacimiento": fake.word(), "pais_residencia": fake.word(),
    "peso":fake.pyint(), "peso_objetivo":fake.pyint(), "plan_nutricional": fake.word(), "preferencia_alimenticia": fake.word(),
    "tipo_sangre":fake.word(),"url_historia_clinica": fake.url(), "vo2max": fake.pyint()
}



