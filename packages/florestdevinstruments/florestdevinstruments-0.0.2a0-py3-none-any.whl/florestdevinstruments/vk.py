"""Перенаправление сообщений, которое получает сообщество к Вам в консоль."""
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

def listen_msgs(token: str):
    """Функция для прослушивания входящих сообщений сообществу.\ntoken: токен приложения, которое привязано к сообществу."""
    vk = VkApi(token)
    longpoll = VkLongPoll(vk)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user = vk.method("users.get", {"user_ids": event.user_id})
                fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
                print(f'Внимание!\n`{fullname}` написал(а) в ЛС сообщества.\nСообщение: `{event.text}`.\nID: `{event.user_id}`.', parse_mode='Markdown')