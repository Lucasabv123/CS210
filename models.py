from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    user_id      = Column(Integer, primary_key=True)
    name         = Column(String, nullable=False)
    email        = Column(String, nullable=False, unique=True)
    signup_date  = Column(DateTime, nullable=False)
    current_plan = Column(String, nullable=False)
    subscriptions = relationship("Subscription", back_populates="contact")
    interactions  = relationship("Interaction",  back_populates="contact")
    notifications = relationship("Notification", back_populates="contact")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    subscription_id = Column(Integer, primary_key=True)
    contact_id      = Column(Integer, ForeignKey('contacts.user_id', ondelete='CASCADE'), nullable=False)
    plan_tier       = Column(String, nullable=False)
    start_date      = Column(Date, nullable=False)
    end_date        = Column(Date, nullable=True)
    contact         = relationship("Contact", back_populates="subscriptions")

class Interaction(Base):
    __tablename__ = 'interactions'
    interaction_id = Column(Integer, primary_key=True)
    contact_id     = Column(Integer, ForeignKey('contacts.user_id', ondelete='CASCADE'), nullable=False)
    type           = Column(String,  nullable=False)
    timestamp      = Column(DateTime, nullable=False)
    notes          = Column(Text)
    contact        = relationship("Contact", back_populates="interactions")

class Notification(Base):
    __tablename__ = 'notifications'
    notification_id   = Column(Integer, primary_key=True)
    contact_id        = Column(Integer, ForeignKey('contacts.user_id', ondelete='CASCADE'), nullable=False)
    timestamp         = Column(DateTime, nullable=False)
    notification_type = Column(String, nullable=False)
    message_id        = Column(String)
    send_status       = Column(String)
    ack_flag          = Column(Boolean)
    contact           = relationship("Contact", back_populates="notifications")

# create engine & session factory
engine = create_engine("postgresql://crm_user:crm_pass@localhost:5432/crm_db")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
