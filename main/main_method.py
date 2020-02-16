import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType


def vkm(id, m):
    vk.messages.send(
        user_id=id,
        random_id=0,
        attachments=0,
        message=m
    )


'''
How look ignor.txt:
[token]
[chief admin]
[all admins THROUGH ',']

How look miniBD.txt:
[all users THROUGH ',']
'''

with open("ignor.txt", "r") as file:
    tok = str(file.readline())[:-1]
    print(tok)
    HeadAdmin = int(file.readline())
    print(HeadAdmin)
    Admins = str(file.readline())
    print(Admins)
file.close()

session = requests.Session()
vk_session = vk_api.VkApi(token=tok)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
BDfi = open('miniBD.txt', 'r')
BD = BDfi.read()

print('Start module. List: ', BD)
p = set(BD.split(','))
BDfi.close()

prod = 0    # work happy
cmdes = {'cmd', 'fp', 'ad', 'ex', 'b~', 'R~'}
ignor_list = set()
time_list = [int(_) for _ in Admins.split(',')]
adm = set(time_list)
vkm(HeadAdmin, 'Жив')

try:
    print('True')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text and event.text.lower() == 'cmd' \
                and event.user_id in adm:
            tsh = 'Команды Администратора из Личных Сообщений: \n <fp> - список всех пользователей \n <R~[text]> - ' \
                  'рассылка пользователям. Запрещена для использования!\n' \
                  '<b~[id]/[text]> - бан\n' \
                  'Команды с ЛС пользователя:\n' \
                  '<ad> - добавление в игнор лист(дублёр не работает, для диалогов)\n' \
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
            p.add(str(id))
            if text[0] == '!':
                m = 'Запрос:\n' + text[1:] + ' : @id' + str(id)
                for i in adm:
                    vkm(i, m)
                vkm(id, 'Ваш запрос отправлен, ожидайте. Администратор свяжется с Вами в ближайшее время :)')
            elif id == 287826084:
                m = text + ' : Alina'
                vkm(HeadAdmin, m)
                vkm(id, text)
            elif id in adm and text == 'fp':
                s = list()
                for i in p:
                    s.append(i)
                vkm(id, s)
            elif id in adm and text[0:2] == 'b~':
                idb = text[2:text.index('/')]
                ignor_list.add(idb)
                ds = 'Вас заблокировали по причине: ' + text[text.index('/') + 1:] + '\n До следующего обновления ' \
                                                                                     'системы. '
                sogl = '@id' + idb + ' , успешно заблокирован!'
                try:
                    vkm(idb, ds)
                    vkm(id, sogl)
                except:
                    vkm(id, 'Ошибочка')
            elif int(id) in adm and text[0:2] == 'R~':
                mes = text[2:] + '\n\n*Получили сообщение, потому что разрешили писать вам. Обещаем писать не часто.'
                print(p)
                for i in p:
                    try:
                        vkm(i, mes)
                    except:
                        m = 'Косяк с @id' + str(i)
                        vkm(HeadAdmin, m)
                        print(m)
                        p -= set(str(i))
                    print('Рассылка для', i, 'true')
            else:
                if str(id) not in ignor_list and text not in cmdes:
                    vkm(id, text)
except:
    print('End work')
    m = 'Не жив, запросов: ' + str(prod)
    vkm(HeadAdmin, m)
    s = ''
    for i in p:
        s = str(s + i + ",")
    BDfi = open('miniBD.txt', 'w')
    BDfi.write(s[:-1])
    BDfi.close()
    vkm(HeadAdmin, s)
