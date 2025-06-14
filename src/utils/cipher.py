import random

class Cipher:
    def __init__(self):
        self.key = None
        self.characters = (
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            '0123456789'
            '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
        )
        self.special_chars = ' .,!?-:;()[]{}"\''
        
    def generate_key(self):
        self.key = ''.join(random.sample(self.characters, len(self.characters)))
        return self.key
    
    def set_key(self, key: str):
        if len(key) != len(self.characters) or not all(c in self.characters for c in key):
            raise ValueError(f"Ключ должен содержать все символы из набора ({len(self.characters)} символов) без повторений")
        self.key = key
    
    def encrypt(self, text: str) -> str:
        if not self.key:
            raise ValueError("Сначала нужно установить ключ")
        
        result = []
        for char in text:
            if char in self.characters:
                index = self.characters.index(char)
                result.append(self.key[index])
            elif char in self.special_chars:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, text: str) -> str:
        if not self.key:
            raise ValueError("Сначала нужно установить ключ")
        
        result = []
        for char in text:
            if char in self.key:
                index = self.key.index(char)
                result.append(self.characters[index])
            elif char in self.special_chars:
                result.append(char)
        return ''.join(result)

    def get_key_info(self) -> str:
        if not self.key:
            return "Ключ не установлен"
        return f"Длина ключа: {len(self.key)} символов\n" \
               f"Содержит: {sum(c.isalpha() for c in self.key)} букв, " \
               f"{sum(c.isdigit() for c in self.key)} цифр, " \
               f"{sum(not (c.isalnum() or c.isspace()) for c in self.key)} специальных символов" 