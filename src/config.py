import pygame
import pandas as pd
import os


pygame.font.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 350, 700


# ================
# 기본 경로 설정
# ================
# __file__이 없는 환경에서도 동작하도록 안전하게 처리
try:
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    FONT_PATH = os.path.join(base_path, "assets", "NanumBarunGothic.ttf")
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
