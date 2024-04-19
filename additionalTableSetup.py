from collections.abc import Iterable
from sqlalchemy import Column, ForeignKeyConstraint, Integer, TIMESTAMP, VARCHAR, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models import Message, Attachment, Contact, Group


class MessageAttachment(declarative_base()):
    __tablename__ = 'Message_Attachments'

    attachment_id = Column(Integer, ForeignKey(Attachment.attachment_id), primary_key=True)
    message_id = Column(Integer, ForeignKey(Message.message_id), primary_key=True)
    
    message = relationship(Message)
    attachment = relationship(Attachment)


class SendAttempt(declarative_base()):
    __tablename__ = 'Send_attempts'

    message_id = Column(Integer, ForeignKey(Message.message_id), primary_key=True)
    attempt = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    error_message = Column(VARCHAR(200), server_default='')

class GroupContacts(declarative_base()):
    __tablename__ = 'Group_Contacts'

    contact_id = Column(Contact.email.type, ForeignKey(Contact.email), primary_key=True)
    group_id = Column(Integer, ForeignKey(Group.id), primary_key=True)
    
    def __init__(self, **kwargs):
        self.group_id: int = kwargs.pop("group_id")
        self.contact_id: str = kwargs.pop("contact_id")
    
    # @classmethod
    # def FromGroup(cls, g: Group):
    #     [GroupContacts(group_id=g.id, contact_id=c_iter) for c_iter in g.contacts]
    
    # @classmethod
    # def get_contacts(cls, group_id: int) -> list[Contact | None]:
        
    
    # def add_record(self, c: Iterable[Contact], g: Group):
    #     for c in self.contacts:
    #         g._add_contact(c)
