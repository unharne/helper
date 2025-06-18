from datetime import datetime
import random
from colorama import Fore, init, Style

init()

class LifeGamification:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.tasks = self.data_manager.get_life_tasks()
        self.level = self.data_manager.get_life_level()
        self.experience = self.data_manager.get_life_experience()
        self.experience_to_next_level = self.level * 100
        self.energy = self.data_manager.get_life_energy()
        self.daily_quests = self.data_manager.get_life_daily_quests()
        self.last_daily_reset = self.data_manager.get_life_last_daily_reset()
        self.check_daily_reset()

    def check_daily_reset(self):
        if not self.last_daily_reset:
            self.last_daily_reset = datetime.now().isoformat()
            self.data_manager.save_life_last_daily_reset(self.last_daily_reset)
            return

        last_reset = datetime.fromisoformat(self.last_daily_reset)
        if (datetime.now() - last_reset).days >= 1:
            self.energy = 100
            self.daily_quests = self.generate_daily_quests()
            self.last_daily_reset = datetime.now().isoformat()
            self.data_manager.save_life_energy(self.energy)
            self.data_manager.save_life_daily_quests(self.daily_quests)
            self.data_manager.save_life_last_daily_reset(self.last_daily_reset)
            print(f"{Fore.GREEN}✨ Ежедневный сброс! Энергия восстановлена{Style.RESET_ALL}")

    def generate_daily_quests(self):
        quest_types = [
            ("🏃", "Спорт", ["Сделать зарядку", "Пробежать 1 км", "Сделать 20 приседаний"]),
            ("📚", "Учеба", ["Прочитать 10 страниц", "Выучить 5 новых слов", "Повторить конспекты"]),
            ("💼", "Работа", ["Выполнить важную задачу", "Сделать что-то полезное", "Помочь коллеге"]),
            ("🏠", "Дом", ["Убраться в комнате", "Помыть посуду", "Постирать вещи"]),
            ("👥", "Общение", ["Позвонить другу", "Помочь близким", "Сделать комплимент"])
        ]

        quests = []
        for emoji, category, tasks in random.sample(quest_types, 3):
            quest = {
                "emoji": emoji,
                "category": category,
                "task": random.choice(tasks),
                "completed": False
            }
            quests.append(quest)
        return quests

    def add_task(self):
        if self.energy < 10:
            print(f"{Fore.RED}❌ Недостаточно энергии! Подождите следующего дня{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== 📝 Добавление задачи ==={Style.RESET_ALL}")
        task_name = input("Введите название задачи: ").strip()
        if not task_name:
            print(f"{Fore.RED}❌ Название задачи не может быть пустым{Style.RESET_ALL}")
            return

        task_type = self._select_task_type()
        difficulty = self._select_difficulty()
        deadline = self._input_deadline()

        task = {
            "name": task_name,
            "type": task_type,
            "difficulty": difficulty,
            "deadline": deadline,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "energy_cost": 10
        }

        self.tasks.append(task)
        self.energy -= 10
        self.data_manager.save_life_tasks(self.tasks)
        self.data_manager.save_life_energy(self.energy)
        print(f"{Fore.GREEN}✅ Задача успешно добавлена!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⚡ Осталось энергии: {self.energy}{Style.RESET_ALL}")

    def _select_task_type(self):
        print(f"\n{Fore.CYAN}Выберите тип задачи:{Style.RESET_ALL}")
        print("1. 🏃 Спорт и здоровье")
        print("2. 📚 Учеба и развитие")
        print("3. 💼 Работа и карьера")
        print("4. 🏠 Дом и быт")
        print("5. 👥 Общение и отношения")

        while True:
            try:
                choice = int(input("\nВыберите тип (1-5): "))
                types = {
                    1: "Спорт и здоровье",
                    2: "Учеба и развитие",
                    3: "Работа и карьера",
                    4: "Дом и быт",
                    5: "Общение и отношения"
                }
                if 1 <= choice <= 5:
                    return types[choice]
                print(f"{Fore.RED}❌ Неверный выбор{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Введите число от 1 до 5{Style.RESET_ALL}")

    def _select_difficulty(self):
        print(f"\n{Fore.CYAN}Выберите сложность:{Style.RESET_ALL}")
        print("1. 🌱 Простая (20 опыта)")
        print("2. 🌿 Средняя (40 опыта)")
        print("3. 🌳 Сложная (60 опыта)")

        while True:
            try:
                choice = int(input("\nВыберите сложность (1-3): "))
                difficulties = {
                    1: ("Простая", 20),
                    2: ("Средняя", 40),
                    3: ("Сложная", 60)
                }
                if 1 <= choice <= 3:
                    return difficulties[choice]
                print(f"{Fore.RED}❌ Неверный выбор{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Введите число от 1 до 3{Style.RESET_ALL}")

    def _input_deadline(self):
        print(f"\n{Fore.CYAN}Выберите срок выполнения:{Style.RESET_ALL}")
        print("1. ⏰ Сегодня")
        print("2. 📅 Завтра")
        print("3. 📆 На этой неделе")
        print("4. 📅 На следующей неделе")
        print("5. 📆 В этом месяце")

        while True:
            try:
                choice = int(input("\nВыберите срок (1-5): "))
                deadlines = {
                    1: "Сегодня",
                    2: "Завтра",
                    3: "На этой неделе",
                    4: "На следующей неделе",
                    5: "В этом месяце"
                }
                if 1 <= choice <= 5:
                    return deadlines[choice]
                print(f"{Fore.RED}❌ Неверный выбор{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Введите число от 1 до 5{Style.RESET_ALL}")

    def complete_task(self):
        if not self.tasks:
            print(f"{Fore.YELLOW}📝 Нет активных задач{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== ✅ Завершение задачи ==={Style.RESET_ALL}")
        for i, task in enumerate(self.tasks, 1):
            if not task["completed"]:
                status = "⏳" if task["deadline"] == "Сегодня" else "📅"
                print(f"{i}. {status} {task['name']} - {task['type']} ({task['difficulty'][0]})")

        try:
            choice = int(input("\nВыберите номер задачи (0 для отмены): "))
            if choice == 0:
                return
            if 1 <= choice <= len(self.tasks):
                task = self.tasks[choice - 1]
                if not task["completed"]:
                    task["completed"] = True
                    task["completed_at"] = datetime.now().isoformat()
                    exp_gained = self._add_experience(task["difficulty"])
                    self.data_manager.save_life_tasks(self.tasks)
                    print(f"{Fore.GREEN}✅ Задача выполнена!{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}⭐ Получено {exp_gained} опыта{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Эта задача уже выполнена{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Неверный номер задачи{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Введите корректный номер{Style.RESET_ALL}")

    def show_daily_quests(self):
        if not self.daily_quests:
            print(f"{Fore.YELLOW}📜 Нет доступных ежедневных заданий{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== 📜 Ежедневные задания ==={Style.RESET_ALL}")
        for i, quest in enumerate(self.daily_quests, 1):
            status = "✅" if quest["completed"] else "⭕"
            print(f"{i}. {quest['emoji']} {quest['category']}: {quest['task']} {status}")

    def complete_daily_quest(self, quest_index):
        if not 0 <= quest_index < len(self.daily_quests):
            print(f"{Fore.RED}❌ Неверный номер задания{Style.RESET_ALL}")
            return

        quest = self.daily_quests[quest_index]
        if quest["completed"]:
            print(f"{Fore.YELLOW}⚠️ Это задание уже выполнено{Style.RESET_ALL}")
            return

        quest["completed"] = True
        exp_gained = self._add_experience(("Средняя", 40))
        self.data_manager.save_life_daily_quests(self.daily_quests)
        print(f"{Fore.GREEN}✅ Задание выполнено!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⭐ Получено {exp_gained} опыта{Style.RESET_ALL}")

    def show_statistics(self):
        print(f"\n{Fore.CYAN}=== 📊 Статистика ==={Style.RESET_ALL}")
        print(f"{Fore.CYAN}👤 Уровень: {self.level} ⭐")
        print(f"⭐ Опыт: {int(self.experience)}/{int(self.experience_to_next_level)}")
        print(f"⚡ Энергия: {self.energy}/100")
        
        completed_tasks = sum(1 for task in self.tasks if task["completed"])
        total_tasks = len(self.tasks)
        print(f"✅ Выполнено задач: {completed_tasks}/{total_tasks}")
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            print(f"📈 Процент выполнения: {completion_rate:.1f}%")
        
        if self.tasks:
            print(f"\n{Fore.CYAN}📋 Последние задачи:{Style.RESET_ALL}")
            for task in self.tasks[-5:]:
                status = "✅" if task["completed"] else "⏳"
                print(f"{status} {task['name']} - {task['type']} ({task['difficulty'][0]})")

    def _add_experience(self, difficulty):
        _, exp = difficulty
        self.experience = round(self.experience + exp, 0)

        while self.experience >= self.experience_to_next_level:
            self.experience = round(self.experience - self.experience_to_next_level, 0)
            self.level += 1
            self.experience_to_next_level = self.level * 100
            print(f"\n{Fore.GREEN}🎉 Поздравляем! Вы достигли {self.level} уровня!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}⭐ До следующего уровня: {int(self.experience)}/{int(self.experience_to_next_level)}{Style.RESET_ALL}")
        
        self.data_manager.save_life_level(self.level)
        self.data_manager.save_life_experience(self.experience)
        return int(exp) 