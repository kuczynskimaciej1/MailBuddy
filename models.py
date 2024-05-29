from __future__ import annotations
from email.mime.multipart import MIMEMultipart
from openpyxl import load_workbook
from sqlalchemy import BOOLEAN, Column, ForeignKey, Integer, String, LargeBinary, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
import re


__all__ = ["Template", "Attachment", "Contact", "User", "Message", "Group"]


class IModel(declarative_base()):
    __abstract__ = True
    run_loading = True
    addQueued: list[IModel] = []
    updateQueued: list[IModel] = []
    retrieveAdditionalQueued: list[IModel] = []

    @staticmethod
    def queueSave(child):
        if not IModel.run_loading:
            IModel.addQueued.append(child)
    
    @staticmethod
    def queueToUpdate(child):
        if not IModel.run_loading:
            IModel.updateQueued.append(child)
       
    @staticmethod
    def retrieveAdditionalData(child):
        if isinstance(child, Template):
            IModel.retrieveAdditionalQueued.append(child)


class DataImport(IModel):
    all_instances: list[DataImport] = []
    __tablename__ = "DataImport"

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    _name = Column("name", String(100))
    _localPath = Column("localPath", String(255), nullable=True)
    _content = Column("content", LargeBinary, nullable=True)
    
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop('_id', None)
        self.name = kwargs.pop('_name', None)
        self.localPath = kwargs.pop('_localPath', None)
        self.content = kwargs.pop('_content', None)
        DataImport.all_instances.append(self)
        IModel.queueSave(child=self)
        
    def getColumnPreview(self) -> dict | None:
        workbook = load_workbook(self.localPath, read_only=True)
        result = dict()
        for sheet in workbook:
            first_row = next(sheet.iter_rows(values_only=True))
            if "Email" not in first_row:
                continue
            
            columns = first_row
            dataPreviewRow = next(sheet.iter_rows(min_row=2, values_only=True))
            for idx, c in enumerate(columns):
                result[c] = dataPreviewRow[idx]
        return result if len(result) > 0 else None
            

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
    
    @hybrid_property
    def localPath(self):
        return self._localPath
    
    @id.setter
    def id(self, newValue: int):
        self._id = newValue

    @name.setter
    def name(self, value: str | None):
        self._name = value
        IModel.queueToUpdate(self)

    @content.setter
    def content(self, value: object | None):
        self._content = value
        IModel.queueToUpdate(self)
        
    @localPath.setter
    def localPath(self, value: str | None):
        self._localPath = value
        IModel.queueToUpdate(self)
#endregion


class Template(IModel):
    all_instances: list[Template] = []
    __tablename__ = "Templates"

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    _name = Column("name", String(100), nullable=True)
    _content = Column("content", String, nullable=True)
    _dataimport_id = Column("dataimport_id", Integer, #ForeignKey("DataImport.id", ondelete='SET NULL'), 
                            nullable=True)
    
    # dataImportRel = relationship(DataImport, foreign_keys=[DataImport._id])
    
    def __init__(self, **kwargs) -> None:
        self.id: int = kwargs.pop('_id', None)
        self.name: str = kwargs.pop('_name', None)
        self.content: object = kwargs.pop('_content', None)
        self.dataimport: DataImport = None
        self.dataimport_id: int = kwargs.pop("_dataimport_id", None)
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
    
    @hybrid_property
    def dataimport_id(self) -> DataImport:
        return self._dataimport_id

    @id.setter
    def id(self, newValue: int):
        # TODO: if initial setup / loading from db
        self._id = newValue

    @name.setter
    def name(self, value: str | None):
        self._name = value
        IModel.queueToUpdate(self)

    @content.setter
    def content(self, value: str | None):
        self._content = value
        IModel.queueToUpdate(self)
        
    @dataimport_id.setter
    def dataimport_id(self, value: int | None):
        self._dataimport_id = value
        IModel.queueToUpdate(self)
        IModel.retrieveAdditionalData(self)
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
    _first_name = Column("first_name", String(50))
    _last_name = Column("last_name", String(50))

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
        self.first_name = kwargs.pop("_first_name", "")
        self.last_name = kwargs.pop("_last_name", "")
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
        if candidate == None:
            return False
        
        if re.match(r"^(?!.*@.*@.*$)[^@]+@[^@]+\.[^@]+$/g", candidate):
            return False    
        
        return True
    
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
    def email(self, newValue: str):
        if not Contact.isEmail(newValue):
            raise AttributeError(f"{newValue} is not an email")
        self._email = newValue

    @first_name.setter
    def first_name(self, value: str | None):
        self._first_name = value

    @last_name.setter
    def last_name(self, value: str | None):
        self._last_name = value
#endregion


class User(IModel):
    all_instances = []
    __tablename__ = "Users"

    _id = Column("_id", Integer, primary_key=True, autoincrement=True)
    _email = Column("email", String(100), ForeignKey('Contacts.email'), unique=True)
    _selected = Column("selected", BOOLEAN)
    
    contactRel = relationship(Contact, foreign_keys=[_email])
    

    def __init__(self, **kwargs) -> None:
        self._email = kwargs.pop("_email")
        self.password = kwargs.pop("_password", None)
        self.contact = self.getExistingContact(kwargs.pop("_first_name", None), kwargs.pop("_last_name", None))
        self._selected = kwargs.pop("_selected", None)
        User.all_instances.append(self)
        IModel.queueSave(child=self)
    
    @staticmethod
    def GetCurrentUser() -> User | None:
        for u in User.all_instances:
            if u._selected:
                return u
        return None
        
    def getExistingContact(self, first_name, last_name) -> Contact:
        for c in Contact.all_instances:
            if c.email == self._email:
                return c
        return Contact(_first_name=first_name, _last_name=last_name, _email=self._email)


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
        self.contacts: list[Contact] = kwargs.pop("_contacts", [])
        Group.all_instances.append(self)
        IModel.queueSave(self)
        
    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str | None):
        self._name = value
        IModel.queueToUpdate(self)
    
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
        IModel.queueToUpdate(self)
#endregion
