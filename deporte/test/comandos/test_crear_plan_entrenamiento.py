import pytest
from unittest.mock import patch
from faker import Faker
from test.mock_session import MockSession
from src.comandos.crear_plan_entrenamiento import CrearPlanEntrenamiento
from src.modelos.plan_entrenamiento import PlanEntrenamiento
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField

fake = Faker()
_TOKEN = fake.uuid4()
_ENTRENAMIENTO = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

def crear_plan_emtrenamiento(session, plan_mock, headers):
    return CrearPlanEntrenamiento(session,headers,
                        {"nombre": plan_mock.nombre,
                        "deporte": plan_mock.deporte,
                        "entrenamientos": {                            
                        } }                  
                     )


def plan_mockq():
    return PlanEntrenamiento(fake.name(), fake.uuid4())

def plan_mockq_missing():
    return PlanEntrenamiento("", fake.uuid4())

@patch('test.mock_session', autospec=True)
def test_crear_plan_entrenamiento(mock_session,requests_mock):
    my_plan_mock = plan_mockq()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = my_plan_mock
  
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    crear_plan_emtrenamiento_respuesta = crear_plan_emtrenamiento(session=mock_session_instance, plan_mock=my_plan_mock, headers={"Authorization": "Bearer"} )
    result = crear_plan_emtrenamiento_respuesta.execute()
    assert len(result) > 0

@patch('test.mock_session', autospec=True)
def test_crear_plan_entrenamiento_missing_requiredfield(mock_session, requests_mock):
    my_plan_mock = plan_mockq_missing()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value

    mock_query.filter.return_value.first.return_value = my_plan_mock
  
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    
    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_plan_emtrenamiento(session=mock_session_instance, plan_mock=my_plan_mock, headers={"Authorization": "Bearer"} )
        service.execute()
        
    assert exc_info.value.code == 404




