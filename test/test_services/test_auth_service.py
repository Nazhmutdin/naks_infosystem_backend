import pytest
from datetime import datetime, timedelta

from services.auth_service import AuthService

service = AuthService()


def test_create_token():
    token = service.create_token(exp_dt=datetime.now() + timedelta(minutes=60), user_id="b7b6cc89931d460a92e4025734c968e4")

    assert token


@pytest.mark.parametrize(
        "payload",
        [
            {"exp_dt": "fsrefsd", "user_id": "b7b6cc89931d460a92e4025734c968e4"},
            {"exp_dt": datetime.now() + timedelta(minutes=60), "user_id": "fsfrrf"},
            {"exp_dt": "fsrefsd", "user_id": "fsfrrf"}
        ]
)
def test_create_token_failed(payload: dict):
    with pytest.raises(ValueError):
        service.create_token(**payload)


def test_read_token():
    token = service.create_token(exp_dt=datetime.now() + timedelta(minutes=60), user_id="b7b6cc89931d460a92e4025734c968e4")

    service.read_token(token)


def test_gen_refresh_token():
    token = service.gen_refresh_token(gen_dt=datetime.now(), exp_dt=datetime.now() + timedelta(minutes=60), user_id="b7b6cc89931d460a92e4025734c968e4")

    assert token


@pytest.mark.parametrize(
        "payload",
        [
            {"gen_dt": "cdwss", "exp_dt": "fsrefsd", "user_id": "b7b6cc89931d460a92e4025734c968e4"},
            {"gen_dt": "cdwss", "exp_dt": datetime.now() + timedelta(minutes=60), "user_id": "fsfrrf"},
            {"gen_dt": datetime.now(), "exp_dt": "fssrfr", "user_id": "fsfrrf"},
            {"gen_dt": "cdwss", "exp_dt": "fsrefsd", "user_id": "fsfrrf"}
        ]
)
def test_gen_refresh_token_failed(payload: dict):
    with pytest.raises(ValueError):
        service.create_token(**payload)


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
