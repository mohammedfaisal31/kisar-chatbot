from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    user_honorific = Column(Enum("Dr", "Mr", "Mrs", "Ms"), nullable=False)
    user_first_name = Column(String(255), index=True)
    user_middle_name = Column(String(255), index=True)
    user_last_name = Column(String(100), index=True,server_default=" ")
    user_email = Column(String(255), nullable=False)
    user_phone = Column(String(10), unique=True, nullable=False)
    user_med_council_number = Column(String(255), nullable=False)  
    user_category = Column(Enum("Delegate", "Faculty"), nullable=False)
    user_type = Column(String(255), nullable=False)
    user_package_id = Column(Integer,nullable=True)
    user_city = Column(String(255), nullable=False)
    user_state_of_practice = Column(String(255), nullable=False)
    user_payment_id = Column(String(36),server_default="MOJO" ,nullable=False)
    user_payment_status = Column(Enum("SUCCESS", "FAILED","PENDING"), server_default="PENDING")
    user_registration_type = Column(String(10),server_default="DEFAULT" ,nullable=False)
    user_organisation=Column(String(255),server_default="INDIVIDUAL" ,nullable=False)

class Package(Base):
    __tablename__ = "packages"
    package_id = Column(Integer ,primary_key=True,index=True)
    package_title = Column(String(100) ,nullable=False) # Residential or Non-Residential
    package_price = Column(Integer ,nullable=False)
    package_occupancy = Column(Enum("Single", "Double"), nullable=False)
    package_duration = Column(Enum("One-day", "Two-day","Non-Residential"),server_default="Non-Residential", nullable=False)
    
class SessionManager(Base):
    __tablename__ = "sessions"
    id = Column(Integer ,primary_key=True,index=True)
    user_phone = Column(String(10) ,unique=True,index=True)
    session_number = Column(Integer,server_default="0")




    

    
