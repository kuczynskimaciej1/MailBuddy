import pytest
from MessagingService.readers import IMAPReader
from models import User
from personalSecrets import *
from dataGenerators import getGmailOAuth2Secret


@pytest.fixture
def createImapReaderGmail(secret: str=getGmailOAuth2Secret) -> IMAPReader:
    return IMAPReader.getGmailConfig(secret)

def test_createImapReaderGmail(createImapReaderGmail):
    imap_reader = createImapReaderGmail
    assert getattr(imap_reader, "oauth2_access_token") != ""
    assert getattr(imap_reader, "host") != ""
    assert getattr(imap_reader, "port") != 0


def test_loginInGmail(createImapReaderGmail, getUser):
    rdr = createImapReaderGmail
    u = getUser
    rdr.login(user=u.contact.email, password=u.password)
