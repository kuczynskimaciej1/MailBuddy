from __future__ import annotations
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from sqlalchemy import Column, Integer, String, LargeBinary, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from abc import ABCMeta, abstractmethod
from pathlib import Path
import re


__all__ = ["Template", "Attachment", "Contact", "User", "Message", "Group"]


class IModel(declarative_base()):
    __abstract__ = True
    run_loading = True
    saveQueued: list[IModel] = []

    @staticmethod
    def queueSave(child):
        if not IModel.run_loading:
            IModel.saveQueued.append(child)


class Template(IModel):
    all_instances: list[Template] = []
    __tablename__ = "Templates"

    _id = Column("id", Integer, primary_key=True)
    _name = Column("name", String(100), nullable=True)
    _content = Column("content", String, nullable=True)

    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop('_id', None)
        self.name = kwargs.pop('_name', None)
        self.content = kwargs.pop('_content', None)
        Template.all_instances.append(self)
        IModel.queueSave(child=self)


    def __str__(self) -> str:
        return self.name if self.name != None else "<puste>"
    
    def __repr__(self):
        return f"Template(_name={self.name}, _content={self.content}, _id={self.id})"

# region Properties
    @hybrid_property
    def id(self):
        return self._id

    @hybrid_property
    def name(self):
        return self._name

    @hybrid_property
    def content(self):
        return self._content

    @id.setter
    def id(self, newValue: int):
        if newValue:
            self._id = newValue
        else:
            self._id = max((i.id for i in Template.all_instances), default=0) + 1

    @name.setter
    def name(self, value: str | None):
        self._name = value

    @content.setter
    def content(self, value: str | None):
        self._content = value
#endregion

class Attachment(IModel):
    all_instances = []
    __tablename__ = "Attachments"

    attachment_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=True)
    file = Column(LargeBinary, nullable=True)

    def __init__(self, path, type, attachment_id: int | None = None) -> None:
        self.attachment_id = attachment_id
        self.path = path
        self.type = type
        Attachment.all_instances.append(self)
        IModel.queueSave(child=self)

    # def prepareAttachment(self):
    #     att = MIMEApplication(open(self.path, "rb").read(), _subtype=self.type)
    #     att.add_header('Content-Disposition',
    #                    "attachment; filename= %s" % self.path.split("\\")[-1])
    #     return att


class Contact(IModel):
    all_instances = []
    __tablename__ = "Contacts"

    _email = Column("email", String(100), primary_key=True)
    _first_name = Column("first_name", String(50), nullable=True)
    _last_name = Column("last_name", String(50), nullable=True)

    def __init__(self, **kwargs) -> None:
        """Creates instance and adds it to all_instances
        Args:
            first_name (str): any string
            last_name (str): any string
            email (str): must match standard pattern x@y.z
        Raises:
            AttributeError: when email doesn't match standard pattern
        """
        self.email = kwargs.pop("_email", None)
        self.first_name = kwargs.pop("_first_name", None)
        self.last_name = kwargs.pop("_last_name", None)
        Contact.all_instances.append(self)
        IModel.queueSave(child=self)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, <{self.email}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Contact):
            return NotImplemented
        return self.email == other.email and self.first_name == other.first_name and self.last_name == other.last_name

    @classmethod
    def get_by_id(cls, searched_id: int) -> Contact | None:
        for candidate in cls.all_instances:
            if candidate.id == searched_id:
                return candidate
        return None

    @staticmethod
    def isEmail(candidate: str) -> bool:
        if re.match(r"[^@]+@[^@]+\.[^@]+", candidate):
            return True
        return False
    
# region Properties
    @hybrid_property
    def email(self):
        return self._email

    @hybrid_property
    def first_name(self):
        return self._first_name
    
    @hybrid_property
    def last_name(self):
        return self._last_name

    @email.setter
    def email(self, newValue: int):
        if not Contact.isEmail(newValue):
            raise AttributeError("Value is not an email")
        self._email = newValue

    @first_name.setter
    def first_name(self, value: str | None):
        self._first_name = value

    @last_name.setter
    def last_name(self, value: str | None):
        self._last_name = value
#endregion


class User():
    all_instances = []

    def __init__(self, first_name: str, last_name: str,
                 email: str, password: str) -> None:
        self.contact = Contact(first_name, last_name, email)
        self.password = password
        User.all_instances.append(self)
        IModel.queueSave(child=self)


class Message(IModel, MIMEMultipart):
    all_instances = []
    __tablename__ = "Messages"

    message_id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)
    template_id = Column(Integer, nullable=False)
    sent_at = Column(TIMESTAMP, default=func.now())

    # TODO
    # trigger = relationship("Trigger")
    # contact = relationship("Contact")
    # template = relationship("Template")

    def __init__(self, recipient: Contact,
                 att: list[Attachment] = None) -> None:
        self.recipient = recipient
        self.att = att
        Message.all_instances.append(self)
        IModel.queueSave(child=self)


class Group(IModel):
    all_instances: list[Group] = []
    __tablename__ = "Groups"
    
    _id = Column("id", Integer, primary_key=True)
    _name = Column("name", String(100), nullable=True)
    
    def __init__(self, **kwargs):
        self.id: int = kwargs.pop('_id', None)
        self.name: str = kwargs.pop('_name', "")
        self.contacts : list[Contact] = kwargs.pop("_contacts", [])
        IModel.queueSave(self)
    
    def __str__(self):
        return f"{self.id}: {self.name}"
    
    @classmethod
    def get_by_id(cls, searched_id: int) -> Group | None:
        for candidate in cls.all_instances:
            if candidate.id == searched_id:
                return candidate
        return None
    
    def _add_contact(self, c: Contact) -> bool:
        if c not in self.contacts:
            self.contacts.append(c)
            return True
        return False
    
#region Properties
    @hybrid_property
    def id(self):
        return self._id

    @hybrid_property
    def name(self):
        return self._name
    
    @id.setter
    def id(self, newValue: int):
        if newValue:
            self._id = newValue
        else:
            self._id = max((i.id for i in Group.all_instances), default=-1) + 1

    @name.setter
    def name(self, value: str | None):
        self._name = value
#endregion