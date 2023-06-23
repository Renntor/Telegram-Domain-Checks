import pytest
from src.whois import Whois


@pytest.fixture
def domain():
    return Whois('ya.ru')

def test_Whois(domain):

    assert str(domain) == 'ya.ru'
    assert repr(domain) == "Whois('ya.ru')"
