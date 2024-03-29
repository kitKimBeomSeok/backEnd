from orm_models.music_playlist import MusicPlaylist
from orm_models.playlist import Playlist
from orm_models.music import Music

#플레이리스트 생성
"""
자신이 선택한 음원들을 하나의 플레이리스로 만든다. 음악은 post 요청시 list의 형태로 id를 전달한다
"""
def create_playlist(session,title,user_id,selected_musics):
    # selected_musics에서 음악의 ID를 사용하여 해당 음악을 가져옴
    print(selected_musics)
    try :
        music_list = session.query(Music).filter(Music.id.in_(selected_musics)).all()
        print(music_list)
        Playlist.create_playlist(session,title,user_id,music_list)
    except Exception as e :
        print("오류 발생" ,e)
    finally:
        session.close()

#플레이리스트 조회 - 플레이리스트
"""자신이 생성한 플레이리스트를 조회한다."""

#플레이리스트 조회 - 음원
"""선택한 플레이리스트의 음원 정보를 가져온다."""
def load_playlist(session, playlist_id):
    try:
        # MusicPlaylist를 사용하여 해당 playlist_id에 속한 음악의 id를 가져옵니다.
        music_ids = session.query(MusicPlaylist.music_id).filter_by(playlist_id=playlist_id).all()
        print(music_ids)
        # 가져온 음악 id를 사용하여 실제 Music 테이블에서 음악 정보를 가져옵니다.
        music_list = session.query(Music).filter(Music.id.in_([music_id for music_id, in music_ids])).all()
        for music in music_list:
            print(music.id)

        return music_list

    except Exception as e:
        print("Error occurred:", e)
        return None
#플레이리스트 삭제
"""
자신이 선택한 플레이리스트 삭제
"""

"""
플레이리스트 안의 음악 목록을 수정
"""
#플레이리스트 수정

