import os
import datetime
import json
import hashlib
import socket

class SecurityManager:
    def __init__(self):
        self.secret_key = os.urandom(32)
        self.transaction_log = []
        self.max_money = 1000000
        self.max_items = 1000
        self.max_seeds = 100
        self.max_transactions_per_minute = 50
        self.suspicious_activities = []
        self.last_transaction_time = datetime.datetime.now()
        self.transaction_count = 0
        
    def generate_hash(self, data: dict) -> str:
        # Создаем копию данных без хеша для консистентности
        data_copy = data.copy()
        if "security" in data_copy:
            data_copy["security"] = data_copy["security"].copy()
            data_copy["security"]["hash"] = ""
            data_copy["security"]["last_modified"] = ""
        
        # Сортируем ключи и преобразуем в JSON
        sorted_data = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(sorted_data.encode('utf-8')).hexdigest()
    
    def verify_hash(self, data: dict, hash_value: str) -> bool:
        try:
            calculated_hash = self.generate_hash(data)
            return calculated_hash == hash_value
        except Exception as e:
            print(f"Ошибка при проверке хеша: {e}")
            return False
    
    def log_transaction(self, transaction_type: str, amount: int, old_value: int, new_value: int):
        current_time = datetime.datetime.now()
        
        if (current_time - self.last_transaction_time).total_seconds() < 60:
            self.transaction_count += 1
            if self.transaction_count > self.max_transactions_per_minute:
                self.log_suspicious_activity("Превышен лимит транзакций в минуту")
                return False
        else:
            self.transaction_count = 1
            self.last_transaction_time = current_time
        
        if abs(new_value - old_value) > self.max_money * 0.5:
            self.log_suspicious_activity(f"Подозрительное изменение {transaction_type}: {old_value} -> {new_value}")
        
        timestamp = current_time.isoformat()
        self.transaction_log.append({
            "timestamp": timestamp,
            "type": transaction_type,
            "amount": amount,
            "old_value": old_value,
            "new_value": new_value,
            "ip": self.get_client_ip()
        })
        return True
    
    def log_suspicious_activity(self, activity: str):
        self.suspicious_activities.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "activity": activity,
            "ip": self.get_client_ip()
        })
        print(f"⚠️ Обнаружена подозрительная активность: {activity}")
    
    def get_client_ip(self) -> str:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "unknown"
    
    def validate_money_change(self, old_value: int, new_value: int) -> bool:
        if new_value < 0 or new_value > self.max_money:
            self.log_suspicious_activity(f"Попытка установить недопустимый баланс: {new_value}")
            return False
        if abs(new_value - old_value) > self.max_money * 0.1:
            self.log_suspicious_activity(f"Подозрительное изменение баланса: {old_value} -> {new_value}")
            return False
        return True
    
    def validate_item_change(self, old_value: int, new_value: int) -> bool:
        if new_value < 0 or new_value > self.max_items:
            self.log_suspicious_activity(f"Попытка установить недопустимое количество предметов: {new_value}")
            return False
        if abs(new_value - old_value) > self.max_items * 0.2:
            self.log_suspicious_activity(f"Подозрительное изменение количества предметов: {old_value} -> {new_value}")
            return False
        return True
    
    def validate_seed_change(self, old_value: int, new_value: int) -> bool:
        if new_value < 0 or new_value > self.max_seeds:
            self.log_suspicious_activity(f"Попытка установить недопустимое количество семян: {new_value}")
            return False
        if abs(new_value - old_value) > self.max_seeds * 0.2:
            self.log_suspicious_activity(f"Подозрительное изменение количества семян: {old_value} -> {new_value}")
            return False
        return True
    
    def get_security_report(self) -> str:
        report = []
        report.append("=== 📊 Отчет о безопасности ===")
        report.append(f"Всего транзакций: {len(self.transaction_log)}")
        report.append(f"Подозрительных активностей: {len(self.suspicious_activities)}")
        
        if self.suspicious_activities:
            report.append("\nПоследние подозрительные активности:")
            for activity in self.suspicious_activities[-5:]:
                report.append(f"• {activity['timestamp']}: {activity['activity']}")
        
        return "\n".join(report) 