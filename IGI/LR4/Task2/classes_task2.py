import re
from collections import Counter
import zipfile


class BaseAnalyzer:
    def __init__(self,  text):
        self._text = text

    
    def count_sentences(self):
        pattern = r"[^.!?]*?[.!?](?=\s+|$|\n)"
        sentences = re.findall(pattern, self._text, flags=re.MULTILINE)


        sentences = [s.strip() for s in sentences if s.strip()]
        question_count = sum(1 for s in sentences if s.strip().endswith('?'))
        exclam_count = sum(1 for s in sentences if s.strip().endswith('!'))
        normal_count = sum(1 for s in sentences if s.strip().endswith('.'))

        return normal_count, question_count, exclam_count
    

    def calculate_avg_sen_length(self):
        pattern = r"[^.!?]*?[.!?](?=\s+|$|\n)"
        sentences = re.findall(pattern, self._text)

        sentence_lengths = []
        for sentence in sentences:
            words = re.findall(r'\w+', sentence)
            total_chars = sum(len(word) for word in words)
            sentence_lengths.append(total_chars)

        average_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        return average_length
    

    def calculate_average_word_length(self):
        pattern = r"\b\w+\b"
        words = re.findall(pattern, self._text)
        total_len = 0
        count = 0
        for word in words:
            count += 1
            total_len += len(word)
        return total_len/count
    

    def analyze_on_smiles(self):
        pattern = r"[;:]-*[()\[\]]+"
        number_of_smiles = re.findall(pattern, self._text,)
        return len(number_of_smiles)
    



class SuperAnalyzer(BaseAnalyzer):
    def __init__(self,  text):
        super().__init__(text)

    def checking_for_plus(self):
        pattern = r"\d\s*\+"
        sentences = re.search(pattern, self._text)
        return sentences is not None

    def numb_of_4letters_words(self):
        pattern = r"\b\w{4}\b"
        sentences = re.findall(pattern, self._text)
        return len(sentences)

    def get_sorted_words(self):
        pattern = r"\b[а-яА-ЯёЁa-zA-Z]+\b"
        sentences = re.findall(pattern, self._text)
        sorted_words = sorted(sentences, key=len, reverse=True)
        return sorted_words
    
    def get_hexadecimal_numbers(self):
        pattern = r"\b0[xX][0-9a-fA-F]\b"
        sentences = re.findall(pattern, self._text)
        return sentences
    
    def is_balanced(self, word):
        vowels = 'аеёиоуыэюяaeiou'
        consonants = 'бвгджзйклмнпрстфхцчшщbcdfghjklmnpqrstvwxyz'

        v_count = sum(1 for ch in word.lower() if ch in vowels)
        c_count = sum(1 for ch in word.lower() if ch in consonants)

        return v_count == c_count and v_count > 0
    
    def find_balanced_words(self):
        pattern = r"\b[а-яА-ЯёЁa-zA-Z]+\b"
        words = re.findall(pattern, self._text)

        balanced = []
        for i, word in enumerate(words, start=1):
            if self.is_balanced(word):
                balanced.append((i, word))

        return balanced
    

    def analyze_text(self):
        n_count, q_count, e_count = self.count_sentences()
        result = f'''Количество повествовательных предложений: {n_count};
        Количество вопросительных предложений: {q_count};
        Количество восклицательных предложений: {e_count};
        Средняя длина предложения: {self.calculate_avg_sen_length()};
        Средняя длина слова: {self.calculate_average_word_length()};
        Количество смайликов: {self.analyze_on_smiles()};
        Список шестнадцатеричных чисел {self.get_hexadecimal_numbers()};
        {'Есть числа, после которых идет +' if self.checking_for_plus() else 'Нет чисел, после которых идет +'};
        Число слов длиной 4 символа: {self.numb_of_4letters_words()};
        Слова, у которых количество гласных равно количеству согласных и их порядковые номера: {self.find_balanced_words()}
        Слова в порядке убывания: {self.get_sorted_words()}
        '''
        return result


class FileWorker():

    def reader(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    
    def writer(file_path, content):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        

    def zipper(zip_path, file_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path)

    def get_zip_inform(zip_path):
        with zipfile.ZipFile(zip_path, "r") as zipf:
            info_list = zipf.infolist()
        return info_list