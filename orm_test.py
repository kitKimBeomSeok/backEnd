from sqlalchemy import create_engine
from sqlite3 import IntegrityError

import orm_models.table
from orm_models import table
from orm_models.table import Music, User, Playlist, MusicPlaylist
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 엔진 생성
engine = create_engine('mysql+pymysql://root:102302@127.0.0.1/music', echo=True)
# Session 클래스 생성
Session = sessionmaker(bind=engine)
# Session 인스턴스 생성
DB_session = Session()


music = orm_models.table.Music
file_path = "/audio/y"
music.create_music(DB_session,"utttane","asd","audio/y2mate.com - Leinaうたたね  utataneMV.mp3","audio/y2mate.com - Leinaうたたね  utataneMV.dpipqxiy.composer1.mid","1")
