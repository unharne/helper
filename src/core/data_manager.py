import os
import json
import datetime
from .security_manager import SecurityManager

class DataManager:
    def __init__(self):
        self.data_file = "data.json"
        self.security = SecurityManager()
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "user_data": {"name": "Гость"},
                "farm": {
                    "field": [["пусто" for _ in range(5)] for _ in range(5)],
                    "inventory": {},
                    "money": 100,
                    "seeds": {
                        "морковь": 5,
                        "картофель": 3,
                        "помидор": 2,
                        "огурец": 2,
                        "баклажан": 1,
                        "тыква": 1,
                        "капуста": 1,
                        "чеснок": 3
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
                "life_gamification": {
                    "tasks": [],
                    "achievements": [],
                    "level": 1,
                    "experience": 0,
                    "energy": 100,
                    "coins": 0,
                    "inventory": [],
                    "daily_quests": [],
                    "last_daily_reset": None
                }
            }

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_user_data(self):
        return self.data.get("user_data", {"name": "Гость"})

    def update_user_data(self, user_data):
        self.data["user_data"] = user_data
        self.save_data()

    def get_life_tasks(self):
        return self.data.get("life_gamification", {}).get("tasks", [])

    def get_life_achievements(self):
        return self.data.get("life_gamification", {}).get("achievements", [])

    def get_life_level(self):
        return self.data.get("life_gamification", {}).get("level", 1)

    def get_life_experience(self):
        return self.data.get("life_gamification", {}).get("experience", 0)

    def get_life_energy(self):
        return self.data.get("life_gamification", {}).get("energy", 100)

    def get_life_coins(self):
        return self.data.get("life_gamification", {}).get("coins", 0)

    def get_life_inventory(self):
        return self.data.get("life_gamification", {}).get("inventory", [])

    def get_life_daily_quests(self):
        return self.data.get("life_gamification", {}).get("daily_quests", [])

    def get_life_last_daily_reset(self):
        return self.data.get("life_gamification", {}).get("last_daily_reset")

    def save_life_tasks(self, tasks):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["tasks"] = tasks
        self.save_data()

    def save_life_achievements(self, achievements):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["achievements"] = achievements
        self.save_data()

    def save_life_level(self, level):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["level"] = level
        self.save_data()

    def save_life_experience(self, experience):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["experience"] = experience
        self.save_data()

    def save_life_energy(self, energy):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["energy"] = energy
        self.save_data()

    def save_life_coins(self, coins):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["coins"] = coins
        self.save_data()

    def save_life_inventory(self, inventory):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["inventory"] = inventory
        self.save_data()

    def save_life_daily_quests(self, quests):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["daily_quests"] = quests
        self.save_data()

    def save_life_last_daily_reset(self, last_reset):
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["last_daily_reset"] = last_reset
        self.save_data()

    def get_farm_data(self) -> dict:
        return self.data["farm"]

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

    def get_life_goals(self) -> list:
        return self.data["life_gamification"]["goals"]

    def save_life_goals(self, goals: list):
        self.data["life_gamification"]["goals"] = goals
        self.save_data()

    def get_life_streak(self) -> dict:
        return self.data["life_gamification"].get("streak", {"current": 0, "max": 0})

    def get_life_skills(self):
        """Получить навыки"""
        return self.data.get("life_gamification", {}).get("skills", {})

    def get_life_quests(self) -> list:
        return self.data["life_gamification"].get("quests", [])

    def get_life_rewards(self) -> list:
        return self.data["life_gamification"].get("rewards", [])

    def get_life_last_completion(self) -> str:
        return self.data["life_gamification"].get("last_completion", None)

    def save_life_streak(self, streak: dict):
        self.data["life_gamification"]["streak"] = streak
        self.save_data()

    def save_life_skills(self, skills):
        """Сохранить навыки"""
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["skills"] = skills
        self.save_data()

    def save_life_quests(self, quests: list):
        self.data["life_gamification"]["quests"] = quests
        self.save_data()

    def save_life_rewards(self, rewards: list):
        self.data["life_gamification"]["rewards"] = rewards
        self.save_data()

    def save_life_last_completion(self, last_completion: str):
        self.data["life_gamification"]["last_completion"] = last_completion
        self.save_data()

    def get_life_daily_quests(self):
        """Получить ежедневные задания"""
        return self.data.get("life_daily_quests", [])

    def save_life_daily_quests(self, quests):
        """Сохранить ежедневные задания"""
        self.data["life_daily_quests"] = quests
        self.save_data()

    def get_life_last_daily_reset(self):
        """Получить время последнего сброса ежедневных заданий"""
        return self.data.get("life_last_daily_reset")

    def get_life_friends(self):
        """Получить список друзей"""
        return self.data.get("life_gamification", {}).get("friends", [])

    def save_life_friends(self, friends):
        """Сохранить список друзей"""
        if "life_gamification" not in self.data:
            self.data["life_gamification"] = {}
        self.data["life_gamification"]["friends"] = friends
        self.save_data() 