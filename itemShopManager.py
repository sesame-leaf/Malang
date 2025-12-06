import pandas as pd
import os
import pygame
import features
from features import base_path
from ast import literal_eval
import math

def safe_load_and_scale(path, target_size ):
    try:
        if not path or not os.path.exists(path):
            return None
        
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img,target_size)
        
    except Exception as e:  # <-- 에러를 잡아서 변수 'e'에 저장!
        print("--- 이미지 로드 실패 상세 디버깅 ---")
        print(f"시도한 경로: {path}")
        print(f"파이게임이 뱉은 실제 오류: {e}") # <--- 이 메시지가 범인이야!
        print("---------------------------------")
        return None

lay_off_img = safe_load_and_scale(os.path.join(base_path,'assets',"lay_off.png"), (52, 13))
put_on_img = safe_load_and_scale(os.path.join(base_path,'assets',"put_on.png"), (52,13))
using_img = safe_load_and_scale(os.path.join(base_path,'assets',"using.png"), (39, 13))
change_img = safe_load_and_scale(os.path.join(base_path,'assets',"change.png"), (52, 13))
cozy_yellow_square = pygame.Surface((103, 103), pygame.SRCALPHA)

# 2. 더 밝은 노란색 설정 (레몬색에 가까움)
# (255, 255, 180): 아주 밝고 환한 노란색
# (255, 245, 100): 쨍하고 선명한 노란색
bright_yellow = (200, 200, 200) 

# 3. 둥근 사각형 그리기
# border_radius=20: 이 숫자가 클수록 더 둥글둥글해집니다 (최대 51까지 가능)
pygame.draw.rect(cozy_yellow_square, bright_yellow, cozy_yellow_square.get_rect(), border_radius=10)


class Item:
    dotoriImg = safe_load_and_scale(os.path.join(base_path,'assets',"dotoriImg.png"),(22,22))
    dotoriImg.set_colorkey((255,255,255))
    dotoriImgWidth = dotoriImg.get_width()

    def __init__(self, name, broad_category,category,purchased=False,equipped=False, price=0, itemIcon_path="",realItem_path='',target_pos='',target_size=''):
        self.name = name
        self.broad_category = broad_category
        self.category = category
        self.purchased = purchased
        self.equipped = equipped
        self.price = price
        self.itemIcon = safe_load_and_scale(os.path.join(base_path,'assets',itemIcon_path), (103, 103))
        if broad_category in ['furniture']:
            new = cozy_yellow_square.copy()
            new.blit(self.itemIcon,(0,0))
            self.itemIcon = new
        elif broad_category in ['flooring','wallpaper']:
            smooth_surface = pygame.transform.smoothscale(self.itemIcon, (70, 70))
            new = cozy_yellow_square.copy()
            # 1. 작은 서피스(붙일 것)의 사각형 정보를 가져옵니다.
            rect = smooth_surface.get_rect()

            # 2. 그 사각형의 중심(center)을 배경 서피스 사각형의 중심에 맞춥니다.
            rect.center = new.get_rect().center

            # 3. 그 위치(rect)에 그립니다.
            new.blit(smooth_surface, rect)
            self.itemIcon = new
        self.realItemImage = safe_load_and_scale(os.path.join(base_path,'assets',realItem_path), target_size)
        #self.realItemImage.set_colorkey((255,255,255),pygame.RLEACCEL)
        self.target_pos = target_pos
        self.rect = None
        self.superScreen = None
    
    def make_button(self,superScreen,x,y):
        self.superScreen = superScreen
        superScreen.blit(self.itemIcon,(x,y))
        width = self.itemIcon.get_width()
        self.rect = pygame.Rect(x,y,width,width+Item.dotoriImgWidth*1.2)
        if self.purchased == False:
            price = features.font_small.render(str(self.price),True,(0,0,0))
            price.set_colorkey((255,255,255))
            priceSurface= pygame.Surface((Item.dotoriImg.get_width()+price.get_width()+5,Item.dotoriImgWidth),pygame.SRCALPHA)
            priceSurface.blit(Item.dotoriImg,(0,0))
            priceSurface.blit(price,(Item.dotoriImg.get_width()+5,(priceSurface.get_height()-price.get_height())/2))
            middle = priceSurface.get_rect()
            middle.center = (x+width/9*4,y+width+Item.dotoriImgWidth/11*7)
            superScreen.blit(priceSurface, middle)
        elif self.equipped == False:
            self.is_purchased()
        else:
            self.is_equipped()
        #디버그용 버튼 테두리 표시
        #pygame.draw.rect(self.superScreen, (111,111,111),self.rect, width=1)
        
        
        

    def is_clicked(self,pos):
        return self.rect.collidepoint(pos)
    
    def is_purchased(self):
        
        wh = pygame.Surface((self.itemIcon.get_width(),Item.dotoriImgWidth))
        wh.fill((255,255,255))
        self.superScreen.blit(wh,(self.rect.x,self.rect.y+self.itemIcon.get_height()))
        if self.broad_category not in ['wallpaper','body','flooring']:
            self.superScreen.blit(put_on_img,(self.rect.x+(self.itemIcon.get_width()-put_on_img.get_width())/2,self.rect.y+self.itemIcon.get_height()+(self.dotoriImg.get_height()-put_on_img.get_height())/2+2))
        else:
            self.superScreen.blit(change_img,(self.rect.x+(self.itemIcon.get_width()-change_img.get_width())/2,self.rect.y+self.itemIcon.get_height()+(self.dotoriImg.get_height()-change_img.get_height())/2+2))
    
    def is_equipped(self):
        
        wh = pygame.Surface((self.itemIcon.get_width(),Item.dotoriImgWidth))
        wh.fill((255,255,255))
        self.superScreen.blit(wh,(self.rect.x,self.rect.y+self.itemIcon.get_height()))
        if self.broad_category not in ['wallpaper','body','flooring']:
            self.superScreen.blit(lay_off_img,(self.rect.x+(self.itemIcon.get_width()-lay_off_img.get_width())/2,self.rect.y+self.itemIcon.get_height()+(self.dotoriImg.get_height()-lay_off_img.get_height())/2+2))
        else:
            self.superScreen.blit(using_img,(self.rect.x+(self.itemIcon.get_width()-using_img.get_width())/2,self.rect.y+self.itemIcon.get_height()+(self.dotoriImg.get_height()-using_img.get_height())/2+2))



class ItemManager:
    def __init__(self, filename="data/player_items.csv"):
        """
        아이템 관리자를 초기화합니다.
        - filename: 아이템 소유 및 착용 정보를 저장할 CSV 파일 이름
        """
        self.filename = filename
        self.item_data = []

        self.item_class_list = []
        self.hamster_surface = None

        self._load_items()
        self.item_data['target_pos'] = self.item_data['target_pos'].apply(literal_eval)
        self.item_data['target_size'] = self.item_data['target_size'].apply(literal_eval)
    def _load_items(self):
        """
        CSV 파일에서 아이템 정보를 로드합니다.
        파일이 없으면, 기본 아이템 목록으로 새로 생성합니다.
        """
        if os.path.exists(self.filename):
            self.item_data = pd.read_csv(self.filename)
        else:
            print(f"'{self.filename}' 파일이 없어 새로 생성합니다.")
            default_items = {
                'item_name': ['sunflower', 'glasses'], # 아이템의 고유한 이름
                'category':  ['hat', 'glasses'], # 아이템 종류 (같은 종류는 중복 착용 불가)
                'purchased': [False, False],        # 구매 상태 (기본셔츠는 기본 제공)
                'equipped':  [False, False],
                'price': [25,30],
                'itemImg_path': ['assets/sunflower.png', 'assets/glasses.png']
            }

            self.item_data = pd.DataFrame(default_items)
            
            
            
            self._save_items()
    def get_equipped_hamster_surface(self):
        """
        미리 렌더링된 Item 객체의 realItemImage 서피스를 활용하여 
        착용된 아이템들을 합쳐 하나의 햄스터 서피스를 생성하고 반환합니다.
        """
        hamster_surface = None
        
        # 1. 착용 중인 모든 아이템 객체 찾기
        equipped_item_objects = []
        for item_obj in self.item_class_list:
            if item_obj.equipped and item_obj.broad_category in ['body','face','Adornment']:
                equipped_item_objects.append(item_obj)
        
        # 2. 기본 몸체 서피스 (body 카테고리) 찾기
        body_obj = None
        adornment_objs = []
        
        for item_obj in equipped_item_objects:
            if item_obj.category == 'body':
                body_obj = item_obj
            else:
                adornment_objs.append(item_obj)
        
        if body_obj is None or body_obj.realItemImage is None:
            print("오류: 착용된 햄스터 몸체 객체 또는 이미지를 찾을 수 없습니다.")
            return None
            
        # 3. 기본 햄스터 서피스 복사 (베이스 서피스)
        # 이미 로드된 서피스를 복사하여 덧씌울 준비를 합니다.
        hamster_surface = body_obj.realItemImage.copy()
        
        # 크기를 HAMSTER_SIZE로 통일해야 한다면 (혹시 로드 시 크기가 다를 경우)
        HAMSTER_SIZE = (300,300)
        #if hamster_surface.get_size() != HAMSTER_SIZE:
        #    hamster_surface = pygame.transform.smoothscale(hamster_surface, HAMSTER_SIZE)


        # 4. 장식 아이템 덧씌우기 (Overlay)
        for item_obj in adornment_objs:
            item_img = item_obj.realItemImage
            
            if item_img:
                # 덧씌우기 전에 크기가 맞는지 확인 (이미 Item.__init__에서 로드 시 크기가 맞춰졌다고 가정)
                
                hamster_surface.blit(item_img,item_obj.target_pos) 
        
        self.hamster_surface = hamster_surface
        return hamster_surface
    
    def home_surface(self):
        screen = pygame.Surface((350, 700), pygame.SRCALPHA)
        equipped_item_objects = []
        for item_obj in self.item_class_list:
            if item_obj.equipped and item_obj.broad_category in ['wallpaper','flooring','furniture']:
                equipped_item_objects.append(item_obj)
        
        for item_obj in equipped_item_objects:
            item_img = item_obj.realItemImage
            
            if item_img:
                # 덧씌우기 전에 크기가 맞는지 확인 (이미 Item.__init__에서 로드 시 크기가 맞춰졌다고 가정)
                
                screen.blit(item_img,item_obj.target_pos) 
        
        return screen
    def get_item_price(self, item_name):
        """
        특정 아이템의 가격을 가져옵니다.
        - item_name: 가격을 알고 싶은 아이템의 이름
        - 반환값: 가격(정수), 아이템이 없으면 -1 또는 None
        """
        # 1. 아이템 이름이 데이터에 있는지 확인
        if item_name not in self.item_data['item_name'].values:
            print(f"정보 없음: '{item_name}' 아이템을 찾을 수 없습니다.")
            return -1 # 오류를 의미하는 값 반환

        # === 핵심 로직: 불리언 인덱싱 ===
        # 2. 'item_name' 컬럼의 값이 item_name과 일치하는 행(row)을 찾는다.
        item_row = self.item_data[self.item_data['item_name'] == item_name]
        
        # 3. 그 행에서 'price' 컬럼의 값을 추출한다.
        # .iloc[0]은 찾은 행들 중 첫 번째 행의 값을 가져온다는 의미입니다.
        price = item_row['price'].iloc[0]
        
        return int(price)

    def _save_items(self):
        """ 현재 아이템 정보를 CSV 파일에 저장합니다. """
        self.item_data.to_csv(self.filename, index=False)
        print(f"아이템 정보가 '{self.filename}' 파일에 저장되었습니다.")

    def purchase_item(self, item):
        """ 특정 아이템을 구매만 처리합니다. (수정된 최종 버전) """
        # 1. 아이템 존재 여부 확인
        if item.name not in self.item_data['item_name'].values:
            print(f"오류: '{item.name}'은(는) 존재하지 않는 아이템입니다.")
            return False

        # 2. 이미 구매한 아이템인지 확인
        if self.is_purchased(item):
            print(f"정보: '{item.name}'은(는) 이미 구매한 아이템입니다.")
            return False

        # 3. 아이템 가격과 현재 보유 도토리 확인
        item_price = self.get_item_price(item.name)
        current_dotori = load_dotori_count()

        # 4. 도토리가 충분한지 확인
        if current_dotori < item_price:
            print(f"오류: 해바라기씨앗이 부족하여 아이템을 구매할 수 없습니다. (필요: {item_price}, 보유: {current_dotori})")
            return False
        else:
        # 5. 모든 조건 통과 -> 구매 절차 진행
        # 5-1. 도토리 차감
            use_dotori(item_price)
            item.is_purchased()
            item.purchased = True

        # 5-2. 아이템 구매 상태를 True로 변경
            item_index = self.item_data[self.item_data['item_name'] == item.name].index
            self.item_data.loc[item_index, 'purchased'] = True

        
        
        # 5-3. 변경된 내용을 파일에 저장
            self._save_items()
        
            print(f"'{item.name}' 아이템을 구매했습니다! (해바라기씨앗 {item_price}개 사용)")

        # [핵심 수정] 구매 시 자동으로 착용하던 equip_item() 호출 부분을 삭제했습니다.
        # 이제 구매만 하고 착용은 하지 않습니다.
        
        return True
    
    '''def equip_item(self, item):
        if item.name not in self.item_data['item_name'].values:
            print(f"오류: '{item.name}'은(는) 존재하지 않는 아이템입니다.")
            return False
        filtered_df = self.item_data[self.item_data['category'] == item.category]

        # 'i'가 인덱스(index)가 되고, 'row'가 행 데이터(Series)가 됩니다.
        for index, row in filtered_df.iterrows():
            # 이제 'row'를 통해 필터링된 행의 각 값에 접근할 수 있습니다.
            if row['category'] == item.category:
                self.item_class_list[index].is_purchased()
                break

        item_index = self.item_data[self.item_data['item_name'] == item.name].index
        self.item_data.loc[item_index, 'equipped'] = True
        self._save_items()
        item.is_equipped()

        print(f"'{item.name}' 아이템을 착용했습니다.")
        return False'''
    def equip_item(self, item):
        if item.name not in self.item_data['item_name'].values:
            print(f"오류: '{item.name}'은(는) 존재하지 않는 아이템입니다.")
            return False

        # 1. 같은 카테고리 아이템 필터링을 위한 마스크 생성
        category_mask = (self.item_data['category'] == item.category)
        
        # 2. **모든** 같은 카테고리 아이템의 equipped 상태를 False로 설정 (착용 해제)
        # 단, 현재 착용하려는 아이템('item.name')은 제외해야 하지만,
        # 이전에 착용했던 아이템만 False로 만들면 되므로, 아래처럼 진행합니다.
        
        # **데이터프레임에서** 같은 카테고리의 모든 아이템의 equipped를 False로 설정
        self.item_data.loc[category_mask, 'equipped'] = False
        
        # 3. 데이터프레임에서 현재 아이템의 equipped 상태를 True로 변경 (착용)
        item_index = self.item_data[self.item_data['item_name'] == item.name].index
        self.item_data.loc[item_index, 'equipped'] = True
        for i in self.item_class_list:
            if i.name == item.name:
                i.equipped = True
        
        # 4. 변경된 내용을 파일에 저장
        self._save_items()
        
        # 5. **화면에 보이는 Item 객체의 상태도 업데이트**
        # 현재 화면에 그려져 있는 (self.item_class_list에 있는) Item 객체들을 찾아서
        # 착용 해제(`is_purchased()`) 함수를 호출해야 합니다.
        
        # **Item 객체 업데이트 로직:**
        for item_obj in self.item_class_list:
            if item_obj.category == item.category:
                if item_obj.name != item.name and item_obj.purchased == True:
                    # 같은 카테고리이지만 현재 착용하는 아이템이 아닌 경우 -> 착용 해제 상태로 변경
                    item_obj.equipped = False # 객체 상태 업데이트
                    item_obj.is_purchased()  # 화면에 'PUT ON' 버튼으로 다시 그리기
                    
        # 6. 현재 아이템을 화면에 착용 상태로 그리기
        item.is_equipped()
        item.equipped = True # 현재 객체 상태 업데이트

        print(f"'{item.name}' 아이템을 착용했습니다.")
        return True # 착용 성공

    def unequip_item(self, item):
        """ 특정 아이템을 착용 해제합니다. """
        if item.name not in self.item_data['item_name'].values:
            print(f"오류: '{item.name}'은(는) 존재하지 않는 아이템입니다.")
            return False
        
        item_index = self.item_data[self.item_data['item_name'] == item.name].index
        self.item_data.loc[item_index, 'equipped'] = False
        for i in self.item_class_list:
            if i.name == item.name:
                i.equipped = False
        self._save_items()
        item.is_purchased()
        
        print(f"'{item.name}' 아이템을 착용 해제했습니다.")
        return True

    def is_purchased(self, item):
        """ 특정 아이템의 구매 여부를 확인합니다. """
        if item.name not in self.item_data['item_name'].values: return False
        status = self.item_data[self.item_data['item_name'] == item.name]['purchased'].iloc[0]
        return bool(status)

    def is_equipped(self, item):
        """ 특정 아이템의 착용 여부를 확인합니다. """
        if item.name not in self.item_data['item_name'].values: return False
        status = self.item_data[self.item_data['item_name'] == item.name]['equipped'].iloc[0]
        return bool(status)

    def get_equipped_items(self):
        """ 현재 착용 중인 모든 아이템의 리스트를 반환합니다. """
        equipped_df = self.item_data[self.item_data['equipped'] == True]
        return equipped_df['item_name'].tolist()
        
    def get_all_items_status(self):
        """ 모든 아이템의 전체 상태를 리스트-딕셔너리 형태로 반환합니다. """
        return self.item_data.to_dict('records')
    
    def scrollSurface(self,broad_category):
        df = self.item_data[self.item_data['broad_category'] == broad_category]
        rows = (len(df.index) - 1) // 3 + 1
        
# [중요] 높이 계산 시 int()로 감싸기
        height = int(10 + (108 + Item.dotoriImgWidth * 1.2) * rows)

# 2. 높이 계산 (마지막에 int로 감싸서 확실하게 정수로 만듦)
        
        scrollSurface = pygame.Surface((350, height),pygame.SRCALPHA)
        for i in range(len(df)):

            row = df.iloc[i]
            name = row.get('item_name')
            broad_category = row.get('broad_category')
            category = row.get('category')
            purchased = row.get('purchased')
            equipped = row.get('equipped')
            price = int(row.get('price', 0))
            itemIcon_path = row.get('itemIcon_path', "")
            realItem_path = row.get('realItem_path', "")
            target_pos = row.get('target_pos',"")
            target_size = row.get('target_size',"")
            
            # Item 객체 생성
            a = Item(name,broad_category, category,purchased,equipped,  price, itemIcon_path,realItem_path,target_pos,target_size)
            
            # 위치 계산 (유저의 원본 로직 유지)
            x_pos = 10 + (i % 3) * 113
            y_pos = 10 + (i // 3) * 137
            
            a.make_button(scrollSurface, x_pos, y_pos)
            
            # 클릭 이벤트 관리를 위해 리스트에 저장
            self.item_class_list.append(a)
            
        return scrollSurface



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
        print("오류: 사용하려는 해바라기씨앗 수가 보유 해바라기씨앗 수보다 많습니다.")
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
