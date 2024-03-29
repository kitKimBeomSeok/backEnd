from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    user_id = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'))
    status = Column(String(255))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="playlists")
    musics = relationship("Music", secondary="music_playlist")

    @classmethod
    def create_playlist(cls, session, title, user_id, music_list):
        new_playlist = cls(title=title, user_id=user_id)

        for music in music_list:
            new_playlist.musics.append(music)

        session.add(new_playlist)
        session.commit()

    @classmethod
    def read_playlist(cls, session, playlist_id):
        return session.query(cls).filter_by(id=playlist_id).first()

    @classmethod
    def update_playlist(cls, session, playlist_id, new_title, new_body):
        playlist = session.query(cls).filter_by(id=playlist_id).first()
        if playlist:
            playlist.title = new_title
            playlist.body = new_body
            session.commit()

    @classmethod
    def delete_playlist(cls, session, playlist_id):
        playlist = session.query(cls).filter_by(id=playlist_id).first()
        if playlist:
            session.delete(playlist)
            session.commit()
