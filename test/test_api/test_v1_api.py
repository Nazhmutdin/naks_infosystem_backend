import pytest

from client import client


class BaseTestCRUDEndpoints:

    def test_add(self, api_path: str): ...
