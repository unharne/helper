import socket
import threading
import datetime
import random
import string
from colorama import Fore

class Chat:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.key = 23  # XOR-ключ
        self.clients = {}
        
    def xor_cipher(self, message, key):
        return ''.join(chr(ord(c) ^ key) for c in message)

    def generate_access_key(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def start_server(self):
        access_key = self.generate_access_key()
        print(Fore.CYAN + f"\n🔐 Ключ доступа: {Fore.YELLOW}{access_key}\n(Сообщите этот ключ подключающимся пользователям)\n")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(Fore.CYAN + f"\n🌟 [SERVER] Сервер запущен на {self.host}:{self.port} 🚀\n")

        def broadcast(message, exclude_conn=None):
            for client_conn in self.clients:
                if client_conn != exclude_conn:
                    client_conn.send(message.encode())

        def send_participants():
            participants = "👥 Участники: " + ', '.join(self.clients.values())
            broadcast(self.xor_cipher(f"[SERVER] {participants}", self.key))
            print(Fore.MAGENTA + f"\n📢 {participants}\n")

        def handle_client(conn, addr):
            try:
                encrypted_key = conn.recv(1024).decode()
                client_key = self.xor_cipher(encrypted_key, self.key)

                if client_key.strip() != access_key:
                    print(Fore.RED + f"🚫 Неверный ключ от {addr}. Отклонено.")
                    conn.send(self.xor_cipher("[SERVER] ❌ Неверный ключ. Подключение отклонено.", self.key).encode())
                    conn.close()
                    return

                conn.send(self.xor_cipher("[SERVER] ✅ Ключ подтвержден. Введите имя.", self.key).encode())
                encrypted_name = conn.recv(1024).decode()
                username = self.xor_cipher(encrypted_name, self.key)
                self.clients[conn] = username

                print(Fore.GREEN + f"✅ {username} подключился с {addr} 🟢")
                broadcast(self.xor_cipher(f"🎉 {username} присоединился к чату! 🎉", self.key), conn)
                send_participants()

                while True:
                    encrypted_msg = conn.recv(1024).decode()
                    if not encrypted_msg:
                        break
                    decrypted_msg = self.xor_cipher(encrypted_msg, self.key)

                    if decrypted_msg == "/exit":
                        break

                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(Fore.YELLOW + f"💬 [{timestamp}] [{username}] {decrypted_msg}")
                    broadcast(self.xor_cipher(f"💬 [{timestamp}] [{username}] {decrypted_msg}", self.key), conn)

            except:
                pass
            finally:
                if conn in self.clients:
                    print(Fore.RED + f"❌ {self.clients.get(conn)} отключился. 🔴")
                    broadcast(self.xor_cipher(f"❌ {self.clients.get(conn)} покинул чат. 🔴", self.key), conn)
                    conn.close()
                    del self.clients[conn]
                    send_participants()

        def accept_connections():
            while True:
                conn, addr = server.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()

        def server_send():
            while True:
                msg = input(Fore.CYAN + "> (Вы - сервер) ")
                if msg.strip() == "":
                    continue
                if msg == "/exit":
                    print(Fore.CYAN + "🚪 Сервер завершил чат.")
                    broadcast(self.xor_cipher(f"🚪 Сервер завершил чат.", self.key))
                    break
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                broadcast(self.xor_cipher(f"💻 [{timestamp}] [Сервер] {msg}", self.key))
                print(Fore.YELLOW + f"💬 [{timestamp}] [Вы] {msg}")

        threading.Thread(target=accept_connections, daemon=True).start()
        server_send()
        server.close()

    def start_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.host, self.port))
        except Exception as e:
            print(Fore.RED + f"🚫 Не удалось подключиться к {self.host}:{self.port}: {e}")
            return

        user_key = input(Fore.CYAN + "🔐 Введите ключ доступа: ").strip()
        client.send(self.xor_cipher(user_key, self.key).encode())

        try:
            server_response = client.recv(1024).decode()
            decrypted_response = self.xor_cipher(server_response, self.key)
            if "Неверный ключ" in decrypted_response:
                print(Fore.RED + "🚫 Неверный ключ. Подключение закрыто.")
                client.close()
                return
            elif "Ключ подтвержден" in decrypted_response:
                print(Fore.GREEN + "✅ Ключ подтвержден. Продолжение подключения... 🟢")
            else:
                print(Fore.RED + "🚫 Непредвиденный ответ от сервера.")
                client.close()
                return

        except:
            print(Fore.RED + "🚫 Ошибка подключения.")
            client.close()
            return

        username = input(Fore.CYAN + "👤 Введите ваше имя: ").strip()
        if not username:
            username = "Гость"

        encrypted_name = self.xor_cipher(username, self.key)
        client.send(encrypted_name.encode())
        print(Fore.GREEN + f"\n🔗 Подключен к серверу {self.host}:{self.port} как {username} 🟢")
        print(Fore.CYAN + "✏️  Введите сообщения, используйте /exit для выхода.\n")

        def receive_messages():
            while True:
                try:
                    encrypted_msg = client.recv(1024).decode()
                    decrypted_msg = self.xor_cipher(encrypted_msg, self.key)
                    if decrypted_msg:
                        if decrypted_msg.startswith("[SERVER]") or "Участники" in decrypted_msg:
                            print(Fore.MAGENTA + f"\n{decrypted_msg}\n> ", end="")
                        else:
                            print(Fore.YELLOW + f"\n📨 {decrypted_msg}\n> ", end="")
                except:
                    print(Fore.RED + "\n❗ [ERROR] Потеря соединения с сервером. 🔴\n")
                    client.close()
                    break

        def send_messages():
            while True:
                msg = input("> ")
                if msg.strip() == "":
                    continue
                if msg == "/exit":
                    encrypted_msg = self.xor_cipher(msg, self.key)
                    client.send(encrypted_msg.encode())
                    print(Fore.CYAN + "🚪 Выход из чата...")
                    client.close()
                    break
                encrypted_msg = self.xor_cipher(msg, self.key)
                client.send(encrypted_msg.encode())

        threading.Thread(target=receive_messages, daemon=True).start()
        send_messages() 