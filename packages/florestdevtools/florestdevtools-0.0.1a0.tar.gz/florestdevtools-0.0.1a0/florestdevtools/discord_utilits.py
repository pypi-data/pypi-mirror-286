"""Модуль библиотеки "FlorestDevTools" для взаимодействия с Discord вебхуками, а также активностями."""
from discord import SyncWebhook, Embed
from pypresence import Presence
import pypresence
from time import time

class WebhookSender:
    """Класс для отправки чего-либо через Webhook'и. Эмбеды и текст.\n:url: Ссылка на вебхук."""
    def __init__(self, url: str):
        try:
            self.webhook = SyncWebhook.from_url(url)
        except:
            pass
    def send_text(self, text: str) -> bool:
        """Отправить текст с помощью вебхука. Возвращает `True` в случае удачной отправки текста."""
        try:
            self.webhook.send(text)
            return True
        except:
            return False
    def send_embed(self, embed: Embed):
        """Отправить эмбед с помощью вебхука. Возвращает `True` в случае удачной отправки эмбеда."""
        try:
            self.webhook.send(embed=embed)
            return True
        except:
            return False
        
def set_custom_activity(id: str, details: str, state: str, small_image: str = None, big_image: str = None, btns: list = None, is_time_shared: bool = False):
    """Поставьте свою собственную активность с помощью данного метода.\nid: ID приложения из портала разработчиков Discord.\nbtns: Кнопки с ссылками. Пример: [{'label': 'Тест', 'url':'https://pon.ru/'}]\ndetails: Вторая строчка статуса после "Играет в <название Вашего приложения>".\nstate: Третья строчка, которая идет после `details`.\nbig_image: Большое изображение из портала разработчиков.\nsmall_image: Маленькое изображение из портала разработчиков.\nis_time_shared: Показывать в активности, сколько времени прошло с начала запуска активности?\n\nНеобходимо иметь открытый Discord на ПК (Dekstop версия)."""
    if is_time_shared == True:
        presence = pypresence.Presence(id)
        presence.connect()
        presence.update(state=state, details=details, small_image=small_image, large_image=big_image, buttons=btns, start=time())
        input(f'Успешно сделали активность. Ничего не делайте с консолью.')
    else:
        presence = pypresence.Presence(id)
        presence.connect()
        presence.update(state=state, details=details, small_image=small_image, large_image=big_image, buttons=btns)
        input(f'Успешно сделали активность. Ничего не делайте с консолью.')
        
        