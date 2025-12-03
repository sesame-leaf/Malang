import pygame
import os

#pygame.font.init()
base_path = os.path.dirname(os.path.abspath(__file__))

COLORS = {'bg': (255, 255, 255), 'text': (0, 0, 0), 'ui_bg': (230, 230, 230), 'ui_accent': (200, 200, 200), 'bubble_bg': (255, 255, 255), 'border': (200, 200, 200)}

class Button:
    def __init__(self, rect, text=None, color=None, text_color=None, image_path=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.base_color = color
        self.text_color_override = text_color
        self.image_path = image_path
        self._image = None
        if image_path:
            self._image = self._load_and_scale(image_path)

    def _load_and_scale(self, path):
        try:
            if not os.path.exists(path):
                return None
            img = pygame.image.load(path).convert_alpha()
            w, h = self.rect.width, self.rect.height
            iw, ih = img.get_width(), img.get_height()
            # 비율 유지하여 맞추기
            if ih/iw >= h/w:
                # 이미지가 세로로 긴 경우: 높이에 맞추고 너비는 비율대로
                target_h = h
                target_w = max(1, int(iw / ih * target_h))
            else:
                target_w = w
                target_h = max(1, int(ih / iw * target_w))
            scaled = pygame.transform.smoothscale(img, (target_w, target_h))
            return scaled
        except Exception:
            return None

    def reload_image(self):
        if self.image_path:
            self._image = self._load_and_scale(self.image_path)

    def draw(self, surface):
        # 배경 사각형 (이미지 없을 때의 대체)
        color = self.base_color if self.base_color else COLORS['ui_accent']
        text_color = self.text_color_override if self.text_color_override else COLORS['text']
        if self._image:
            # 이미지가 버튼보다 작다면 가운데 정렬
            img = self._image
            img_rect = img.get_rect(center=self.rect.center)
            surface.blit(img, img_rect)
            # 이미지 위 텍스트 (필요 시)
            if self.text:
                txt = font_tiny.render(self.text, True, text_color)
                surface.blit(txt, txt.get_rect(center=self.rect.center))
        else:
            # 기본 렌더
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            if self.text:
                padding = 8
                target_rect = self.rect.inflate(-padding, -padding)
                current_font = font_small
                text_surface = current_font.render(self.text, True, text_color)
                if text_surface.get_width() > target_rect.width:
                    current_font = font_tiny
                    text_surface = current_font.render(self.text, True, text_color)
                surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def transparent_draw(self, surface, border_radius=-1):
        #디버그용 버튼 경계 표시
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, width=1, border_radius=border_radius)

        color = self.base_color if self.base_color else COLORS['ui_accent']
        text_color = self.text_color_override if self.text_color_override else COLORS['text']
        if self.text:
            txt = font_tiny.render(self.text, True, text_color)
            surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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

'''def create_question_display():
    os.path.join()
    return'''