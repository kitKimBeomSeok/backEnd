# orm_models/models.py mysql+pymysql://root:102302@127.0.0.1/music
from datetime import datetime
from sqlite3 import IntegrityError

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# 데이터베이스 연결 설정
engine = create_engine('mysql+pymysql://root:102302@127.0.0.1/music', echo=True)  # 데이터베이스 파일명은 'music.db'입니다.
Base = declarative_base()

# User 모델 정의
class User(Base):
    __tablename__ = 'user'

    id = Column(String(255), primary_key=True)
    username = Column(String(255))

    playlists = relationship("Playlist", back_populates="user", )
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

# Music 모델 정의
class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
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
        def read_file_as_string(cls, file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
                return file_content

        audio_content = read_file_as_string(wav_file_path)
        midi_content = read_file_as_string(midi_file_path)



        new_music = cls(music_name=music_name, music_link=music_link, audio=audio_content, midi=midi_content, user_id=user_id)
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
class Sheet(Base):
    __tablename__ = 'sheets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    music_id = Column(Integer, ForeignKey('music.id', ondelete='CASCADE'))
    sheet_img = Column(String)

    # music 테이블과의 관계 설정
    music = relationship('Music', back_populates='sheets')
# Playlist 모델 정의
class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    body = Column(Text)
    user_id = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'))
    status = Column(String(255))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="playlists")
    musics = relationship("Music", secondary="music_playlist")

    @classmethod
    def create_playlist(cls, session, title, body, user_id):
        new_playlist = cls(title=title, body=body, user_id=user_id)
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


# MusicPlaylist 연결 테이블 모델 정의
class MusicPlaylist(Base):
    __tablename__ = 'music_playlist'

    id = Column(Integer, primary_key=True)
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

# 테이블 생성
Base.metadata.create_all(engine)

