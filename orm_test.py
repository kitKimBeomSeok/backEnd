from sqlalchemy import create_engine
from sqlite3 import IntegrityError

from servcie import music_service,sheets_service,playplist_service,musicPlaylist_service,user_service
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 엔진 생성
engine = create_engine('mysql+pymysql://root:102302@127.0.0.1/music', echo=True)
# Session 클래스 생성
Session = sessionmaker(bind=engine)
# Session 인스턴스 생성
DB_session = Session()
music_list = [4,5,6,7]
playplist_service.load_playlist(DB_session,4)