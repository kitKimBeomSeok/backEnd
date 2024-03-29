from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, autoincrement=True)
    music_name = Column(String(255))
    music_link = Column(String(255))
    audio = Column(String)  # Blob 대신 String 형식으로 변경
    midi = Column(String)  # Blob 대신 String 형식으로 변경
    created_at = Column(TIMESTAMP, default=datetime.now())  # 현재 시각을 기본값으로 설정
    user_id = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'))

    user = relationship("User", back_populates="musics")
    sheets = relationship("Sheet", back_populates="music")

    @classmethod
    def create_music(cls, session, music_name, music_link, wav_file_path, midi_file_path, user_id):

        audio_content = Base.read_file_as_string(wav_file_path)
        midi_content = Base.read_file_as_string(midi_file_path)

        new_music = cls(music_name=music_name, music_link=music_link, audio=audio_content, midi=midi_content,
                        user_id=user_id)
        session.add(new_music)
        session.commit()

    @classmethod
    def read_music(cls, session, music_id):
        return session.query(cls).filter_by(id=music_id).first()

    @classmethod
    def update_music(cls, session, music_id, new_music_name, new_music_link):
        music = session.query(cls).filter_by(id=music_id).first()
        if music:
            music.music_name = new_music_name
            music.music_link = new_music_link
            session.commit()

    @classmethod
    def delete_music(cls, session, music_id):
        music = session.query(cls).filter_by(id=music_id).first()
        if music:
            session.delete(music)
            session.commit()
