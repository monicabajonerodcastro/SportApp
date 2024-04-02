import pytest
from unittest.mock import patch
from faker import Faker

from src.commands.validar_token import ValidarToken
from src.services import servicio_token
from src.errors.errors import InvalidAuthentication

fake = Faker()

token_expirado = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE4NDk3MTUsImlhdCI6MTcxMTg0OTcwMCwic3ViIjoibW9uaWNhLmJham9uZXJvIn0.XufXd5idQhmAHeeaso46S-ytwSr9oLRjXpzfty9nqpw"
_SECRET_TEST = "secret"

def test_validar_token(mocker):
    mocker.patch("src.services.servicio_token.get_secret", return_value=_SECRET_TEST)
    token = servicio_token.generar_token(fake.user_name())
    json_request = {
        "token": token
    }
    (_, status) = ValidarToken(json_request=json_request).execute()
    assert status == 200


def test_validar_token_invalido(mocker):
    json_request = {
        "token": fake.text()
    }

    mocker.patch("src.services.servicio_token.get_secret", return_value=_SECRET_TEST)

    with pytest.raises(InvalidAuthentication):
        ValidarToken(json_request=json_request).execute()

def test_validar_token_expirado(mocker):

    mocker.patch("src.services.servicio_token.get_secret", return_value=_SECRET_TEST)

    json_request = {
        "token": token_expirado
    }

    with pytest.raises(InvalidAuthentication):
        ValidarToken(json_request=json_request).execute()

