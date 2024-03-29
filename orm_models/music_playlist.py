from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class MusicPlaylist(Base):
    __tablename__ = 'music_playlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    playlist_id = Column(Integer, ForeignKey('playlist.id', ondelete='CASCADE'))
    music_id = Column(Integer, ForeignKey('music.id', ondelete='CASCADE'))

    @classmethod
    def create(cls, session, playlist_id, music_id):
        new_entry = cls(playlist_id=playlist_id, music_id=music_id)
        session.add(new_entry)
        session.commit()

    @classmethod
    def read(cls, session, music_playlist_id):
        return session.query(cls).filter_by(id=music_playlist_id).first()

    @classmethod
    def update(cls, session, music_playlist_id, new_playlist_id, new_music_id):
        entry = session.query(cls).filter_by(id=music_playlist_id).first()
        if entry:
            entry.playlist_id = new_playlist_id
            entry.music_id = new_music_id
            session.commit()

    @classmethod
    def delete(cls, session, music_playlist_id):
        entry = session.query(cls).filter_by(id=music_playlist_id).first()
        if entry:
            session.delete(entry)
            session.commit()
