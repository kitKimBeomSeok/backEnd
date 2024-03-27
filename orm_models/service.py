from sqlite3 import IntegrityError

from sqlalchemy import create_engine
from orm_models.table import Music, User, Playlist, MusicPlaylist
from sqlalchemy.orm import sessionmaker
from midiutil import MIDIFile
#음원 조회
import io
from pydub import AudioSegment

# 데이터베이스 연결 엔진 생성
engine = create_engine('mysql+pymysql://root:102302@127.0.0.1/music', echo=True)
# Session 클래스 생성
Session = sessionmaker(bind=engine)
# Session 인스턴스 생성
DB_session = Session()
#음원 재생

#음원 등록



