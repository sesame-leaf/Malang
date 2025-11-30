import pygame
import sys
import pandas as pd
import random
import os
import math

pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 350, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("말랑")

import itemShopManager

from features import font_large ,font_medium ,font_small ,font_tiny ,font_atomic
from features import Button


# ================
# 기본 경로 설정
# ================
# __file__이 없는 환경에서도 동작하도록 안전하게 처리
try:
    base_path = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_path = os.getcwd()
ASSET_PATHS = {
    "logo": os.path.join(base_path, "assets", "logo.png"),
    "guest_button": os.path.join(base_path, "assets", "btn_guest.png"),
    "account_button": os.path.join(base_path, "assets", "btn_account.png"),
    "back_button": os.path.join(base_path, "assets", "back_button.png"),
    "nav_books": os.path.join(base_path, "assets", "nav_books.png"),
    "nav_home": os.path.join(base_path, "assets", "nav_home.png"),
    "nav_social": os.path.join(base_path, "assets", "nav_social.png"),
    "exit_button": os.path.join(base_path, "assets", "btn_exit.png"),
    "login_menu_bg": os.path.join(base_path, "assets", "login_menu_bg.png"),
    "main_menu_bg": os.path.join(base_path, "assets", "main_menu_bg.png"),
    "room_bg": os.path.join(base_path, "assets", "room_bg.png"),
    "social_vs_bg": os.path.join(base_path, "assets", "social_vs_bg.png"),
    "my_room_bg": os.path.join(base_path, "assets", "my_room_bg.png"),
    "my_home_bg": os.path.join(base_path, "assets", "my_home_bg.png"),
    "ranking_bg": os.path.join(base_path, "assets", "ranking_bg.png"),
    "pick_a_word_bg": os.path.join(base_path, "assets", "pick_a_word_bg.png"),
    "select_the_meaning_bg": os.path.join(base_path, "assets", "select_the_meaning_bg.png"),
    "check_icon": os.path.join(base_path, "assets", "check_img.png"),
    "x_icon": os.path.join(base_path, "assets", "x_icon.png"),
    "next_question_btn": os.path.join(base_path,"assets","next_question_btn.png"),
    "char_default": os.path.join(base_path, "assets", "char_default.png"),
    "item_shirt": os.path.join(base_path, "assets", "item_shirt.png"),
    "item_pants": os.path.join(base_path, "assets", "item_pants.png"),
    "item_glasses": os.path.join(base_path, "assets", "item_glasses.png"),
    "item_hat": os.path.join(base_path, "assets", "item_hat.png"),
    "hamster_with_glasses": os.path.join(base_path, "assets", "hamster_with_glasses.png"),
    "hamster_with_glasses,sunflower": os.path.join(base_path, "assets", "hamster_with_glasses,sunflower.png"),
    "hamster_with_sunflower": os.path.join(base_path,"assets","hamster_with_sunflower.png"),
    "sunflower_price" : os.path.join(base_path, "assets", "sunflower_price.png"),
    "glasses_price" : os.path.join(base_path, "assets", "glasses_price.png"),
    "lay_off": os.path.join(base_path, "assets", "lay_off.png"),
    "put_on": os.path.join(base_path, "assets", "put_on.png"),
    "quiz_option": os.path.join(base_path, "assets", "quiz_option.png"),
    "toggle_on": os.path.join(base_path, "assets", "toggle_on.png"),
    "toggle_off": os.path.join(base_path, "assets", "toggle_off.png"),
    "theme_light": os.path.join(base_path, "assets", "theme_light.png"),
    "theme_dark": os.path.join(base_path, "assets", "theme_dark.png"),
}

# ================
# 화면 설정
# ================


# 색상 및 테마
RED, BLUE = (220, 80, 80), (100, 140, 250)
GREEN_LIGHT, RED_LIGHT = (144, 238, 144), (255, 182, 193)
GRAY = (180, 180, 180)
LIGHT_BLUE_GRAY = (200, 210, 230)
light_theme_colors = {'bg': (255, 255, 255), 'text': (0, 0, 0), 'ui_bg': (230, 230, 230), 'ui_accent': (200, 200, 200), 'bubble_bg': (255, 255, 255), 'border': (200, 200, 200)}
dark_theme_colors = {'bg': (40, 42, 54), 'text': (248, 248, 242), 'ui_bg': (68, 71, 90), 'ui_accent': (98, 114, 164), 'bubble_bg': (68, 71, 90), 'border': (150, 150, 150)}
current_theme, COLORS = "light", light_theme_colors

# 폰트 로딩 (assets 폴더 사용)
try:
    FONT_PATH = os.path.join(base_path, "assets", "onkim.ttf")
    font_large = pygame.font.Font(FONT_PATH, 36)
    font_medium = pygame.font.Font(FONT_PATH, 24)
    font_small = pygame.font.Font(FONT_PATH, 17)
    font_tiny = pygame.font.Font(FONT_PATH, 14)
    font_atomic = pygame.font.Font(FONT_PATH, 10)
except Exception:
    # 경고는 출력하지만 실행은 계속
    try:
        print(f"경고: 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")
    except Exception:
        pass
    font_large, font_medium, font_small, font_tiny = [pygame.font.SysFont(None, size) for size in [48, 32, 24, 18]]

# ======================
# 데이터(문제) 로드
# ======================
LEVEL_CHOICES = [1, 2, 3]
try:
    questions_path = os.path.join(base_path, "data", "vocabulary_spelling_questions.csv")
    df = pd.read_csv(questions_path, encoding='utf-8').astype(str).replace('nan', '')
    questions_by_level = {lvl: df[df['단계'] == str(lvl)].to_dict('records') for lvl in LEVEL_CHOICES}
    all_questions = []
    for lvl in LEVEL_CHOICES:
        all_questions.extend(questions_by_level[lvl])
except FileNotFoundError:
    print("오류: 'vocabulary_spelling_questions.csv' 파일을 찾을 수 없습니다.")
    questions_by_level = {lvl: [] for lvl in LEVEL_CHOICES}
    all_questions = []

available_levels = {lvl: len(questions_by_level.get(lvl, [])) > 0 for lvl in LEVEL_CHOICES}

def has_available_levels():
    return any(available_levels.values())

class WordMeaningManager:
    def __init__(self, filename):
        self.meanings = {}
        self._load(filename)

    def _load(self, filename):
        try:
            df = pd.read_csv(filename, encoding='utf-8-sig').astype(str).replace('nan', '')
            for _, row in df.iterrows():
                word = str(row.get('단어', '')).strip()
                meaning = str(row.get('뜻', '')).strip()
                if word:
                    self.meanings[word] = meaning
        except FileNotFoundError:
            print("오류: 'vocabulary_word_meaning.csv' 파일을 찾을 수 없습니다.")

    def get(self, word):
        if word is None:
            return ""
        return self.meanings.get(str(word).strip(), "")

word_meaning_manager = WordMeaningManager(os.path.join(base_path, "data", "vocabulary_word_meaning.csv"))

IM = itemShopManager.ItemManager()

DOTORI_FILE = "dotori_count.txt"
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

  # 전역 변수로 아이템 매니저 인스턴스 생성
# ================
# 헬퍼 함수
# ================
def get_text_lines(text, font, max_width):
    if not text:
        return []
    words, lines, current_line = text.split(' '), [], ""
    for word in words:
        if font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip()); current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_text_in_container(lines, font, color, surface, container_rect, align="left"):
    y_offset = 0
    if not color==0:
        pygame.draw.rect(surface, color,container_rect)
    try:
        if lines.isdigit() :
            line_surface = font.render(lines, True, (0,0,0))
            surface.blit(line_surface, line_surface.get_rect(center=container_rect.center))
    except:
        indent = 0
        for i,line in enumerate(lines):
            line_surface = font.render(line, True, (0,0,0))
            line_rect = line_surface.get_rect()
            if i == 0:
                indent = (container_rect.width - line_rect.width) / 2
            if align == "left":
                line_rect.topleft = (container_rect.x+indent, container_rect.y + y_offset)
            elif align == "center":
                line_rect.midtop = (container_rect.centerx, container_rect.y +y_offset)
                
            surface.blit(line_surface, line_rect)

            y_offset += font.get_height()


# ================
# 퀴즈 로직 상태 변수
# ================
current_level, current_question_index, score = 0, 0, 0
quiz_questions, answer_buttons = [], []
user_answer, correct_answer = None, None
answer_checked = False
current_quiz_mode, total_questions = None, 0
unlock_message = ""
clicked = False
selected_answer_button = None
selected_answer_correct = False
feedback_active = False
FEEDBACK_DURATION_MS = 1000
selected_answer_explanation = ""
unlocked_level = max([lvl for lvl, has in available_levels.items() if has], default=0)

def start_quiz(mode, level=None):
    global scene, current_quiz_mode, current_level, quiz_questions, total_questions, score, user_answer, answer_checked, current_question_index
    global selected_answer_button, selected_answer_correct, feedback_active, selected_answer_explanation
    scene, current_quiz_mode = "quiz_game", mode
    score, user_answer, answer_checked, current_question_index = 0, None, False, 0
    selected_answer_button = None
    selected_answer_correct = False
    feedback_active = False
    selected_answer_explanation = ""
    if mode == "practice" and level and questions_by_level.get(level):
        current_level, total_questions = level, min(15, len(questions_by_level[level]) or 15)
        quiz_questions = random.sample(questions_by_level[level] if questions_by_level[level] else [], total_questions) if questions_by_level[level] else []
    elif mode == "test":
        if level and questions_by_level.get(level):
            current_level = level
            pool = questions_by_level[level]
        else:
            current_level = None
            pool = all_questions
        count = len(pool) if pool else 0
        total_questions = min(20, count) if count else 0
        quiz_questions = random.sample(pool, total_questions) if count else []
    # 준비
    prepare_current_question()

def prepare_current_question():
    global answer_buttons, correct_answer,how_many_options, context_existence
    global selected_answer_button, selected_answer_correct, feedback_active, selected_answer_explanation
    
    pygame.time.set_timer(pygame.USEREVENT, 0)
    selected_answer_button = None
    selected_answer_correct = False
    feedback_active = False
    selected_answer_explanation = ""
    answer_buttons.clear()
    if not quiz_questions or current_question_index >= len(quiz_questions):
        return
    question = quiz_questions[current_question_index]
    how_many_options = question.get('선택지3')
    context_existence = question.get('보기')
    options = []
    context_text = None

    # 2지선다 예외 처리
    if question.get('보기') and question.get('선택지1') and not question.get('선택지2'):
        options = [question['보기'], question['선택지1']]
        correct_answer = question.get('정답', '')
    else:
        options = [question.get(f'선택지{i}', '') for i in [1,2,3,4] if question.get(f'선택지{i}', '')]
        if question.get('정답', '').isdigit():
            correct_idx = int(question['정답']) - 1
            correct_answer = options[correct_idx] if 0 <= correct_idx < len(options) else ""
        else:
            correct_answer = question.get('정답', '')
        context_text = question.get('보기', None)

    # UI 레이아웃 동적 계산
    side_margin = SCREEN_WIDTH * 0.075
    content_width = SCREEN_WIDTH - (side_margin * 2)
    current_y = 80
    # 문제 텍스트 높이 계산
    question_lines = get_text_lines(question.get('문제', ''), font_medium, content_width)
    q_height = len(question_lines) * font_medium.get_height()
    current_y += q_height + 20

    if context_text:
        context_lines = get_text_lines(context_text, font_small, content_width - 40)
        box_h = len(context_lines) * font_small.get_height() + 20
        current_y +=   50+box_h
    if how_many_options == '':
        current_y = 248
    else:
        current_y = 201
    button_height = 65
    button_gap = 10
    for option in options:
        button_rect = (side_margin, current_y, content_width, button_height)
        # 여기서 이미지 기반 버튼으로 생성 (퀴즈 선택지도 이미지로 대체 가능)
        btn = Button(button_rect, option, image_path=ASSET_PATHS.get("quiz_option"))
        answer_buttons.append(btn)
        current_y += button_height + button_gap

# ================
# 리소스(이미지) 로드 / 기본 대체
# ================
def safe_load_and_scale(path, target_size):
    try:
        if not path or not os.path.exists(path):
            return None
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, target_size)
    except Exception:
        return None

#배경이미지 (있으면 로드)
back_button_img = safe_load_and_scale(ASSET_PATHS.get("back_button"), (33, 33))
login_menu_bg = safe_load_and_scale(ASSET_PATHS.get("login_menu_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
main_menu_bg = safe_load_and_scale(ASSET_PATHS.get("main_menu_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
social_vs_bg = safe_load_and_scale(ASSET_PATHS.get("social_vs_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
pick_a_word_bg = safe_load_and_scale(ASSET_PATHS.get("pick_a_word_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
select_the_meaning_bg = safe_load_and_scale(ASSET_PATHS.get("select_the_meaning_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
my_room_bg = pygame.image.load(ASSET_PATHS.get("my_room_bg")).convert()
my_room_bg = pygame.transform.smoothscale(my_room_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
my_room_bg.set_colorkey((255,255,255), pygame.RLEACCEL)
my_home_bg = safe_load_and_scale(ASSET_PATHS.get("my_home_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
hamster_with_glasses = safe_load_and_scale(ASSET_PATHS.get("hamster_with_glasses"), (SCREEN_WIDTH, SCREEN_HEIGHT))
hamster_with_sunflower = safe_load_and_scale(ASSET_PATHS.get("hamster_with_sunflower"), (SCREEN_WIDTH, SCREEN_HEIGHT))
hamster_with_glasses_and_sunflower = safe_load_and_scale(ASSET_PATHS.get("hamster_with_glasses,sunflower"), (SCREEN_WIDTH, SCREEN_HEIGHT))
lay_off_img = safe_load_and_scale(ASSET_PATHS.get("lay_off"), (60, 15))
put_on_img = safe_load_and_scale(ASSET_PATHS.get("put_on"), (60,15))
sunflower_price_img = safe_load_and_scale(ASSET_PATHS.get("sunflower_price"), (100, 35))
flushing_price_img = safe_load_and_scale(ASSET_PATHS.get("sunflower_price"), (100, 35))
glasses_price_img = safe_load_and_scale(ASSET_PATHS.get("glasses_price"), (100, 35))
char_default_img = safe_load_and_scale(ASSET_PATHS.get("char_default"), (160, 200))
check_icon_img = safe_load_and_scale(ASSET_PATHS.get("check_icon"), (31, 31))
x_icon_img = safe_load_and_scale(ASSET_PATHS.get("x_icon"), (33, 27))
next_question_btn_img = safe_load_and_scale(ASSET_PATHS.get("next_question_btn"),(126,42))
AdornmentScrollSurface = IM.scrollSurface('Adornment')
bodyScrollSurface = IM.scrollSurface('body')
# ================
# 상태 및 버튼 정의 (이미지 경로 지정 가능)
# ================
scene, quiz_bubble_visible = "login", False
scroll_offset_x = 0

# 버튼들 (이미지 경로를 Button 생성자에 넣어두면 바꿀 수 있음)
guest_btn = Button((25, 335, 300, 67), image_path=ASSET_PATHS.get("guest_button"))
account_btn = Button((25, 425, 300, 67), image_path=ASSET_PATHS.get("account_button"))
setting_btn = Button((292, 17, 41, 41), image_path=None)
next_question_btn = Button(((88, 518, 178, 72)),image_path=None)
#items_middle_btn = Button((121, 550, 107, 150), image_path=None)
#items_right_btn = Button((238, 550, 107, 150), image_path=None)
scroll_btn = Button((0,550,300,150),image_path=None)
x_mar = 17
y_mar = 493
nav_btn_in_room = [
    Button((x_mar,y_mar,(SCREEN_WIDTH-2*x_mar)/3,40)),
    Button((x_mar+(SCREEN_WIDTH-2*x_mar)/3,y_mar,(SCREEN_WIDTH-2*x_mar)/3,40)),
    Button((x_mar+(SCREEN_WIDTH-2*x_mar)/3*2,y_mar,(SCREEN_WIDTH-2*x_mar)/3,40)),
]
nav_btn_in_home =[]
from_home_to_room = Button((75,238,200,200))

# 네비게이션 (여덟 개)
x_main = 25
x_gap = 62
nav_buttons = [
    Button((35, 508, 83, 37), image_path=ASSET_PATHS.get("nav_books")),
    Button((133, 508, 83, 37), image_path=ASSET_PATHS.get("nav_home")),
    Button((231, 508, 83, 37), image_path=ASSET_PATHS.get("nav_social")),
    Button((x_main, 640, 50, 50)),
    Button((x_main +x_gap, 640, 49, 49), image_path=ASSET_PATHS.get("nav_books")),
    Button((x_main +2*x_gap, 640, 49, 49), image_path=ASSET_PATHS.get("nav_social")),
    Button((x_main +3*x_gap, 640, 49, 49),image_path=ASSET_PATHS.get("ranking_bg")),
    Button((x_main +4*x_gap, 640, 49, 49), image_path=ASSET_PATHS.get("nav_home")),
]

# 퀴즈 드롭다운(버블) 관련
back_btn = Button((20, 19, 33, 33),image_path=None)
back_btn_settings = Button((20, 19, 33, 33),text='back',image_path=None)
back_btn_my_room = Button((18, 13, 33, 33),image_path=None)

level_buttons = [Button((75, 175 + i*100, 200, 60), f"{i+1}단계") for i in range(3)]
retry_btn, main_menu_btn = Button((40, 450, 130, 50), "다시하기"), Button((180, 450, 130, 50), "메인 메뉴")
exit_quiz_flow_btn = Button((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60, 80, 40), "나가기", image_path=ASSET_PATHS.get("exit_button"))

# 설정 토글 (이미지로 표시할 토글 경로 사용)
i = 90
bgm_btn = Button((210, 184, 100, 40),'on',(20,93,191),(255,255,255), image_path=ASSET_PATHS.get("toggle_on"))
sfx_btn = Button((210, 184+i, 100, 40),'on',(20,93,191),(255,255,255), image_path=ASSET_PATHS.get("toggle_on"))
theme_btn = Button((210, 184+2*i, 100, 40),"다크 모드 on",COLORS['ui_bg'], image_path=ASSET_PATHS.get("theme_light"))

# 꾸미기 아이템 목록(집 메뉴에 표시)
item_images = [
    ASSET_PATHS.get("item_shirt"),
    ASSET_PATHS.get("item_pants"),
    ASSET_PATHS.get("item_glasses"),
    ASSET_PATHS.get("item_hat"),
]
# ================
# 메인 루프
# ================
running = True
quiz_bubble_visible = False
is_dragging = False
has_moved = False
momentum_velocity_y = 0
FRICTION = 0.8
MOMENTUM_CUTOFF = 2
last_mouse_y = 0
scroll_offset_y =0
item_clicked_flag = False
category_in_room = 'Adornment'
category_surf_in_room = AdornmentScrollSurface
category_in_home = ''
updateHamster = IM.get_equipped_hamster_surface()
updateHamster_in_home = pygame.transform.smoothscale(updateHamster, (230, 230))


# 퀴즈 준비 (만약 start_quiz 호출 없이 들어갔을 때 오류 방지)
if quiz_questions:
    prepare_current_question()

while running:
    event_list = pygame.event.get()

    # 2. 저장된 이벤트들의 'type'만 뽑아서 리스트를 만듭니다.
    event_types = [e.type for e in event_list]

    # 3. 특정 타입(예: 마우스 클릭)이 '없는지' 확인합니다.
    if pygame.MOUSEMOTION not in event_types:
        is_dragging2 = False

    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

        # 마우스 휠로 집 화면 아이템 슬라이드 처리
        if scene == "my_room" and event.type == pygame.MOUSEWHEEL:
            # 한 슬롯 너비는 110 (같은 방식으로 하드코딩된 UI를 준수)
            max_scroll = max(0, len(item_images) * 110 - (SCREEN_WIDTH - 40))
            scroll_offset_x = max(min(0, scroll_offset_x + event.y * 30), -max_scroll)
        
        elif scene == "my_room" and event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and scroll_btn.is_clicked(event.pos):
            is_dragging = True
            last_mouse_y = event.pos[1]
            momentum_velocity_y = 0  # 기존 관성 속도 제거
            has_moved = False
        
        # --- 2) 마우스 드래그/움직임 ---
        if event.type == pygame.MOUSEMOTION:
            is_dragging2 = True
            if is_dragging:
                has_moved = True
                # 현재 프레임에서 마우스가 움직인 거리 (Delta) 계산
                delta_y = event.pos[1] - last_mouse_y
                
                # 스크롤 오프셋 즉시 이동 (화면을 따라 움직임)
                temp = scroll_offset_y
                scroll_offset_y -= delta_y
                if scroll_offset_y >= category_surf_in_room.get_height()-150 or scroll_offset_y <= 0:
                    scroll_offset_y =temp
                    delta_y =0
                
                # 다음 프레임을 위한 마지막 위치 업데이트
                last_mouse_y = event.pos[1]
                
                # ★ 관성 속도를 최근 움직인 속도로 갱신 ★
                # (delta_y를 그대로 사용하면 간단하게 구현 가능)
                momentum_velocity_y = delta_y 
        
        
                
        # --- 3) 마우스 버튼 떼기/터치 해제 (관성 시작) ---
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if scene == "my_room" and  momentum_velocity_y <= 0.1 and has_moved == False and clicked == False:
                
                if back_btn_my_room.is_clicked(pos):
                    scene = "main_menu"
                # 아이템 구매/착용 처리
                item_pos = (pos[0],pos[1]-539+scroll_offset_y)
                for item in IM.item_class_list:
                    if item.is_clicked(item_pos) and not IM.is_purchased(item) and clicked == False and item.broad_category == category_in_room:

                        IM.purchase_item(item)
                        updateHamster = IM.get_equipped_hamster_surface()
                        updateHamster_in_home = pygame.transform.smoothscale(updateHamster, (200, 200))
                    elif item.is_clicked(item_pos) and IM.is_purchased(item) and clicked == False and item.broad_category == category_in_room:
                        if IM.is_equipped(item) and category_in_room != 'body':
                            IM.unequip_item(item)
                        else:
                            IM.equip_item(item)
                        updateHamster = IM.get_equipped_hamster_surface()
                        updateHamster_in_home = pygame.transform.smoothscale(updateHamster, (200, 200))
            is_dragging = False
        
        if not is_dragging:
            # 1. 관성 속도만큼 스크롤 오프셋 이동
            scroll_offset_y -= momentum_velocity_y

            # 2. 마찰(Friction) 적용: 속도를 점진적으로 줄임
            momentum_velocity_y *= FRICTION 

            # 3. 속도가 너무 느려지면 멈춤 (0으로 고정)
            if abs(momentum_velocity_y) < MOMENTUM_CUTOFF:
                momentum_velocity_y = 0

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # 로그인 화면
            if scene == "login":
                if guest_btn.is_clicked(pos):
                    scene = "main_menu"
            elif scene == "main_menu":
                if nav_buttons[0].is_clicked(pos):
                    if has_available_levels():
                        scene = "practice_level_selection"
                    else:
                        start_quiz(mode="test", level=None)
                elif nav_buttons[1].is_clicked(pos):
                    scene = "my_room"
                    clicked = True
                elif nav_buttons[2].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[3].is_clicked(pos):
                    scene = "main_menu"
                elif nav_buttons[4].is_clicked(pos):
                    if has_available_levels():
                        scene = "practice_level_selection"
                    else:
                        start_quiz(mode="test", level=None)
                elif nav_buttons[5].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[6].is_clicked(pos):
                    scene = "ranking"
                elif nav_buttons[7].is_clicked(pos):
                    scene = "my_home"
                    clicked = True
                elif setting_btn.is_clicked(pos):
                    scene = "settings"
            # 공통 뒤로가기
            if scene in ["social_vs", "settings", "practice_level_selection", "practice_test_selection", "quiz_results", "ranking", "my_home"]:
                if back_btn.is_clicked(pos):
                    scene = "main_menu"
            elif scene == "my_room":
                if back_btn.is_clicked(pos):
                    scene = "my_home"
            # 연습 레벨 선택
            if scene == "practice_level_selection":
                for i, btn in enumerate(level_buttons):
                    level_value = i + 1
                    if not available_levels.get(level_value):
                        continue
                    if btn.is_clicked(pos):
                        start_quiz(mode="test", level=level_value)
                        break
                        
            # 퀴즈 진행 중
            elif scene == "quiz_game":
                if nav_buttons[3].is_clicked(pos):
                    scene = "main_menu"
                elif nav_buttons[4].is_clicked(pos):
                    if has_available_levels():
                        scene = "practice_level_selection"
                    else:
                        start_quiz(mode="test", level=None)
                elif nav_buttons[5].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[6].is_clicked(pos):
                    scene = "ranking"
                elif nav_buttons[7].is_clicked(pos):
                    scene = "my_room"
                
                if back_btn.is_clicked(pos):
                    scene = "main_menu"
                elif not answer_checked:
                    for btn in answer_buttons:
                        if btn.is_clicked(pos):
                            
                            user_answer = btn.text
                            answer_checked = True
                            selected_answer_button = btn
                            selected_answer_correct = (user_answer == correct_answer)
                            if selected_answer_correct:
                                score += 1
                                selected_answer_explanation = ""
                            else:
                                word_key = correct_answer
                                selected_answer_explanation = word_meaning_manager.get(word_key)
                            feedback_active = True
                            #pygame.time.set_timer(pygame.USEREVENT, FEEDBACK_DURATION_MS)
                            break
                if next_question_btn.is_clicked(pos) and scene == "quiz_game" and answer_checked and feedback_active:
                    current_question_index += 1
                    user_answer, answer_checked = None, False
                    feedback_active = False
                    selected_answer_button = None
                    selected_answer_correct = False
                    selected_answer_explanation = ""
                    if current_question_index < total_questions:
                        prepare_current_question()
                        
                    else:
                        scene = "quiz_results"
                    
            elif scene == "quiz_results":
                if retry_btn.is_clicked(pos):
                    start_quiz(mode=current_quiz_mode, level=current_level)
                    dotori_obtained = False  # 재시작 시 도토리 획득 여부 초기화
                elif main_menu_btn.is_clicked(pos):
                    scene = "main_menu"
                    dotori_obtained = False
            elif scene == "social_vs":
                if nav_buttons[3].is_clicked(pos):
                    scene = "main_menu"
                elif nav_buttons[4].is_clicked(pos):
                    if has_available_levels():
                        scene = "practice_level_selection"
                    else:
                        start_quiz(mode="test", level=None)
                elif nav_buttons[5].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[6].is_clicked(pos):
                    scene = "ranking"
                elif nav_buttons[7].is_clicked(pos):
                    scene = "my_room"
            elif scene == "my_room" :
                if nav_btn_in_room[0].is_clicked(pos) and not category_in_room == 'body':
                    category_in_room = 'body'
                    category_surf_in_room = bodyScrollSurface
                    scroll_offset_y = 0
                elif nav_btn_in_room[1].is_clicked(pos) and not category_in_room == 'Adornment':
                    category_in_room = 'Adornment'
                    category_surf_in_room = AdornmentScrollSurface
                    scroll_offset_y = 0
                elif nav_btn_in_room[2].is_clicked(pos) and not category_in_room == 'Adornment':
                    category_in_room = 'Adornment'
                    category_surf_in_room = AdornmentScrollSurface
                    scroll_offset_y = 0
            elif scene == "my_home":
                if from_home_to_room.is_clicked(pos):
                    scene = "my_room"
            # 설정 화면 테마 토글
            elif scene == "settings":
                '''if theme_btn.is_clicked(pos):
                    current_theme, COLORS = ("dark", dark_theme_colors) if current_theme == "light" else ("light", light_theme_colors)
                    # 테마 버튼 이미지 갱신(이미지 경로로 바꾸고 싶으면 ASSET_PATHS 수정)
                    theme_btn.image_path = ASSET_PATHS.get("theme_dark" if current_theme == "dark" else "theme_light")
                    theme_btn.reload_image()'''
            # 퀴즈/소셜 화면 등에서 '나가기' 버튼 (exit_quiz_flow_btn 사용)
            if scene in ["quiz_menu"]:
                # (이미 exit handlers 있지만 안전하게 처리)
                if exit_quiz_flow_btn.is_clicked(pos):
                    scene = "main_menu"
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = False

        # 퀴즈 자동 진행 타이머 이벤트
        if event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            if scene == "quiz_game" and answer_checked and feedback_active:
                current_question_index += 1
                user_answer, answer_checked = None, False
                feedback_active = False
                selected_answer_button = None
                selected_answer_correct = False
                selected_answer_explanation = ""
                if current_question_index < total_questions:
                    prepare_current_question()
                else:
                    scene = "quiz_results"

    # --- 화면 그리기 ---
    screen.fill(COLORS['bg'])

    if scene == "login":
        # (로고 + 버튼 - 이미지가 있으면 이미지로 표시)
        
        screen.blit(login_menu_bg, (0,0))
        guest_btn.transparent_draw(screen); account_btn.transparent_draw(screen)

    elif scene == "main_menu":
        # 배경 이미지 있으면 표시, 없으면 기본
        if main_menu_bg:
            screen.blit(main_menu_bg, (0,0))
        else:
            pygame.draw.rect(screen, COLORS['ui_bg'], (0,0, SCREEN_WIDTH, SCREEN_HEIGHT))
        # 네비 버튼
        for btn in nav_buttons:
            btn.transparent_draw(screen)
        setting_btn.transparent_draw(screen)

    elif scene == "my_room":
        back_btn_my_room.transparent_draw(screen)
        equipped =  IM.get_equipped_items()
        screen.blit(my_room_bg,(0,0))
        screen.blit(updateHamster,(175-updateHamster.get_width()/2,148))
        
        for i in nav_btn_in_room:
            i.transparent_draw(screen)
        '''if 'glasses' in equipped and 'sunflower' in equipped:
            screen.blit(hamster_with_glasses_and_sunflower,(0,0))
        elif 'glasses' in equipped:
            screen.blit(hamster_with_glasses,(0,0))
        elif 'sunflower' in equipped:
            screen.blit(hamster_with_sunflower,(0,0))
        else:
            screen.blit(my_room_bg,(0,0))'''
        
        screen.blit(category_surf_in_room,(0,537),area=(0,scroll_offset_y,350,170))
        
        '''for item in IM.item_data['item_name']:
            if not IM.is_purchased(item):
                if item == 'sunflower':
                    screen.blit(sunflower_price_img, (124, SCREEN_HEIGHT - 40))
                elif item == 'glasses':
                    screen.blit(glasses_price_img, (238, SCREEN_HEIGHT - 40))
            elif not IM.is_equipped(item):
                if item == 'sunflower':
                    screen.blit(put_on_img, put_on_img.get_rect(center=( SCREEN_WIDTH/2,SCREEN_HEIGHT - 27)))
                elif item == 'glasses':
                    screen.blit(put_on_img, put_on_img.get_rect(center=( SCREEN_WIDTH*(2/3)+put_on_img.get_width()/2+28,SCREEN_HEIGHT - 27)))
                    
            else:
                if item == 'sunflower':
                    screen.blit(lay_off_img, lay_off_img.get_rect(center=( SCREEN_WIDTH/2,SCREEN_HEIGHT - 27)))
                elif item == 'glasses':
                    screen.blit(lay_off_img, lay_off_img.get_rect(center=( SCREEN_WIDTH*(2/3)+lay_off_img.get_width()/2+28,SCREEN_HEIGHT - 27)))'''
        
        rect = pygame.Rect(280, 25, 40, 22)
        draw_text_in_container(f"{load_dotori_count()}", font_tiny, (255,255,255), screen, rect, align="center")
        '''items_middle_btn.transparent_draw(screen)
        items_right_btn.transparent_draw(screen)
        screen.blit(flushing_price_img, (8,SCREEN_HEIGHT-40))'''
    
    elif scene == "my_home":
        screen.blit(my_home_bg,(0,0))
        screen.blit(updateHamster_in_home,(175-updateHamster_in_home.get_width()/2,220))
        back_btn.transparent_draw(screen)
        from_home_to_room.transparent_draw(screen)
        rect = pygame.Rect(280, 25, 40, 22)
        draw_text_in_container(f"{load_dotori_count()}", font_tiny, (255,255,255), screen, rect, align="center")
        # (아이템을 클릭했을 때 동작하도록 하려면 여기에 is_clicked 검사 추가 가능)

    elif scene == "social_vs":
        screen.blit(social_vs_bg,(0,0))
        back_btn.transparent_draw(screen)
        for btn in nav_buttons[3:]:
            btn.transparent_draw(screen)
        # 오른쪽 하단 '나가기' 버튼 (이미지/대체)
        #exit_quiz_flow_btn.draw(screen)
    elif scene == "ranking":
        screen.blit(safe_load_and_scale(ASSET_PATHS.get("ranking_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        back_btn.transparent_draw(screen)

    elif scene == "settings":
        screen.blit(back_button_img, (20, 19)) if back_button_img else back_btn.transparent_draw(screen)
        title = font_large.render("설정", True, COLORS['text']); screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 80)))
        for i, label in enumerate(["배경음", "효과음", "테마 색상"]):
            screen.blit(font_medium.render(label, True, COLORS['text']), (40, 190 + i*90))
        # theme_btn 표시: 이미지가 있으면 이미지로
        bgm_btn.draw(screen); sfx_btn.draw(screen); theme_btn.draw(screen)

    elif scene == "practice_test_selection":
        back_btn.draw(screen)
        title = font_large.render("퀴즈 모드 선택", True, COLORS['text']); screen.blit(title, title.get_rect(center=(200, 80)))

    elif scene == "practice_level_selection":
        screen.blit(back_button_img, (20, 19)) if back_button_img else back_btn.transparent_draw(screen)
        title = font_large.render("레벨 선택", True, COLORS['text']); screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 90)))
        for i, btn in enumerate(level_buttons):
            level_value = i + 1
            if available_levels.get(level_value):
                btn.text, btn.base_color = f"{level_value}단계", (255, 200, 180)
                btn.text_color_override = None
            else:
                btn.text, btn.base_color = f"{level_value}단계 (없음)", GRAY
                btn.text_color_override = (140, 140, 140)
            btn.draw(screen)

    elif scene == "quiz_game":
        if quiz_questions and current_question_index < len(quiz_questions):
            if how_many_options == '' and context_existence == '':
                screen.blit(pick_a_word_bg, (0,0))
                pygame.draw.rect(screen, (255,246,246), (55,90, 240, 30))
                current_y = 130
            elif how_many_options == '':
                screen.blit(pick_a_word_bg, (0,0))
                current_y = 85
                context_y = 140
            else:
                screen.blit(select_the_meaning_bg, (0,0))
                current_y = 85
                context_y = 130
            for btn in nav_buttons[3:]:
                btn.transparent_draw(screen)
            back_btn.transparent_draw(screen)
            a = font_small.render(f"{current_question_index + 1} / {total_questions}", True, COLORS['text'])
            screen.blit(a,a.get_rect(center=(SCREEN_WIDTH/2,35)))
            question = quiz_questions[current_question_index]
            side_margin = SCREEN_WIDTH * 0.1
            content_width = SCREEN_WIDTH - (side_margin * 2)
            

            q_lines = get_text_lines(question.get('문제', ''), font_small, 240)
            q_rect = pygame.Rect(55, current_y, 240, len(q_lines) * font_small.get_height()+5)
            draw_text_in_container(q_lines, font_small, (255,244,244), screen, q_rect,align="left")
            current_y = q_rect.bottom 

            context_text = None
            if not (question.get('보기') and question.get('선택지1') and not question.get('선택지2')):
                context_text = question.get('보기')

            if context_text:
                context_lines = get_text_lines(context_text, font_tiny, content_width - 40)
                box_h = len(context_lines) * font_tiny.get_height() + 20
                box_rect = pygame.Rect(side_margin, context_y, content_width, box_h)
                draw_text_in_container(context_lines, font_tiny, 0, screen, box_rect.inflate(-20, -20), align="left")

            for btn in answer_buttons:
                original_color = btn.base_color
                if answer_checked:
                    if btn.text == correct_answer:
                        btn.base_color = GREEN_LIGHT
                    elif btn.text == user_answer:
                        btn.base_color = RED_LIGHT
                else:
                    btn.base_color = COLORS['ui_bg']
                btn.transparent_draw(screen)

                if answer_checked and btn is selected_answer_button:
                    if (not selected_answer_correct) and selected_answer_explanation:
                        text_lines = get_text_lines(selected_answer_explanation, font_tiny, btn.rect.width - 60)
                        max_text_width = max((font_tiny.size(line)[0] for line in text_lines), default=0)
                        box_width = max_text_width + 20
                        text_height = len(text_lines) * font_tiny.get_height()
                        overlay_rect = pygame.Rect(0, 0, box_width, text_height)
                        overlay_rect.center = btn.rect.center
                        icon_surface = x_icon_img
                        icon_gap = 6 if icon_surface else 0
                        if icon_surface:
                            # Shift the entire overlay right so icon+text are centered as a group.
                            overlay_rect.centerx += (icon_surface.get_width() + icon_gap) / 2
                        draw_text_in_container(
                            text_lines,
                            font_tiny,
                            (255, 255, 255),
                            screen,
                            overlay_rect,
                            align="center"
                        )
                        if icon_surface:
                            icon_rect = icon_surface.get_rect()
                            icon_rect.centery = btn.rect.centery
                            text_left = overlay_rect.centerx - max_text_width / 2
                            icon_rect.right = text_left - icon_gap
                            min_left = btn.rect.left + 6
                            if icon_rect.left < min_left:
                                icon_rect.left = min_left
                            screen.blit(icon_surface, icon_rect)
                    else:
                        icon_surface = check_icon_img if selected_answer_correct else x_icon_img
                        if icon_surface:
                            text_surface = font_tiny.render(btn.text, True, COLORS['text'])
                            text_rect = text_surface.get_rect(center=btn.rect.center)
                            icon_rect = icon_surface.get_rect()
                            icon_rect.centery = text_rect.centery
                            icon_rect.right = text_rect.left - 6
                            min_left = btn.rect.left + 6
                            if icon_rect.left < min_left:
                                icon_rect.left = min_left
                            screen.blit(icon_surface, icon_rect)
                        
                btn.base_color = original_color
            next_question_btn.transparent_draw(screen)
            if answer_checked == True:
                screen.blit(next_question_btn_img,(115,532))

        #exit_quiz_flow_btn.draw(screen)

    elif scene == "quiz_results":
        title_text = "연습 결과" if current_quiz_mode == "practice" else "테스트 결과"
        title = font_large.render(title_text, True, COLORS['text']); screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 100)))
        score_text = font_medium.render(f"총 {total_questions}문제 중 {score}개를 맞혔습니다!", True, COLORS['text']); screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH/2, 220)))
        pass_threshold = total_questions * 0.9 if total_questions else 9999
        if current_quiz_mode == "practice" and score >= pass_threshold and current_level < 3 and current_level + 1 > unlocked_level:
            unlocked_level = current_level + 1
            #save_level_progress(unlocked_level)
            unlock_message = "🎉 다음 레벨이 해금되었습니다! 🎉"
        elif current_quiz_mode == "test" and score >= pass_threshold and dotori_obtained == False:
            dotori_earned = random.randint(5, 15)
            total_dotori = load_dotori_count() + dotori_earned
            save_dotori_count(total_dotori)
            unlock_message = f"해바라기씨앗 {dotori_earned}개를 획득했습니다! 🎉 (총 해바라기씨앗: {total_dotori}개)"
        msg, color = ("🎉 통과했습니다! 🎉", BLUE) if score >= pass_threshold else ("다시 도전해보세요!", RED)
        result = font_large.render(msg, True, color); screen.blit(result, result.get_rect(center=(SCREEN_WIDTH/2, 300)))
        try:
            unlock_msg_render = font_tiny.render(unlock_message, True, GREEN_LIGHT)
            screen.blit(unlock_msg_render, unlock_msg_render.get_rect(center=(SCREEN_WIDTH/2, 350)))
        except:
            pass
        retry_btn.draw(screen); main_menu_btn.draw(screen)

    '''if quiz_bubble_visible:
        draw_quiz_bubble(screen)'''

    pygame.display.flip()

pygame.quit()
sys.exit()
