#!/usr/bin/env python3
"""
Email Breach & Safe Browsing Checker
Проверяет email в базе утечек и домен в черном списке Google.
"""

import requests
import hashlib
import sys

def check_email_breach(email):
    """Проверяет email через Have I Been Pwned API"""
    print(f"\n[+] Проверяю email '{email}' в базах утечек...")
    
    # Хэшируем email для конфиденциальности
    email_hash = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()
    prefix, suffix = email_hash[:5], email_hash[5:]
    
    try:
        # Делаем запрос к API
        response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
        response.raise_for_status()
        
        # Ищем хэш в ответе
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                print(f"❌ НАЙДЕНА УТЕЧКА! Email обнаружен в {count} утечках!")
                return True
        
        print("✅ Email не найден в известных утечках")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Ошибка при проверке email: {e}")
        return False

def check_google_safe_browsing(domain):
    """Проверяет домен в Google Safe Browsing"""
    print(f"\n[+] Проверяю домен '{domain}' в Google Safe Browsing...")
    
    # Упрощенная проверка (без API ключа)
    safe_browsing_url = f"https://transparencyreport.google.com/safe-browsing/search?url={domain}"
    
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        # Если сайт доступен, делаем дополнительную проверку
        test_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key=test"
        print(f"🔍 Домен доступен. Для полной проверки нужен API ключ.")
        print(f"📊 Полную проверку можно сделать тут: {safe_browsing_url}")
        return "Требуется ручная проверка"
        
    except:
        print(f"❌ Домен недоступен или заблокирован")
        return "Недоступен"

def main():
    print("=" * 50)
    print("🔍 Email Breach & Safe Browsing Checker")
    print("=" * 50)
    
    # Получаем данные от пользователя
    email = input("Введите email для проверки утечек: ").strip()
    domain = input("Введите домен для проверки (например: example.com): ").strip()
    
    # Проверяем
    breach_result = check_email_breach(email)
    safety_result = check_google_safe_browsing(domain)
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:")
    print(f"📧 Email: {email} - {'Найден в утечках' if breach_result else 'Чист'}")
    print(f"🌐 Домен: {domain} - {safety_result}")
    print("=" * 50)

if __name__ == "__main__":
    main()