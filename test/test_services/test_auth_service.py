import pytest
from datetime import datetime, timedelta

from services.auth_service import AuthService

service = AuthService()


def test_create_access_token():
    token = service.create_access_token(gen_dt=datetime.now() + timedelta(minutes=60), user_ident="b7b6cc89931d460a92e4025734c968e4")

    assert token


@pytest.mark.parametrize(
        "payload",
        [
            {"gen_dt": "fsrefsd", "user_ident": "b7b6cc89931d460a92e4025734c968e4"},
            {"gen_dt": datetime.now() + timedelta(minutes=60), "user_ident": "fsfrrf"},
            {"gen_dt": "fsrefsd", "user_ident": "fsfrrf"}
        ]
)
def test_create_token_failed(payload: dict):
    with pytest.raises(ValueError):
        service.create_access_token(**payload)


def test_read_token():
    token = service.create_access_token(
        gen_dt=datetime.now() + timedelta(minutes=60), 
        user_ident="b7b6cc89931d460a92e4025734c968e4"
    )

    service.read_token(token)


def test_create_refresh_token():
    token = service.create_refresh_token(
        gen_dt=datetime.now(), 
        exp_dt=datetime.now() + timedelta(minutes=60), 
        user_ident="b7b6cc89931d460a92e4025734c968e4",
        ident="b7c6cc89931d460a92e4025734c968e4"
    )

    assert token


@pytest.mark.parametrize(
        "payload",
        [
            {"gen_dt": "cdwss", "exp_dt": "fsrefsd", "user_ident": "b7b6cc89931d460a92e4025734c968e4"},
            {"gen_dt": "cdwss", "exp_dt": datetime.now() + timedelta(minutes=60), "user_ident": "fsfrrf"},
            {"gen_dt": datetime.now(), "exp_dt": "fssrfr", "user_ident": "fsfrrf"},
            {"gen_dt": "cdwss", "exp_dt": "fsrefsd", "user_ident": "fsfrrf"}
        ]
)
def test_create_refresh_token_failed(payload: dict):
    with pytest.raises(ValueError):
        service.create_refresh_token(**payload)


@pytest.mark.parametrize(
    "token",
    [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxMDo1MTowMiIsInVzZXJfaWRlbnQiOiJiN2I2Y2M4OTkzMWQ0NjBhOTJlNDAyNTczNGM5NjhlNCJ9.scwrMCIRTx-rhwqKFXX3Jjd8sN5vtBUD9Uc56C96dII"
    ]
)
def test_validate_access_token(token: str):
    assert service.validate_access_token(token)

    
@pytest.mark.parametrize(
    "token",
    [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxMDo1mTowMiIsInVzZXJfaWRlbnQiOiJiN2I2Y2M4OTkzMWQ0NjBhOTJlNDAyNTczNGM5NjhlNCJ9.scwrMCIRTx-rhwqKFXX3Jjd8sN5vtBUD9Uc56C96dII"
    ]
)
def test_validate_access_token_invalid(token: str):
    assert not service.validate_access_token(token)


@pytest.mark.parametrize(
    "token",
    [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxMzozODoxMiIsImV4cF9kdCI6IjIwMjQvMDUvMzAsIDEzOjM4OjEyIiwidXNlcl9pZGVudCI6IjcyZTM4ZjYwYTAyNTQ5OWRiMjVjNzRhYWMwNGNhMTliIiwiaWRlbnQiOiIyZTQzMDQ4YWRiYmM0ZDVlYjZmMTlhMWMyODdlNGUwOCJ9.kvBSU70rKnzewF7MjQnnIIGAdkWn9ZWfMDCR1KVILyw"
    ]
)
def test_validate_refresh_token(token: str):
    assert service.validate_refresh_token(token)

    
@pytest.mark.parametrize(
    "token",
    [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxmzozODoxMiIsImV4cF9kdCI6IjIwMjQvMDUvMzAsIDEzOjM4OjEyIiwidXNlcl9pZGVudCI6IjcyZTM4ZjYwYTAyNTQ5OWRiMjVjNzRhYWMwNGNhMTliIiwiaWRlbnQiOiIyZTQzMDQ4YWRiYmM0ZDVlYjZmMTlhMWMyODdlNGUwOCJ9.kvBSU70rKnzewF7MjQnnIIGAdkWn9ZWfMDCR1KVILyw"
    ]
)
def test_validate_refresh_token_invalid(token: str):
    assert not service.validate_refresh_token(token)


def test_hash_password():
    string = "fsfrfrfrecawsd"

    assert service.hash_password(string)


def test_successful_password_validation():
    string = "hrtydfdgt"

    hashed = service.hash_password(string)

    assert service.validate_password(string, hashed)
    

def test_failed_password_validation():
    string = "hrtydfdgt"

    hashed = service.hash_password(string)

    assert not service.validate_password("fsrsdd", hashed)
