
from unittest.mock import patch
from faker import Faker
import pytest
from src.errores.errores import InvalidAuthenticationError, MissingRequiredField
from src.modelos.rutina_alimenticia import RutinaAlimenticia
from src.comandos.crear_rutina_alimenticia import CrearRutinaAlimenticia

fake = Faker()
_TOKEN = fake.uuid4()

def rutina_alimenticia_mock():
    return RutinaAlimenticia(nombre=fake.name(), descripcion=fake.text())


def rutina_alimenticia_request():
    return (
        {
            "nombre": fake.name(),
            "descripcion": fake.text(),
            "productos" : [
                {
                    "producto_id" : fake.uuid4(),
                    "dosis": fake.text()
                }
            ]
        }
    )


@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    (response, status_code) = CrearRutinaAlimenticia(mock_session_instance,  {"Authorization": "Bearer"}, rutina_alimenticia_request()).execute()
    assert status_code == 201
    assert response.get("respuesta")
    assert response["respuesta"] == "Rutina alimenticia creada exitosamente"


@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia_sin_nombre(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    json_request = rutina_alimenticia_request()
    json_request["nombre"] = ""

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearRutinaAlimenticia(mock_session_instance,  {"Authorization": "Bearer"}, json_request).execute()

    assert exc_info.value.code == 404

@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia_sin_descripcion(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    json_request = rutina_alimenticia_request()
    json_request["descripcion"] = ""

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearRutinaAlimenticia(mock_session_instance,  {"Authorization": "Bearer"}, json_request).execute()

    assert exc_info.value.code == 404


@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia_sin_productos(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    json_request = rutina_alimenticia_request()
    json_request["productos"] = []

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearRutinaAlimenticia(mock_session_instance,  {"Authorization": "Bearer"}, json_request).execute()

    assert exc_info.value.code == 404


@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia_sin_producto_id(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    json_request = rutina_alimenticia_request()
    for prod in json_request["productos"]:
        prod["producto_id"] = ""

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearRutinaAlimenticia(mock_session_instance,  {"Authorization": "Bearer"}, json_request).execute()

    assert exc_info.value.code == 404

@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia_sin_dosis(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    json_request = rutina_alimenticia_request()
    for prod in json_request["productos"]:
        prod["dosis"] = ""

    with pytest.raises(MissingRequiredField) as exc_info:
        CrearRutinaAlimenticia(mock_session_instance,  {"Authorization": "Bearer"}, json_request).execute()

    assert exc_info.value.code == 404

@patch('test.mock_session', autospec=True)
def test_crear_rutina_alimenticia_sin_autorizacion(mock_session, requests_mock):
    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    json_request = rutina_alimenticia_request()
    
    with pytest.raises(InvalidAuthenticationError) as exc_info:
        CrearRutinaAlimenticia(mock_session_instance, {}, json_request).execute()
    
    assert exc_info.value.code == 403
