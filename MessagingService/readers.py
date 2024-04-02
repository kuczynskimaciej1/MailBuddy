from __future__ import annotations
from abc import ABCMeta, abstractmethod
from builtins import list as _list
from imaplib import IMAP4_SSL, IMAP4
from base64 import b64encode
import ssl


class IReader(metaclass=ABCMeta):
    @abstractmethod
    def ReadAll() -> None:
        raise AssertionError

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        if cls is IReader:
            if any("ReadAll" in B.__dict__ for B in __subclass.__mro__):
                return True
        return NotImplemented


class IMAPReader(IMAP4_SSL, IReader):
    def __init__(self, host: str = "", port: int = 993, *, ssl_context: ssl.SSLContext |
                 None = ssl.create_default_context(), timeout: float | None = None) -> None:
        super().__init__(host, port, ssl_context=ssl_context, timeout=timeout)

    def ReadAll(messages, limiter) -> None:
        pass

    @staticmethod
    def GenerateOAuth2String(username, access_token, base64_encode=True) -> bytes | str:
        auth_string = f'user={username}\001auth=Bearer {access_token}\001\001'.encode('utf-8')
        if base64_encode:
            auth_string = b64encode(auth_string)
        return auth_string

    def login(self, user: str, password: str):
        if self.oauth2_access_token:
            auth_string = IMAPReader.GenerateOAuth2String(user, self.oauth2_access_token, False)
            self.authenticate("XOAUTH2", lambda x: auth_string)
            
        try:
            response = super().login(user, password)
        except IMAP4.error as e:
            print(f"Login error, {e}")
        return

    @classmethod
    def getGmailConfig(cls, oauth2_access_token: str | None = None) -> IMAPReader:
        """Returns IMAPReader with default Gmail config
        data via https://developers.google.com/gmail/imap/imap-smtp#protocol

        Returns:
            IMAPReader: Instantiated IMAPReader
        """
        result = IMAPReader('imap.gmail.com', 993)
        if oauth2_access_token:
            result.oauth2_access_token = oauth2_access_token

        return result


class MockIMAPReader(IReader):
    def __init__(self, host: str = "", port: int = 143,
                 timeout: float | None = None) -> None:
        pass

    def ReadAll() -> None:
        raise AssertionError

    @classmethod
    def getGmailConfig(cls) -> MockIMAPReader:
        return MockIMAPReader()
