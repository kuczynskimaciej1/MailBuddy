import pytest
from MessagingService.readers import IMAPReader
try:
    from personalSecrets import *
    secretsAvailable = True
except ImportError:
    secretsAvailable = False
from dataGenerators import getGmailOAuth2Secret


@pytest.fixture
def createImapReaderGmail(secret: str=getGmailOAuth2Secret) -> IMAPReader:
    return IMAPReader.getGmailConfig(secret)

def test_createImapReaderGmail(createImapReaderGmail):
    imap_reader = createImapReaderGmail
    assert getattr(imap_reader, "oauth2_access_token") != ""
    assert getattr(imap_reader, "host") != ""
    assert getattr(imap_reader, "port") != 0


@pytest.mark.skipif(not secretsAvailable, reason="Personal secrets not provided")
def test_loginInGmail(createImapReaderGmail, getUser):
    rdr = createImapReaderGmail
    u = getUser
    rdr.login(user=u.contact.email, password=u.password)
