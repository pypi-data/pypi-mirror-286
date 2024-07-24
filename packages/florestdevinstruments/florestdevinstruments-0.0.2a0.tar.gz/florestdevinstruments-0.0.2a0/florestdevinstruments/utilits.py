"""Всякие утилиты для работы с ИИ и RCON!"""
import g4f.client
from rcon.source import Client
from g4f.Provider import Bing
from MukeshAPI import api
import g4f
import requests
from typing import Union

def ai_text(prompt: str) -> str:
    """Попросите ИИ написать Вам любой текст на Ваш вкус по запросу."""
    response = g4f.client.Client().chat.completions.create(model='gpt-4o', messages=[{"role": "user", "content": prompt}], provider=Bing)
    return response.choices[0].message.content

def ai_image(prompt: str) -> bytes:
    """Попросите ИИ нарисовать картинку по Вашему запросу.\n\nВНИМАНИЕ! МОГУТ БЫТЬ НЕТОЧНОСТИ, ЖЕЛАТЕЛЬНО ВВОДИТЬ СВОЙ ЗАПРОС НА АНГЛИЙСКОМ ЯЗЫКЕ.\nФункция возвращает тип `bytes`.\nВот примерчик использования: ```with open('file.png', 'rb') as file:\nfile.write(ai_image('Draw a car.'))\nfile.close()```"""
    return api.ai_image(prompt)

def rcon_connect(host: str, passwd: str, port: int, command: str, arg1: str = None, arg2: str = None):
    """Взаимодействуйте с RCON с помощью данной функции.\nhost: IP/Домен сервера.\npasswd: RCON пароль сервера.\ncommand: Команда, которую надо прописать.\narg1, arg2 - необязательные аргументы."""
    with Client(host, port, passwd=passwd) as server:
        server.run(command, arg1, arg2)

def ip_deanon(ip: str) -> Union[list, str]:
    """Пробейте IP с помощью данной функции.\nВозвращает `list` при удачной завершении операции."""
    response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
    if response.status_code == 404:
        return f'Произошла ошибка 404. Возможно, это проблема с сайтом, которую мы используем для пробива.'
    results = response.json()
    if results['status'] == 'fail':
        return f'Не удалось пробить IP адрес, который был введен в аргумент `ip`.'
    
    record = []
    for key, value in results.items():
        record.append(f"[{key.title()}]: {value}")
    return record

