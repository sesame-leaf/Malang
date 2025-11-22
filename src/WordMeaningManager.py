import pandas as pd


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
