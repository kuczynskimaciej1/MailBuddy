from sqlalchemy import Column, ForeignKeyConstraint, Integer, TIMESTAMP, VARCHAR, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models import Message, Attachment


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
