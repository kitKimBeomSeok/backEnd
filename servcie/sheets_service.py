from orm_models.table import Music,Sheet
import os.path
import subprocess
import logging
"""악보 생성"""
def create_sheet(session, music_id):
    midi_folder = "./midi/"
    sheet_folder = "./sheets/"
    MuseScore4_exe_path = "C:/Program Files/MuseScore 4/bin/MuseScore4.exe"

    file_list = os.listdir(midi_folder)
    for file in file_list:
        print(file)
        midi_to_sheet(f"./midi/{file}", sheet_folder, MuseScore4_exe_path)


    # 파일을 데이터베이스로 이동
    sheet_list = os.listdir(sheet_folder) #악보 리스트
    try:
        for sheet in sheet_list:
            print(f"{sheet_folder}{sheet}")
            Sheet.create_sheet(session, music_id,sheet,f"{sheet_folder}{sheet}")
    except Exception as e:
        # IntegrityError가 발생하면 이미 존재하는 사용자이므로 롤백
        session.rollback()
        print("에러 발생", e)
    finally:
        # Session 종료
        session.close()

    #변환한 이미지를 삭제합니다.
    for file in sheet_list:
        os.remove(f"{sheet_folder}{file}")

"""선택한 음원 악보 조회 list 형태로 반환"""
def select_sheet(music_id):
    print()

"""악보 삭제 : 악보 이미지 리스트 삭제"""
def delete_sheet(sheets):
    print()



logging.basicConfig(filename='midi_to_sheet.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def logging_midi_to_sheet(midi_path, output_path, MuseScore3_exe_path):
    """ midi_to_sheet 함수를 위한 로깅 함수"""

    if not os.path.exists(midi_path):
        print("입력 파일의 위치를 다시 확인해주세요.")
        logging.error("MIDI 파일 경로가 잘못되었습니다: " + midi_path)
        return

    if not os.path.exists("C:/Program Files/MuseScore 4/bin/MuseScore4.exe"):
        print("MuseScore 실행 파일이 존재하지 않습니다: " + MuseScore3_exe_path)
        logging.error(f"MuseScore3.exe가 {MuseScore3_exe_path}에 존재하지 않음.")

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        print("출력 폴더가 존재하지 않습니다. 새로 생성하겠습니다.")
        logging.info("출력 폴더가 존재하지 않습니다. 새로 생성합니다: " + output_dir)
        os.makedirs(output_dir)


def midi_to_sheet(midi_path, output_path,
                  MuseScore3_exe_path):
    """ 미디 경로와 출력폴더를 인자로 받아 midi를 악보로 바꿔주는 함수 """

    # 로깅
    logging_midi_to_sheet(midi_path, output_path, MuseScore3_exe_path)

    # MuseScore에 내릴 명령어를 준비
    file_path, file_extension = os.path.splitext(midi_path)
    file_name = os.path.basename(file_path)
    output_filename_extension = ".png"
    output_name = f"{output_path}/{file_name}{output_filename_extension}"
    command = f'"{MuseScore3_exe_path}" -o "{output_name}" "{midi_path}"'

    # MuseScore로 midi를 악보화
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"MuseScore에 명령을 내리지 못했습니다 {e}")
    except Exception as e:
        logging.error(f"알 수 없는 에러: {e}")

    print("악보 생성 완료")




