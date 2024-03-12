from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from models import User,SessionManager
from sqlalchemy.exc import IntegrityError


def get_user_session_number(user_phone, db):
    try:
        user = db.query(User).filter_by(user_phone=user_phone).one()
        return user.user_session_number
    except NoResultFound:
        return None
    finally:
        db.close()

def check_if_user_exists(user_phone, db):
    try:
        user = db.query(User).filter_by(user_phone=user_phone).one()
        return user
    except NoResultFound:
        return None
    finally:
        db.close()


def update_user_package_id(user_phone, new_package_id, db):
    try:
        user = db.query(User).filter_by(user_phone=user_phone).one()
        user.user_package_id = new_package_id
        db.commit()
        return True
    except NoResultFound:
        return False
    finally:
        db.close()

def create_user(user_honorific, user_first_name, user_middle_name, user_last_name, user_email, user_phone, user_category,  user_package_id, user_med_council_number ,user_city,user_state_of_practice, user_type,db):
    try:
        new_user = User(user_honorific=user_honorific,
                        user_first_name=user_first_name,
                        user_middle_name=user_middle_name,
                        user_last_name=user_last_name,
                        user_email=user_email,
                        user_phone=user_phone,
                        user_category=user_category,
                        user_package_id=user_package_id,
                        user_med_council_number=user_med_council_number,
                        user_city=user_city,
                        user_state_of_practice=user_state_of_practice,
                        user_type=user_type
                        )
        db.add(new_user)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False  
    finally:
        db.close()

def createUserSession(phone,db):
    try:
        new_session = SessionManager(user_phone=phone)
        db.add(new_session)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False 
    finally:
        db.close()

def updateUserSession(phone,session_number,db):
    try:
        session = db.query(SessionManager).filter_by(user_phone=phone).one()
        session.session_number = session_number
        db.commit()
        return True
    except NoResultFound:
        return False 
    finally:
        db.close()

def checkUserSessionNumber(phone,db):
    try:
        result = db.query(SessionManager).filter_by(user_phone=phone).one()
        print(result.session_number)
        return result.session_number
    except NoResultFound:
        return None
    finally:
        db.close()

def updateUserPaymentDetails(phone,payment_id,payment_status,db):
    try:
        user = db.query(User).filter_by(user_phone=phone).one()
        user.user_payment_id = payment_id
        user.user_payment_status = payment_status
        db.commit()
        return True
    except NoResultFound:
        return False
    finally:
        db.close()

