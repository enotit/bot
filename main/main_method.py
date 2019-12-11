import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

session = requests.Session()
vk_session = vk_api.VkApi(token='c4a58f35447ae89db4fd8fc3641ee232e3f7e873c7f757c2e8c64ad73e174af383caebd11431bba5b1761')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
p = set()
try:
    print('True')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:  #  Слушаем longpoll, если пришло сообщение то:
            print(event.user_id, event.text)
            text = event.text
            id = str(event.user_id)
            p.add(id)
            if text[0] == '!':
                m = text + ' : @id' + id
                vk.messages.send(
                    user_id=159128874,
                    random_id=0,
                    attachments=event.attachments,
                    message=m
                )
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=0,
                    attachments=event.attachments,
                    message='Ваш запрос отправлен, ожидайте)'
                )
            elif event.user_id == 287826084:
                m = text + ' : @id' + id
                vk.messages.send(
                    user_id=159128874,
                    random_id=0,
                    attachments=event.attachments,
                    message=m
                )
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=0,
                    attachments=event.attachments,
                    message=event.text
                )
            elif id == '159128874' and text == 'fp':
                s = list()
                for i in p:
                    s.append(i)
                vk.messages.send(
                    user_id=159128874,
                    random_id=0,
                    attachments=event.attachments,
                    message=s
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=0,
                    attachments=event.attachments,
                    message=event.text
                )
except:
    print('Fail')
