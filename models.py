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


__all__ = ["Template", "Attachment", "Contact", "User", "Message"]


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

    email = Column(String(100), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))

    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        """Creates instance and adds it to all_instances
        Args:
            first_name (str): any string
            last_name (str): any string
            email (str): must match standard pattern x@y.z
        Raises:
            AttributeError: when email doesn't match standard pattern
        """
        if Contact.isEmail(email):
            self.email = email
        else:
            raise AttributeError(f"{email} is not valid email")
        self.first_name = first_name
        self.last_name = last_name
        Contact.all_instances.append(self)
        IModel.queueSave(child=self)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, <{self.email}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Contact):
            return NotImplemented
        return self.email == other.email and self.first_name == other.first_name and self.last_name == other.last_name

    @staticmethod
    def isEmail(candidate: str) -> bool:
        if re.match(r"[^@]+@[^@]+\.[^@]+", candidate):
            return True
        return False


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
