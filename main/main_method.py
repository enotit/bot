import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType


def vkm(id, m):
    vk.messages.send(
        user_id=id,
        random_id=0,
        attachments=event.attachments,
        message=m
    )


session = requests.Session()
vk_session = vk_api.VkApi(token='c4a58f35447ae89db4fd8fc3641ee232e3f7e873c7f757c2e8c64ad73e174af383caebd11431bba5b1761')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
p = {159128874, 427135812, 237653092, 541289155, 255211317, 328580258, 259752570, 246786232, 390427933, 255803794, 432477120, 320778806, 240155903, 324686641, 249437012, 267936374, 390240650, 571974303}
#  p = {159128874, 246786232} # for test

adm = (159128874, 246786232)
print('True')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print(event.user_id, event.text)
        text = event.text
        id = event.user_id
        p.add(id)
        if text[0] == '!':
            m = text + ' : @id' + str(id)
            vkm(159128874, m)
            vkm(id, 'Ваш запрос отправлен, ожидайте. Администратор свяжется с Вами в ближайшее время :)')
        elif id == 287826084:
            m = text + ' : Alina'
            vkm(159128874, m)
            vkm(id, text)
        elif id in adm and text == 'fp':
            s = list()
            for i in p:
                s.append(i)
            vkm(159128874, s)
        elif int(id) in adm and text[0:2] == 'R~':
            mes = text[2:] + '\n\n*Получили сообщение, потому что разрешили писать вам. Обещаем писать не часто.'
            print(p)
            for i in p:
                vkm(i, mes)
                print('Рассылка для', i, 'true')
        else:
            vkm(id, text)
