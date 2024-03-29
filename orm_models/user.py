from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(String(255), primary_key=True)
    username = Column(String(255))

    playlists = relationship("Playlist", back_populates="user")
    musics = relationship("Music", back_populates="user")

    @classmethod
    def create_user(cls, session, user_id, username):
        new_user = cls(id=user_id, username=username)
        session.add(new_user)
        session.commit()

    @classmethod
    def read_user(cls, session, user_id):
        return session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def update_user(cls, session, user_id, new_username):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            user.username = new_username
            session.commit()

    @classmethod
    def delete_user(cls, session, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
