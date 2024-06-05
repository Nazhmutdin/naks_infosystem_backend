import pytest

from shemas.request_shemas import *


@pytest.mark.usefixtures("request_refresh_tokens")
def test_refresh_token_request_shema(request_refresh_tokens: list[dict]):
    for el in request_refresh_tokens:
        expression = el.pop("expression")

        assert expression == RefreshTokenRequestShema.model_validate(el).dump_expression().__str__()


@pytest.mark.parametrize(
    "data",
    [
        {
            "tokens": [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxMzozODoxMiIsImV4cF9kdCI6IjIwMjQvMDUvMzAsIDEzOjM4OjEyIiwidXNlcl9pZGVudCI6ImI3YjZjYzg5OTMxZDQ2MGE5MmU0MDI1NzM0Yzk2OGU0IiwiaWRlbnQiOiI2MGI1ZTgxYTZjMjg0MDY0OGEwYmU2MGQyOTRmYmY2MyJ9.BhSBnMFt8dSkT5E5zSm-yrpObh0Jmc6bwS39iKw5ERw",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxMzozODoxMiIsImV4cF9kdCI6IjIwMjQvMDUvMzAsIDEzOjM4OjEyIiwidXNlcl9pZGVudCI6IjcyZTM4ZjYwYTAyNTQ5OWRiMjVjNzRhYWMwNGNhMTliIiwiaWRlbnQiOiIyZTQzMDQ4YWRiYmM0ZDVlYjZmMTlhMWMyODdlNGUwOCJ9.kvBSU70rKnzewF7MjQnnIIGAdkWn9ZWfMDCR1KVILyw"
            ],
            "user_idents": [
                "b7b6cc89931d460a92e4025734c968e4",
                "2e43048adbbc4d5eb6f19a1c288"
            ]
        },
        {
            "gen_dt_from": "hello"
        },
        {
            "tokens": [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzzozODoxMiIsImV4cF9kdCI6IjIwMjQvMDUvMzAsIDEzOjM4OjEyIiwidXNlcl9pZGVudCI6ImI3YjZjYzg5OTMxZDQ2MGE5MmU0MDI1NzM0Yzk2OGU0IiwiaWRlbnQiOiI2MGI1ZTgxYTZjMjg0MDY0OGEwYmU2MGQyOTRmYmY2MyJ9.BhSBnMFt8dSkT5E5zSm-yrpObh0Jmc6bwS39iKw5ERw",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnZW5fZHQiOiIyMDI0LzA1LzI5LCAxMzozODoxMiIsImV4cF9kdCI6IjIwMjQvMDUvMzAsIDEzOjM4OjEyIiwidXNlcl9pZGVudCI6IjcyZTM4ZjYwYTAyNTQ5OWRiMjVjNzRhYWMwNGNhMTliIiwiaWRlbnQiOiIyZTQzMDQ4YWRiYmM0ZDVlYjZmMTlhMWMyODdlNGUwOCJ9.kvBSU70rKnzewF7MjQnnIIGAdkWn9ZWfMDCR1KVILyw"
            ]
        },
        {
            "revoked": "hello"
        }
    ]
)
def test_refresh_token_request_shema_failed(data: dict):

    with pytest.raises(ValueError):

        RefreshTokenRequestShema.model_validate(data).dump_expression().__str__()
