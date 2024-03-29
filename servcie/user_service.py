from sqlite3 import IntegrityError
from orm_models.user import User

def create_user(session,user_id, user_name):
    # 새로운 사용자 추가
    try:
        # 해당 ID가 이미 데이터베이스에 존재하는지 확인
        existing_user = session.query(User).filter_by(id=user_id).first()
        if existing_user is None:
            print("새로운 사용자가 추가되었습니다.")
            User.create_user(session, user_id, user_name)
        else:
            print("이미 존재하는 사용자입니다. 추가하지 않습니다.")
    except IntegrityError:
        # IntegrityError가 발생하면 이미 존재하는 사용자이므로 롤백
        session.rollback()
        print("이미 존재하는 사용자입니다. 추가하지 않습니다.")
    finally:
        # Session 종료
        session.close()


def delete_user(session, user_id):
    # 회원 탈퇴
    try:
        # 해당 ID가 이미 데이터베이스에 존재하는지 확인
        existing_user = session.query(User).filter_by(id=user_id).first()
        if existing_user is None:
            print("존재하지 않습니다.")
        else:
            print("회원탈퇴를 진행합니다")
            User.delete_user(session, user_id)
    except Exception as e:
        # 다른 예외가 발생한 경우에도 롤백하고 메시지 출력
        session.rollback()
        print("오류가 발생했습니다:", e)
    finally:
        # Session 종료
        session.close()
    return None