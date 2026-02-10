import pytest
from config import Settings


@pytest.fixture(scope="session")
def settings():
    return Settings()
