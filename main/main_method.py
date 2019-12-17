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
p = {331413122,390240650,255803794,157378837,390427933,571974303,328580258,159128874,324686641,255211317,320778806,246786232,432477120,541289155,427135812,169037518,249437012,237653092,267936374,259752570,240155903}
#  p = {159128874, 246786232} # for test
prod = 0
ignor_list = set()
adm = (159128874, 246786232, 249437012)
vk.messages.send(
    user_id=159128874,
    random_id=0,
    attachments=0,
    message='Жив'
)
print('True')
#try:
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text and event.text.lower() == 'cmd' and event.user_id in adm:
        tsh = 'Команды Администратора из Личных Сообщений: \n <fp> - список всех пользователей \n <R~[text]> - ' \
              'рассылка пользователям. Запрещена для использования!\n' \
              '<b~[id]/[text]> - бан\n' \
              'Команды с ЛС пользователя:\n' \
              '<ad> - добавление в игнор лист(дублёр не работает, для диалогов)' \
              '<ex> - вытаскивание из игнор листа(бан/диалог)'
        vkm(event.user_id, tsh)
    if event.from_me:
        if event.text == 'ex':
            ignor_list.discard(str(event.user_id))
            vkm(event.user_id, 'Диалог с администратором закончился. Пожалуйста, не оффтопьте.')
        elif event.text == 'ad':
            ignor_list.add(str(event.user_id))
            vkm(event.user_id, 'Начался диалог с администратором. По завершению дублёр вернётся.')
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        prod += 1
        print(event.user_id, event.text)
        text = event.text
        id = event.user_id
        p.add(id)
        if text[0] == '!':
            m = 'Запрос:\n' + text + ' : @id' + str(id)
            for i in adm:
                vkm(i, m)
            vkm(id, 'Ваш запрос отправлен, ожидайте. Администратор свяжется с Вами в ближайшее время :)')
        elif id == 287826084:
            m = text + ' : Alina'
            vkm(159128874, m)
            vkm(id, text)
        elif id in adm and text == 'fp':
            s = list()
            for i in p:
                s.append(i)
            vkm(id, s)
        elif id in adm and text[0:2] == 'b~':
            idb = text[2:text.index('/')]
            ignor_list.add(idb)
            ds = 'Вас заблокировали по причине: ' + text[text.index('/') + 1:] + '\n До следующего обновления системы.'
            sogl = '@id' + idb + ' , успешно заблокирован!'
            vkm(id, sogl)
            vkm(idb, ds)
        elif int(id) in adm and text[0:2] == 'R~':
            mes = text[2:] + '\n\n*Получили сообщение, потому что разрешили писать вам. Обещаем писать не часто.'
            print(p)
            for i in p:
                try:
                    vkm(i, mes)
                except:
                    m = 'Косяк с @' + str(i)
                    vkm(159128874, m)
                    print(m)
                    p -= set(str(i))
                print('Рассылка для', i, 'true')
        else:
            if str(id) not in ignor_list and text != 'ex' and text != 'ad' and text != 'cmd':
                vkm(id, text)
'''except:
    print('End work')
    m = 'Не жив, запросов: ' + str(prod)
    vk.messages.send(
        user_id=159128874,
        random_id=0,
        attachments=0,
        message=m
    )
    s = list()
    for i in p:
        s.append(i)
    vkm(159128874, s)
'''