import os
import json
import datetime
from .security_manager import SecurityManager

class DataManager:
    def __init__(self):
        self.data_file = "data.json"
        self.security = SecurityManager()
        self.default_data = {
            "farm": {
                "field": [["пусто" for _ in range(5)] for _ in range(5)],
                "inventory": {
                    "морковь": 0, "картофель": 0, "помидор": 0,
                    "огурец": 0, "баклажан": 0, "тыква": 0,
                    "капуста": 0, "чеснок": 0
                },
                "money": 100,
                "seeds": {
                    "морковь": 5, "картофель": 5, "помидор": 5,
                    "огурец": 0, "баклажан": 0, "тыква": 0,
                    "капуста": 0, "чеснок": 0
                },
                "level": 1,
                "experience": 0,
                "achievements": {},
                "tools": {
                    "лопата": {"level": 1, "price": 50},
                    "лейка": {"level": 1, "price": 30},
                    "удобрение": {"level": 1, "price": 40}
                },
                "weather": "солнечно",
                "season": "весна"
            },
            "user": {
                "preferences": {
                    "communication_style": "casual",
                    "response_length": "medium",
                    "emoji_usage": "moderate"
                },
                "favorite_topics": [],
                "interaction_history": []
            },
            "security": {
                "hash": "",
                "last_modified": ""
            }
        }
        self.data = self.load_data()

    def load_data(self) -> dict:
        try:
            if not os.path.exists(self.data_file):
                data = self.default_data.copy()
                self.save_data(data)
                return data

            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Проверяем структуру данных
            if not isinstance(data, dict) or "security" not in data:
                print("⚠️ Неверная структура данных. Загружаем резервную копию...")
                return self.default_data.copy()

            # Если хеш отсутствует, генерируем его
            if not data["security"].get("hash"):
                data["security"]["hash"] = ""
                data["security"]["last_modified"] = datetime.datetime.now().isoformat()
                self.save_data(data)
                return data

            # Проверяем хеш
            stored_hash = data["security"]["hash"]
            if not self.security.verify_hash(data, stored_hash):
                print("⚠️ Обнаружена попытка изменения данных! Загружаем резервную копию...")
                return self.default_data.copy()

            return data

        except Exception as e:
            print(f"⚠️ Ошибка при загрузке данных: {e}")
            return self.default_data.copy()

    def save_data(self, data=None):
        try:
            if data is None:
                data = self.data

            data_to_save = data.copy()
            data_to_save["security"]["last_modified"] = datetime.datetime.now().isoformat()
            
            # Генерируем хеш для данных
            data_to_save["security"]["hash"] = self.security.generate_hash(data_to_save)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"⚠️ Ошибка при сохранении данных: {e}")

    def get_farm_data(self) -> dict:
        return self.data["farm"]

    def get_user_data(self) -> dict:
        return self.data["user"]

    def update_farm_data(self, farm_data: dict) -> bool:
        old_data = self.data["farm"]
        
        if not self.security.validate_money_change(old_data["money"], farm_data["money"]):
            print("⚠️ Обнаружена попытка недопустимого изменения баланса!")
            return False
        
        for item, amount in farm_data["inventory"].items():
            if not self.security.validate_item_change(old_data["inventory"][item], amount):
                print(f"⚠️ Обнаружена попытка недопустимого изменения количества {item}!")
                return False
        
        for seed, amount in farm_data["seeds"].items():
            if not self.security.validate_seed_change(old_data["seeds"][seed], amount):
                print(f"⚠️ Обнаружена попытка недопустимого изменения количества семян {seed}!")
                return False
        
        if old_data["money"] != farm_data["money"]:
            self.security.log_transaction("money_change", 
                                       farm_data["money"] - old_data["money"],
                                       old_data["money"],
                                       farm_data["money"])
        
        self.data["farm"] = farm_data
        self.save_data()
        return True

    def update_user_data(self, user_data: dict):
        self.data["user"] = user_data
        self.save_data() 