import os

from src.config import *


DOTORI_FILE = os.path.join(base_path, "dotori_count.txt")
dotori_obtained = False  # 도토리 획득 여부 전역 변수로 추가
 # 초기화

def save_dotori_count(count=0):
    global dotori_obtained
    dotori_obtained = True  # 도토리 획득 여부 (필요 시 로직 추가)
    with open(DOTORI_FILE, 'w') as f:
        f.write(str(count))
if not os.path.exists(DOTORI_FILE):
    save_dotori_count()  # 초기 도토리 수 설정
def use_dotori(count):
    global dotori_obtained
    current_count = load_dotori_count()
    if count > current_count:
        print("오류: 사용하려는 도토리 수가 보유 도토리 수보다 많습니다.")
        return False
    dotori_obtained = True  # 도토리 사용 여부 (필요 시 로직 추가)
    new_count = current_count - count
    with open(DOTORI_FILE, 'w') as f:
        f.write(str(new_count))
    return True

def load_dotori_count():
    try:
        with open(DOTORI_FILE, 'r') as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0
