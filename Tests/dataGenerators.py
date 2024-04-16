import pytest
from faker import Faker
try:
    import personalSecrets as ps
    secretsAvailable = True
except ImportError:
    secretsAvailable = False
from models import Contact, User
from collections.abc import Callable

@pytest.fixture
def getGmailOAuth2Secret() -> str:
    return ps.gmailOAuth2Secret

@pytest.fixture
def genContact() -> Callable[[], Contact]:
    def _generator() -> Contact:
        fake = Faker()
        return Contact(fake.first_name(), fake.last_name(), fake.simple_profile()["mail"])
    return _generator

@pytest.fixture
def genUser() -> Callable[[], User]:
    def _generator() -> User:
        fake = Faker()
        User(fake.first_name(), fake.last_name(), fake.simple_profile()["mail"], fake.password(length=15))
    return _generator

