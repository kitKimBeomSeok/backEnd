import io


from MIDI import MIDIFile
from audiosegment import AudioSegment

from orm_models.music import Music

#TODO  수정해야함 추후 모델 개발후 변경
def insert_music(session, music_name, music_link, wav_file_path, midi_file_path,user_id):
    Music.create_music(session,"utttane","asd","audio/y2mate.com - Leinaうたたね  utataneMV.mp3","audio/y2mate.com - Leinaうたたね  utataneMV.midi","1")

def mp3_to_wav(mp3_data, output_file):
    # MP3 데이터를 BytesIO 객체로 읽어옴
    mp3_stream = io.BytesIO(mp3_data)
    audio_segment = AudioSegment.from_mp3(mp3_stream)
    wav_stream = io.BytesIO()
    audio_segment.export(wav_stream, format="wav")

    with open(output_file, 'wb') as f:
        f.write(wav_stream.getvalue())

def play_music_from_db(session, music_id, sampling_rate):
    # Blob 데이터를 직접 읽어와서 처리
    music = session.query(Music).filter_by(id=music_id).first()

    # music.audio에는 MP3 데이터가 들어있다고 가정합니다.
    mp3_data = music.midi
    wav_data = blob_to_midi(mp3_data,"output.mid")

def blob_to_midi(blob_data, output_file):
    # Blob 데이터를 BytesIO 객체로 읽어옴
    blob_stream = io.BytesIO(blob_data)

    # MIDI 파일 생성
    midi = MIDIFile(numTracks=1)

    # 트랙 0에 MIDI 이벤트 추가
    track = 0
    time = 0
    channel = 0

    # MIDI 데이터를 추가하는 예시
    # 여기서는 간단히 60개의 MIDI 이벤트를 추가합니다.
    for i in range(60):
        midi.addNote(track, channel, i, time + i, 1, 100)  # 채널 0에서 음표 추가

    # MIDI 파일 저장
    with open(output_file, "wb") as f:
        midi.writeFile(f)
# 사용 예시
music_id = 8  # 재생할 음악의 ID
sampling_rate = 22050  # 샘플링 속도

#play_music_from_db(session, music_id, sampling_rate)