import pytest
from unittest.mock import patch
from faker import Faker

from src.commands.validar_token import ValidarToken
from src.services import servicio_token
from src.errors.errors import InvalidAuthentication
import random

fake = Faker()

token_expirado = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE4MzM4ODMsImlhdCI6MTcxMTgzMjk4Mywic3ViIjoibW9uaWNhLmJham9uZXJvIn0.5SnulBHcv2y__jo9dZbEUibPVE2_A50aQ2xkaxZJmfs"

def test_validar_token():
    token = servicio_token.generar_token(fake.user_name())
    json_request = {
        "token": token
    }
    (_, status) = ValidarToken(json_request=json_request).execute()
    assert status == 200


def test_validar_token_invalido():

    json_request = {
        "token": fake.name()
    }

    with pytest.raises(InvalidAuthentication):
        ValidarToken(json_request=json_request).execute()

def test_validar_token_expirado():

    json_request = {
        "token": token_expirado
    }

    with pytest.raises(InvalidAuthentication):
        ValidarToken(json_request=json_request).execute()

