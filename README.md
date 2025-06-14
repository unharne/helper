# Life Assistant

Многофункциональное консольное приложение, которое включает в себя несколько полезных инструментов:

## 🌟 Основные функции

1. 🌾 **Ферма** - мини-игра с выращиванием культур
2. 🌤️ **Погода** - получение актуальной погоды для любого города
3. 🏀 **Баскетбол** - подробный гид по баскетболу
4. 🔐 **Шифрование** - инструмент для шифрования и расшифровки текста
5. 💬 **Локальная беседа** - чат для общения в локальной сети

## 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/unharne/helper.git
cd helper
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## 🎮 Использование

Запустите приложение:
```bash
python main.py
```

## 📁 Структура проекта

```
sol/
├── src/
│   ├── core/
│   │   ├── life_assistant.py
│   │   ├── security_manager.py
│   │   └── data_manager.py
│   ├── games/
│   │   └── farm.py
│   ├── utils/
│   │   ├── weather.py
│   │   └── cipher.py
│   └── network/
│       └── chat.py
├── main.py
├── requirements.txt
└── README.md
```

## 🔧 Требования

- Python 3.7+
- requests
- colorama

## 📝 Лицензия

MIT License 