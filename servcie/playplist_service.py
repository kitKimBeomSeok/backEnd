from orm_models.table import Playlist,Music

#플레이리스트 생성
"""
자신이 선택한 음원들을 하나의 플레이리스로 만든다. 음악은 post 요청시 list의 형태로 id를 전달한다
"""
def create_playlist(session,title,user_id,selected_musics):
    # selected_musics에서 음악의 ID를 사용하여 해당 음악을 가져옴
    try :
        music_list = session.query(Music).filter(Music.id in(selected_musics)).all()
        Playlist.create_playlist(session,title,user_id,music_list)
    except Exception as e :
        print("오류 발생" ,e)
    finally:
        session.close()

#플레이리스트 삭제
"""
자신이 선택한 플레이리스트 삭제
"""

"""
플레이리스트 안의 음악 목록을 수정
"""
#플레이리스트 수정

