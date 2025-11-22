import pandas as pd
import os

# from src.config import *
from src.dotori import *


class ItemManager:
    def __init__(self, filename="player_items.csv"):
        """
        아이템 관리자를 초기화합니다.
        - filename: 아이템 소유 및 착용 정보를 저장할 CSV 파일 이름
        """
        self.filename = filename
        self.item_data = None
        self._load_items()

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
                'price': [25,30]          # 아이템 가격
            }
            self.item_data = pd.DataFrame(default_items)
            self._save_items()
    
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

    def purchase_item(self, item_name):
        """ 특정 아이템을 구매 처리합니다. (수정된 버전) """
        # 1. 아이템 존재 여부 확인
        if item_name not in self.item_data['item_name'].values:
            print(f"오류: '{item_name}'은(는) 존재하지 않는 아이템입니다.")
            return False

        # 2. 아이템 가격과 현재 보유 도토리 확인
        item_price = self.get_item_price(item_name)
        current_dotori = load_dotori_count()

        # 3. 도토리가 충분한지 '확인'만 합니다. (차감은 아직 안 함)
        if current_dotori < item_price:
            print(f"오류: 도토리가 부족하여 아이템을 구매할 수 없습니다. (필요: {item_price}, 보유: {current_dotori})")
            return False

        # 4. 모든 조건이 통과되었으므로, 실제 구매 절차 진행
        # 4-1. 아이템 구매 상태 변경
        item_index = self.item_data[self.item_data['item_name'] == item_name].index
        self.item_data.loc[item_index, 'purchased'] = True
        self._save_items() # CSV 파일에 구매 상태 저장

        # 4-2. 도토리 차감 (use_dotori 함수를 딱 한 번만 호출)
        use_dotori(item_price)

        print(f"'{item_name}' 아이템을 구매했습니다! (도토리 {item_price}개 사용)")
        return True

    def purchase_item(self, item_name):
        """ 특정 아이템을 구매만 처리합니다. (수정된 최종 버전) """
        # 1. 아이템 존재 여부 확인
        if item_name not in self.item_data['item_name'].values:
            print(f"오류: '{item_name}'은(는) 존재하지 않는 아이템입니다.")
            return False

        # 2. 이미 구매한 아이템인지 확인
        if self.is_purchased(item_name):
            print(f"정보: '{item_name}'은(는) 이미 구매한 아이템입니다.")
            return False

        # 3. 아이템 가격과 현재 보유 도토리 확인
        item_price = self.get_item_price(item_name)
        current_dotori = load_dotori_count()

        # 4. 도토리가 충분한지 확인
        if current_dotori < item_price:
            print(f"오류: 도토리가 부족하여 아이템을 구매할 수 없습니다. (필요: {item_price}, 보유: {current_dotori})")
            return False

        # 5. 모든 조건 통과 -> 구매 절차 진행
        # 5-1. 도토리 차감
        use_dotori(item_price)

        # 5-2. 아이템 구매 상태를 True로 변경
        item_index = self.item_data[self.item_data['item_name'] == item_name].index
        self.item_data.loc[item_index, 'purchased'] = True
        
        # 5-3. 변경된 내용을 파일에 저장
        self._save_items()
        
        print(f"'{item_name}' 아이템을 구매했습니다! (도토리 {item_price}개 사용)")

        # [핵심 수정] 구매 시 자동으로 착용하던 equip_item() 호출 부분을 삭제했습니다.
        # 이제 구매만 하고 착용은 하지 않습니다.
        
        return True
    
    def equip_item(self, item_name):
        if item_name not in self.item_data['item_name'].values:
            print(f"오류: '{item_name}'은(는) 존재하지 않는 아이템입니다.")
            return False
        
        item_index = self.item_data[self.item_data['item_name'] == item_name].index
        self.item_data.loc[item_index, 'equipped'] = True
        self._save_items()

        print(f"'{item_name}' 아이템을 착용했습니다.")
        return False

    def unequip_item(self, item_name):
        """ 특정 아이템을 착용 해제합니다. """
        if item_name not in self.item_data['item_name'].values:
            print(f"오류: '{item_name}'은(는) 존재하지 않는 아이템입니다.")
            return False
        
        item_index = self.item_data[self.item_data['item_name'] == item_name].index
        self.item_data.loc[item_index, 'equipped'] = False
        self._save_items()
        print(f"'{item_name}' 아이템을 착용 해제했습니다.")
        return True

    def is_purchased(self, item_name):
        """ 특정 아이템의 구매 여부를 확인합니다. """
        if item_name not in self.item_data['item_name'].values: return False
        status = self.item_data[self.item_data['item_name'] == item_name]['purchased'].iloc[0]
        return bool(status)

    def is_equipped(self, item_name):
        """ 특정 아이템의 착용 여부를 확인합니다. """
        if item_name not in self.item_data['item_name'].values: return False
        status = self.item_data[self.item_data['item_name'] == item_name]['equipped'].iloc[0]
        return bool(status)

    def get_equipped_items(self):
        """ 현재 착용 중인 모든 아이템의 리스트를 반환합니다. """
        equipped_df = self.item_data[self.item_data['equipped'] == True]
        return equipped_df['item_name'].tolist()
        
    def get_all_items_status(self):
        """ 모든 아이템의 전체 상태를 리스트-딕셔너리 형태로 반환합니다. """
        return self.item_data.to_dict('records')
