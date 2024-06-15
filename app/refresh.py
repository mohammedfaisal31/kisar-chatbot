from db import get_db
from models import *
db = get_db()

def delete_users_by_phone_numbers(phone_numbers):

    try:
        # Query users with the specified phone numbers
        users_to_delete = db.query(User).filter(User.user_phone.in_(phone_numbers)).all()
        sessions_to_delete = db.query(SessionManager).filter(SessionManager.user_phone.in_(phone_numbers)).all()

        # Delete the users
        for user in users_to_delete:
            db.delete(user)
        for session in sessions_to_delete:
            db.delete(session)

        # Commit the transaction
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    phone_numbers = [
        '9986168689', '7397308801', '6300441922', '7981772562', '8667237371',
        '9663962950', '9000678946', '8310628938', '7972999478', '9481086566',
        '8304884972', '9894055296', '9742833931', '7299099208', '8971637572',
        '9481747555', '9731591666', '8811090582', '9353676794', '9901731619',
        '9847933332', '8791857653', '9562778890'
    ]
    
    delete_users_by_phone_numbers(phone_numbers)
