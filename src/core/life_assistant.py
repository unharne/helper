import webbrowser
from colorama import Fore, init, Style
from ..core.data_manager import DataManager
from ..games.farm import Farm
from ..utils.weather import Weather
from ..utils.cipher import Cipher
from ..network.chat import Chat
from ..games.life_gamification import LifeGamification

# Initialize colorama
init()

class LifeAssistant:
    def __init__(self):
        self.data_manager = DataManager()
        self.farm = Farm(self.data_manager)
        self.weather = Weather()
        self.cipher = Cipher()
        self.chat = Chat()
        self.life_gamification = LifeGamification(self.data_manager)
        self.name = "Гость"
        user_data = self.data_manager.get_user_data()
        if "name" in user_data:
            self.name = user_data["name"]

    def run(self):
        print("\n=== 👋 Добро пожаловать! ===")
        
        if self.name == "Гость":
            print("\nКак я могу к вам обращаться?")
            new_name = input("Введите ваше имя: ").strip()
            if new_name:
                self.set_name(new_name)
                print(f"\nПриятно познакомиться, {self.name}! 😊")
            else:
                print("\nБуду звать вас Гость! 😊")
        
        self.show_menu()

    def show_menu(self):
        while True:
            print("\n=== 🎯 Главное меню ===")
            print(f"Привет, {self.name}! 👋 Чем могу помочь?")
            print("1. 🌾 Ферма")
            print("2. 🌤️ Погода")
            print("3. 🏀 Баскетбол")
            print("4. ⚙️ Настройки")
            print("5. 🔗 GitHub")
            print("6. 🔐 Шифрование")
            print("7. 💬 Локальная беседа")
            print("8. 🎮 Геймификация жизни")
            print("9. ❌ Выход")
            
            choice = input("\nВыберите действие (1-9): ")
            
            if choice == "1":
                self.farm_game()
            elif choice == "2":
                self.show_weather()
            elif choice == "3":
                self.show_basketball_guide()
            elif choice == "4":
                self.show_settings()
            elif choice == "5":
                self.open_github()
            elif choice == "6":
                self.cipher_menu()
            elif choice == "7":
                self.chat_menu()
            elif choice == "8":
                self.life_gamification_menu()
            elif choice == "9":
                print("\nДо свидания! 👋")
                break
            else:
                print("❌ Неверный выбор")

    def show_settings(self):
        while True:
            print("\n=== ⚙️ Настройки ===")
            print("1. ✏️ Изменить имя пользователя")
            print("2. ↩️ Вернуться в меню")
            
            choice = input("\nВыберите пункт: ")
            
            if choice == "1":
                new_name = input("Введите новое имя пользователя: ").strip()
                if new_name:
                    self.set_name(new_name)
                    print(f"✅ Имя пользователя изменено на: {new_name}")
                else:
                    print("❌ Имя не может быть пустым")
            elif choice == "2":
                break
            else:
                print("❌ Неверный выбор")

    def farm_game(self):
        while True:
            self.farm.grow_crops()
            print("\n=== 🌾 Ферма ===")
            print(f"💰 Деньги: {self.farm.money} монет")
            print(f"📊 Уровень: {self.farm.level}")
            print(f"⭐ Опыт: {self.farm.experience}/{self.farm.level * 100}")
            print(f"🌤️ Погода: {self.farm.weather_effects[self.farm.weather]['emoji']} {self.farm.weather}")
            print(f"🌍 Сезон: {self.farm.seasons[self.farm.season]['emoji']} {self.farm.season}")
            print("\n1. 👀 Показать поле")
            print("2. 🌱 Посадить культуру")
            print("3. 🌿 Собрать урожай")
            print("4. 🎒 Показать инвентарь")
            print("5. 🛒 Купить семена")
            print("6. 💰 Продать урожай")
            print("7. ⚒️ Улучшить инструменты")
            print("8. 🌤️ Сменить сезон")
            print("9. ↩️ Вернуться в меню")
            
            try:
                choice = int(input("\nВыберите действие (1-9): "))
                if choice == 1:
                    self.farm.show_field()
                elif choice == 2:
                    self.farm.plant_crop()
                elif choice == 3:
                    self.farm.harvest_crop()
                elif choice == 4:
                    self.farm.show_inventory()
                elif choice == 5:
                    self.farm.buy_seeds()
                elif choice == 6:
                    self.farm.sell_crops()
                elif choice == 7:
                    self.farm.upgrade_tools()
                elif choice == 8:
                    self.farm.change_season()
                elif choice == 9:
                    break
                else:
                    print("❌ Неверный выбор")
            except ValueError:
                print("❌ Введите число от 1 до 9")

    def show_weather(self):
        city = input("Введите город: ")
        weather_info = self.weather.get_weather(city)
        print(f"\n🌤️ Погода в {city}: {weather_info}")
        input("\nНажмите Enter для продолжения...")

    def show_basketball_guide(self):
        while True:
            print("\n=== 🏀 Баскетбольный гид ===")
            print("1. 📚 Основные правила")
            print("2. 🎯 Техника броска")
            print("3. 🏃 Дриблинг и перемещения")
            print("4. 🛡️ Защита")
            print("5. 🏆 Тактические схемы")
            print("6. 💪 Тренировки")
            print("7. 📊 Статистика и анализ")
            print("8. ↩️ Вернуться в меню")
            
            try:
                choice = int(input("\nВыберите раздел (1-8): "))
                
                if choice == 1:
                    print("\n=== 📚 Основные правила ===")
                    print("• Игра состоит из 4 четвертей по 10 минут")
                    print("• Команда получает 2 очка за бросок с игры")
                    print("• 3 очка за бросок из-за трехочковой линии")
                    print("• 1 очко за штрафной бросок")
                    print("• 24 секунды на атаку")
                    print("• 5 фолов - удаление с площадки")
                    print("• 4 четверти по 10 минут")
                    print("• Перерыв между четвертями - 2 минуты")
                    print("• Большой перерыв - 15 минут")
                    
                elif choice == 2:
                    print("\n=== 🎯 Техника броска ===")
                    print("1. Стойка:")
                    print("   • Ноги на ширине плеч")
                    print("   • Колени слегка согнуты")
                    print("   • Вес на подушечках стоп")
                    print("\n2. Держание мяча:")
                    print("   • Руки образуют букву 'Т'")
                    print("   • Указательный палец на центре мяча")
                    print("   • Локоть под мячом")
                    print("\n3. Механика броска:")
                    print("   • Плавное движение снизу вверх")
                    print("   • Выпрямление рук в локтях")
                    print("   • Завершающее движение кистью")
                    print("\n4. Точка прицеливания:")
                    print("   • Передний край кольца")
                    print("   • Следить за траекторией")
                    
                elif choice == 3:
                    print("\n=== 🏃 Дриблинг и перемещения ===")
                    print("1. Основы дриблинга:")
                    print("   • Контроль мяча кончиками пальцев")
                    print("   • Мяч не выше пояса")
                    print("   • Защита мяча телом")
                    print("\n2. Виды дриблинга:")
                    print("   • Скоростной")
                    print("   • Контролируемый")
                    print("   • Защитный")
                    print("\n3. Финты и обводка:")
                    print("   • Кроссовер")
                    print("   • За спиной")
                    print("   • Между ног")
                    print("   • Разворот")
                    
                elif choice == 4:
                    print("\n=== 🛡️ Защита ===")
                    print("1. Защитная стойка:")
                    print("   • Ноги шире плеч")
                    print("   • Руки в стороны")
                    print("   • Центр тяжести низко")
                    print("\n2. Принципы защиты:")
                    print("   • Всегда между мячом и кольцом")
                    print("   • Активные руки")
                    print("   • Перемещение скольжением")
                    print("\n3. Виды защиты:")
                    print("   • Личная")
                    print("   • Зонная")
                    print("   • Прессинг")
                    
                elif choice == 5:
                    print("\n=== 🏆 Тактические схемы ===")
                    print("1. Атакующие схемы:")
                    print("   • Позиционная атака")
                    print("   • Быстрый прорыв")
                    print("   • Заслон и отрыв")
                    print("\n2. Защитные схемы:")
                    print("   • 2-3 зона")
                    print("   • 3-2 зона")
                    print("   • 1-3-1 зона")
                    print("\n3. Специальные ситуации:")
                    print("   • Вбрасывание")
                    print("   • Последний бросок")
                    
                elif choice == 6:
                    print("\n=== 💪 Тренировки ===")
                    print("1. Физическая подготовка:")
                    print("   • Беговые упражнения")
                    print("   • Прыжковые упражнения")
                    print("   • Силовые тренировки")
                    print("\n2. Технические элементы:")
                    print("   • Броски с разных дистанций")
                    print("   • Дриблинг с препятствиями")
                    print("   • Передачи в движении")
                    print("\n3. Тактические упражнения:")
                    print("   • 2x2, 3x3")
                    print("   • Игровые ситуации")
                    print("   • Контроль времени")
                    
                elif choice == 7:
                    print("\n=== 📊 Статистика и анализ ===")
                    print("1. Основные показатели:")
                    print("   • Процент попаданий")
                    print("   • Подборы")
                    print("   • Передачи")
                    print("   • Перехваты")
                    print("\n2. Анализ игры:")
                    print("   • Эффективность атаки")
                    print("   • Надежность защиты")
                    print("   • Контроль темпа")
                    print("\n3. Прогресс:")
                    print("   • Отслеживание улучшений")
                    print("   • Постановка целей")
                    print("   • Анализ ошибок")
                    
                elif choice == 8:
                    break
                else:
                    print("❌ Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("❌ Введите число от 1 до 8")
            input("\nНажмите Enter для продолжения...")

    def open_github(self):
        webbrowser.open('https://github.com/unharne')
        print("\nОткрываю GitHub профиль...")
        self.show_menu()

    def set_name(self, new_name: str):
        user_data = self.data_manager.get_user_data()
        user_data["name"] = new_name
        self.data_manager.update_user_data(user_data)
        self.name = new_name

    def cipher_menu(self):
        while True:
            print("\n=== 🔐 Шифрование ===")
            print("1. 🔑 Сгенерировать новый ключ")
            print("2. 📝 Ввести свой ключ")
            print("3. 🔒 Зашифровать текст")
            print("4. 🔓 Расшифровать текст")
            print("5. ℹ️ Информация о ключе")
            print("6. ↩️ Вернуться в меню")
            
            choice = input("\nВыберите действие (1-6): ")
            
            try:
                if choice == "1":
                    key = self.cipher.generate_key()
                    print(f"\nСгенерированный ключ: {key}")
                    print("\nСохраните этот ключ! Он понадобится для расшифровки.")
                    print("\nИнформация о ключе:")
                    print(self.cipher.get_key_info())
                
                elif choice == "2":
                    print("\nВведите ключ. Он должен содержать все символы из набора:")
                    print("• Английские буквы (a-z, A-Z)")
                    print("• Русские буквы (а-я, А-Я)")
                    print("• Цифры (0-9)")
                    print("• Специальные символы (!@#$%^&*()_+-=[]{}|;:,.<>?/~`)")
                    print(f"Всего {len(self.cipher.characters)} символов без повторений")
                    key = input("\nВведите ключ: ").strip()
                    self.cipher.set_key(key)
                    print("✅ Ключ успешно установлен")
                    print("\nИнформация о ключе:")
                    print(self.cipher.get_key_info())
                
                elif choice == "3":
                    if not self.cipher.key:
                        print("❌ Сначала нужно установить ключ")
                        continue
                    print("\nВведите текст для шифрования.")
                    print("Поддерживаются русские и английские буквы, цифры и специальные символы.")
                    text = input("\nТекст: ")
                    encrypted = self.cipher.encrypt(text)
                    print(f"\nЗашифрованный текст: {encrypted}")
                
                elif choice == "4":
                    if not self.cipher.key:
                        print("❌ Сначала нужно установить ключ")
                        continue
                    print("\nВведите текст для расшифровки.")
                    print("Поддерживаются русские и английские буквы, цифры и специальные символы.")
                    text = input("\nТекст: ")
                    decrypted = self.cipher.decrypt(text)
                    print(f"\nРасшифрованный текст: {decrypted}")
                
                elif choice == "5":
                    print("\nИнформация о текущем ключе:")
                    print(self.cipher.get_key_info())
                
                elif choice == "6":
                    break
                
                else:
                    print("❌ Неверный выбор")
            
            except ValueError as e:
                print(f"❌ Ошибка: {str(e)}")
            except Exception as e:
                print(f"❌ Произошла ошибка: {str(e)}")
            
            input("\nНажмите Enter для продолжения...")

    def chat_menu(self):
        print(Fore.CYAN + "\n🔸🔸🔸 Локальная Беседа 🔸🔸🔸")
        print("1️⃣  Запустить сервер 🚀")
        print("2️⃣  Подключиться как клиент 💬")
        choice = input("Введите номер: ").strip()

        if choice == "1":
            self.chat.start_server()
        elif choice == "2":
            self.chat.start_client()
        else:
            print(Fore.RED + "🚫 Неверный выбор. Введите 1 или 2.")

    def life_gamification_menu(self):
        while True:
            print(f"\n{Fore.CYAN}=== 🎮 Жизненная геймификация ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}👤 Уровень: {self.life_gamification.level} ⭐")
            print(f"⭐ Опыт: {int(self.life_gamification.experience)}/{int(self.life_gamification.experience_to_next_level)}")
            print(f"⚡ Энергия: {self.life_gamification.energy}/100{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Доступные действия:{Style.RESET_ALL}")
            print("1. 📝 Добавить задачу")
            print("2. ✅ Завершить задачу")
            print("3. 📜 Ежедневные задания")
            print("4. 📊 Статистика")
            print("0. ↩️ Вернуться в главное меню")
            
            choice = input(f"\n{Fore.CYAN}Выберите действие (0-4): {Style.RESET_ALL}")
            
            if choice == "0":
                break
            elif choice == "1":
                self.life_gamification.add_task()
            elif choice == "2":
                self.life_gamification.complete_task()
            elif choice == "3":
                self.life_gamification.show_daily_quests()
                if self.life_gamification.daily_quests:
                    quest_choice = input(f"\n{Fore.CYAN}Выберите задание для выполнения (1-3) или 0 для возврата: {Style.RESET_ALL}")
                    if quest_choice in ["1", "2", "3"]:
                        self.life_gamification.complete_daily_quest(int(quest_choice) - 1)
            elif choice == "4":
                self.life_gamification.show_statistics()
            else:
                print(f"{Fore.RED}❌ Неверный выбор{Style.RESET_ALL}") 