import random
from ..core.data_manager import DataManager

class Farm:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.field = self.data_manager.get_farm_data()["field"]
        self.inventory = self.data_manager.get_farm_data()["inventory"]
        self.money = self.data_manager.get_farm_data()["money"]
        self.seeds = self.data_manager.get_farm_data()["seeds"]
        self.level = self.data_manager.get_farm_data().get("level", 1)
        self.experience = self.data_manager.get_farm_data().get("experience", 0)
        self.achievements = self.data_manager.get_farm_data().get("achievements", {})
        self.tools = self.data_manager.get_farm_data().get("tools", {
            "лопата": {"level": 1, "price": 50},
            "лейка": {"level": 1, "price": 30},
            "удобрение": {"level": 1, "price": 40}
        })
        self.weather = self.data_manager.get_farm_data().get("weather", "солнечно")
        self.season = self.data_manager.get_farm_data().get("season", "весна")
        self.crops = {
            "морковь": {"time": 3, "price": 10, "sell": 15, "emoji": "🥕", "season": ["весна", "осень"]},
            "картофель": {"time": 5, "price": 15, "sell": 25, "emoji": "🥔", "season": ["весна", "лето"]},
            "помидор": {"time": 4, "price": 20, "sell": 35, "emoji": "🍅", "season": ["лето"]},
            "огурец": {"time": 4, "price": 25, "sell": 40, "emoji": "🥒", "season": ["лето"]},
            "баклажан": {"time": 6, "price": 30, "sell": 50, "emoji": "🍆", "season": ["лето"]},
            "тыква": {"time": 7, "price": 40, "sell": 70, "emoji": "🎃", "season": ["осень"]},
            "капуста": {"time": 5, "price": 35, "sell": 60, "emoji": "🥬", "season": ["осень"]},
            "чеснок": {"time": 4, "price": 20, "sell": 35, "emoji": "🧄", "season": ["весна", "осень"]}
        }
        self.field_emojis = {
            "пусто": "⬜",
            "морковь": "🥕",
            "картофель": "🥔",
            "помидор": "🍅",
            "огурец": "🥒",
            "баклажан": "🍆",
            "тыква": "🎃",
            "капуста": "🥬",
            "чеснок": "🧄",
            "росток": "🌱",
            "растущий": "🌿",
            "удобренный": "💚"
        }
        self.weather_effects = {
            "солнечно": {"growth": 1.0, "emoji": "☀️"},
            "дождливо": {"growth": 1.5, "emoji": "🌧️"},
            "пасмурно": {"growth": 0.8, "emoji": "☁️"},
            "засуха": {"growth": 0.5, "emoji": "🌵"}
        }
        self.seasons = {
            "весна": {"emoji": "🌸", "weather": ["солнечно", "дождливо"]},
            "лето": {"emoji": "☀️", "weather": ["солнечно", "засуха"]},
            "осень": {"emoji": "🍂", "weather": ["пасмурно", "дождливо"]},
            "зима": {"emoji": "❄️", "weather": ["пасмурно"]}
        }

    def save_game(self) -> bool:
        farm_data = {
            "field": self.field,
            "inventory": self.inventory,
            "money": self.money,
            "seeds": self.seeds,
            "level": self.level,
            "experience": self.experience,
            "achievements": self.achievements,
            "tools": self.tools,
            "weather": self.weather,
            "season": self.season
        }
        return self.data_manager.update_farm_data(farm_data)

    def load_game(self):
        farm_data = self.data_manager.get_farm_data()
        self.field = farm_data["field"]
        self.inventory = farm_data["inventory"]
        self.money = farm_data["money"]
        self.seeds = farm_data["seeds"]
        self.level = farm_data.get("level", 1)
        self.experience = farm_data.get("experience", 0)
        self.achievements = farm_data.get("achievements", {})
        self.tools = farm_data.get("tools", {
            "лопата": {"level": 1, "price": 50},
            "лейка": {"level": 1, "price": 30},
            "удобрение": {"level": 1, "price": 40}
        })
        self.weather = farm_data.get("weather", "солнечно")
        self.season = farm_data.get("season", "весна")

    def add_experience(self, amount: int):
        self.experience += amount
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.level_up()
        self.save_game()

    def level_up(self):
        self.level += 1
        self.experience = 0
        print(f"\n🎉 Поздравляем! Вы достигли {self.level} уровня!")
        print("Доступны новые культуры и улучшения!")
        self.check_achievements()

    def check_achievements(self):
        achievements = {
            "first_harvest": {"name": "Первый урожай", "condition": lambda: sum(self.inventory.values()) > 0},
            "rich_farmer": {"name": "Богатый фермер", "condition": lambda: self.money >= 1000},
            "master_farmer": {"name": "Мастер-фермер", "condition": lambda: self.level >= 5},
            "crop_collector": {"name": "Коллекционер культур", "condition": lambda: len(self.inventory) >= 5}
        }
        
        for ach_id, ach_data in achievements.items():
            if ach_id not in self.achievements and ach_data["condition"]():
                self.achievements[ach_id] = True
                print(f"\n🏆 Достижение разблокировано: {ach_data['name']}!")
                self.money += 100

    def update_weather(self):
        season_weathers = self.seasons[self.season]["weather"]
        self.weather = random.choice(season_weathers)
        print(f"\n🌤️ Погода изменилась: {self.weather_effects[self.weather]['emoji']} {self.weather}")

    def change_season(self):
        seasons = list(self.seasons.keys())
        current_index = seasons.index(self.season)
        next_index = (current_index + 1) % len(seasons)
        self.season = seasons[next_index]
        print(f"\n🌍 Смена сезона: {self.seasons[self.season]['emoji']} {self.season}")
        self.update_weather()

    def grow_crops(self):
        weather_effect = self.weather_effects[self.weather]["growth"]
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j] != "пусто":
                    crop = self.field[i][j]
                    if isinstance(crop, dict) and "time" in crop:
                        crop["time"] -= weather_effect
                        if crop["time"] <= 0:
                            self.field[i][j] = crop["name"]
                            self.add_experience(10)
        self.save_game()

    def show_field(self):
        print(f"\n=== 🌾 Ферма (Уровень {self.level}) ===")
        print(f"🌤️ Погода: {self.weather_effects[self.weather]['emoji']} {self.weather}")
        print(f"🌍 Сезон: {self.seasons[self.season]['emoji']} {self.season}")
        print("  1 2 3 4 5")
        for i, row in enumerate(self.field):
            print(f"{i+1}", end=" ")
            for cell in row:
                if cell == "пусто":
                    print(self.field_emojis["пусто"], end=" ")
                elif isinstance(cell, dict):
                    if cell.get("fertilized"):
                        print(self.field_emojis["удобренный"], end=" ")
                    elif cell["time"] > 1:
                        print(self.field_emojis["росток"], end=" ")
                    else:
                        print(self.field_emojis["растущий"], end=" ")
                else:
                    print(self.field_emojis[cell], end=" ")
            print()
        print("\nЛегенда:")
        print("⬜ - Пустая клетка")
        print("🌱 - Росток")
        print("🌿 - Растущая культура")
        print("💚 - Удобренная культура")
        for crop, data in self.crops.items():
            print(f"{data['emoji']} - {crop}")
        input("\nНажмите Enter для продолжения...")

    def plant_crop(self):
        print("\n=== 🌱 Посадка ===")
        print("Доступные семена:")
        crops_list = [(crop, data) for crop, data in self.crops.items() 
                     if crop in self.seeds and self.season in data["season"]]
        
        if not crops_list:
            print("❌ Нет доступных семян для текущего сезона")
            input("\nНажмите Enter для продолжения...")
            return

        for i, (crop, data) in enumerate(crops_list, 1):
            print(f"{i}. {data['emoji']} {crop}: {self.seeds[crop]} шт.")
        print("0. ↩️ Вернуться")
        
        try:
            choice = int(input("\nВыберите культуру (номер): "))
            if choice == 0:
                return
            if not (1 <= choice <= len(crops_list)):
                print("❌ Неверный выбор")
                return
            
            crop, data = crops_list[choice-1]
            if self.seeds[crop] <= 0:
                print("❌ Недостаточно семян")
                return
            
            print("\nВыберите место для посадки (строка и столбец от 1 до 5):")
            row = int(input("Строка: ")) - 1
            col = int(input("Столбец: ")) - 1
            
            if not (0 <= row < 5 and 0 <= col < 5):
                print("❌ Неверные координаты")
                return
            
            if self.field[row][col] != "пусто":
                print("❌ Это место уже занято")
                return
            
            fertilized = False
            if self.tools["удобрение"]["level"] > 1:
                use_fertilizer = input("Использовать удобрение? (да/нет): ").lower() == "да"
                if use_fertilizer:
                    fertilized = True
                    print("✅ Удобрение применено!")
            
            self.field[row][col] = {
                "name": crop,
                "time": data["time"],
                "fertilized": fertilized
            }
            self.seeds[crop] -= 1
            if not self.save_game():
                print("⚠️ Ошибка сохранения. Изменения отменены.")
                self.load_game()
            else:
                print(f"✅ {data['emoji']} {crop} посажена!")
                self.add_experience(5)
            
        except ValueError:
            print("❌ Введите число")
        input("\nНажмите Enter для продолжения...")

    def harvest_crop(self):
        print("\n=== 🌿 Сбор урожая ===")
        harvested = False
        total_harvest = {}
        
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if isinstance(self.field[i][j], str) and self.field[i][j] != "пусто":
                    crop = self.field[i][j]
                    amount = 2 if self.field[i][j].get("fertilized") else 1
                    self.inventory[crop] = self.inventory.get(crop, 0) + amount
                    total_harvest[crop] = total_harvest.get(crop, 0) + amount
                    self.field[i][j] = "пусто"
                    harvested = True
        
        if harvested:
            if not self.save_game():
                print("⚠️ Ошибка сохранения. Изменения отменены.")
                self.load_game()
            else:
                print("✅ Урожай собран!")
                print("\nСобрано:")
                for crop, amount in total_harvest.items():
                    print(f"{self.crops[crop]['emoji']} {crop}: +{amount} шт.")
                self.add_experience(15)
        else:
            print("❌ Нечего собирать")
        
        input("\nНажмите Enter для продолжения...")

    def show_inventory(self):
        print("\n=== 🎒 Инвентарь ===")
        print("Урожай:")
        for crop, amount in self.inventory.items():
            print(f"{self.crops[crop]['emoji']} {crop}: {amount} шт.")
        
        print("\nСемена:")
        for crop, amount in self.seeds.items():
            print(f"{self.crops[crop]['emoji']} {crop}: {amount} шт.")
        
        print(f"\n💰 Деньги: {self.money} монет")
        print(f"📊 Уровень: {self.level}")
        print(f"⭐ Опыт: {self.experience}/{self.level * 100}")
        
        if self.achievements:
            print("\n🏆 Достижения:")
            for ach_id in self.achievements:
                print(f"• {ach_id}")
        
        input("\nНажмите Enter для продолжения...")

    def buy_seeds(self):
        print("\n=== 🛒 Магазин семян ===")
        print("Доступные семена:")
        crops_list = [(crop, data) for crop, data in self.crops.items() 
                     if self.level >= self.get_crop_level(crop)]
        
        for i, (crop, data) in enumerate(crops_list, 1):
            print(f"{i}. {data['emoji']} {crop}: {data['price']} 💰")
        print("0. ↩️ Вернуться")
        
        try:
            choice = int(input("\nВыберите семена (номер): "))
            if choice == 0:
                return
            if not (1 <= choice <= len(crops_list)):
                print("❌ Неверный выбор")
                return
            
            crop, data = crops_list[choice-1]
            amount = int(input("Количество: "))
            if amount <= 0:
                print("❌ Введите положительное число")
                return
            
            total_cost = data["price"] * amount
            if self.money < total_cost:
                print("❌ Недостаточно денег")
                return
            
            self.money -= total_cost
            self.seeds[crop] = self.seeds.get(crop, 0) + amount
            if not self.save_game():
                print("⚠️ Ошибка сохранения. Изменения отменены.")
                self.load_game()
            else:
                print(f"✅ Куплено {amount} {data['emoji']} {crop}")
                self.add_experience(2)
            
        except ValueError:
            print("❌ Введите число")
        input("\nНажмите Enter для продолжения...")

    def get_crop_level(self, crop: str) -> int:
        crop_levels = {
            "морковь": 1,
            "картофель": 1,
            "помидор": 2,
            "огурец": 2,
            "баклажан": 3,
            "тыква": 3,
            "капуста": 4,
            "чеснок": 4
        }
        return crop_levels.get(crop, 1)

    def upgrade_tools(self):
        print("\n=== ⚒️ Улучшение инструментов ===")
        print("Доступные инструменты:")
        for i, (tool, data) in enumerate(self.tools.items(), 1):
            print(f"{i}. {tool.capitalize()} (Уровень {data['level']}) - {data['price']} 💰")
        print("0. ↩️ Вернуться")
        
        try:
            choice = int(input("\nВыберите инструмент (номер): "))
            if choice == 0:
                return
            if not (1 <= choice <= len(self.tools)):
                print("❌ Неверный выбор")
                return
            
            tool = list(self.tools.keys())[choice-1]
            tool_data = self.tools[tool]
            
            if self.money < tool_data["price"]:
                print("❌ Недостаточно денег")
                return
            
            self.money -= tool_data["price"]
            tool_data["level"] += 1
            tool_data["price"] = int(tool_data["price"] * 1.5)
            
            if not self.save_game():
                print("⚠️ Ошибка сохранения. Изменения отменены.")
                self.load_game()
            else:
                print(f"✅ {tool.capitalize()} улучшен до уровня {tool_data['level']}!")
                self.add_experience(20)
            
        except ValueError:
            print("❌ Введите число")
        input("\nНажмите Enter для продолжения...")

    def sell_crops(self):
        print("\n=== 💰 Продажа урожая ===")
        if not any(self.inventory.values()):
            print("❌ Нечего продавать")
            input("\nНажмите Enter для продолжения...")
            return
        
        print("Доступный урожай:")
        crops_list = [(crop, amount) for crop, amount in self.inventory.items() if amount > 0]
        
        for i, (crop, amount) in enumerate(crops_list, 1):
            print(f"{i}. {self.crops[crop]['emoji']} {crop}: {amount} шт. ({self.crops[crop]['sell']} 💰 за шт.)")
        print("0. ↩️ Вернуться")
        
        try:
            choice = int(input("\nВыберите культуру (номер): "))
            if choice == 0:
                return
            if not (1 <= choice <= len(crops_list)):
                print("❌ Неверный выбор")
                return
            
            crop, amount = crops_list[choice-1]
            sell_amount = int(input(f"Сколько продать (макс. {amount})? "))
            
            if sell_amount <= 0 or sell_amount > amount:
                print("❌ Неверное количество")
                return
            
            total_earnings = self.crops[crop]["sell"] * sell_amount
            self.money += total_earnings
            self.inventory[crop] -= sell_amount
            
            if not self.save_game():
                print("⚠️ Ошибка сохранения. Изменения отменены.")
                self.load_game()
            else:
                print(f"✅ Продано {sell_amount} {self.crops[crop]['emoji']} {crop} за {total_earnings} 💰")
                self.add_experience(5)
            
        except ValueError:
            print("❌ Введите число")
        input("\nНажмите Enter для продолжения...") 