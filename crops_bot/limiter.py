import time
from collections import defaultdict
from datetime import datetime, timedelta

# Хранилище для статистики запросов
request_history = defaultdict(list)

def check_rate_limit(user_id: int) -> tuple:
    """Проверяет, не превысил ли пользователь лимиты запросов"""
    now = time.time()
    user_requests = request_history[user_id]
    
    # Фильтруем запросы за последний час
    hourly_requests = [t for t in user_requests if now - t < 3600]
    
    # Фильтруем запросы за последние 24 часа
    daily_requests = [t for t in user_requests if now - t < 86400]
    
    if len(hourly_requests) >= 5:
        return False, "hourly"
    if len(daily_requests) >= 20:
        return False, "daily"
    return True, None

def add_request(user_id: int):
    """Добавляет запрос в историю пользователя"""
    request_history[user_id].append(time.time())
    
    # Очищаем старые записи (старше 48 часов)
    request_history[user_id] = [t for t in request_history[user_id] if time.time() - t < 172800]

def get_usage_stats(user_id: int) -> dict:
    """Возвращает статистику использования для пользователя"""
    now = time.time()
    user_requests = request_history.get(user_id, [])
    
    return {
        "hourly": len([t for t in user_requests if now - t < 3600]),
        "daily": len([t for t in user_requests if now - t < 86400]),
        "total": len(user_requests)
    }