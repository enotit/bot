import random
from datetime import datetime

import requests
import traceback
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType


def pr(s):
    print('-' * 5, s, '-' * 5)


def ti():
    now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    return str(f'[{now}]')


def user_id_vk(id):
    user = (vk_session.method("users.get", {"user_ids": id}))
    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
    return fullname


def name_user(id):
    return (user_id_vk(id)).split()[0]


def second_name_user(id):
    return (user_id_vk(id)).split()[1]


def vkm(id, m):
    vk.messages.send(
        user_id=id,
        random_id=random.randint(-2147483648, +2147483648),
        attachments=0,
        message=m
    )


'''
How look ignor.txt:
[token]
[chief admin]
[all admins THROUGH ',']
[all users THROUGH ',', min 2 users]
'''

pr('START')
with open("ignor.txt", "r") as file:
    tok = str(file.readline())[:-1]
    HeadAdmin = int(file.readline())
    Admins = str(file.readline())
    users = set(str(file.readline()).split(','))

print(ti(), ' All connect users: ', users, '\n',
      ti(), ' All admins team: ', Admins[:-1], '\n',
      ti(), ' Main admin: ', HeadAdmin, '\n',
      ti(), ' Token: ', tok, '\n', sep='', end='')
print('>> connect - ', ti())
session = requests.Session()
vk_session = vk_api.VkApi(token=tok)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
prod = 0  # work happy
cmdes = {'cmd', 'fp', 'ad', 'ex', 'b~', 'R~', 'Список команд'}
ignor_list = set()
time_list = [int(_) for _ in Admins.split(',')]
adm = set(time_list)
vkm(HeadAdmin, f'{ti()} {name_user(HeadAdmin)}, я работаю!')
try:
    print(ti(), 'Bot in work by mn1v')
    pr('LOG')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text and \
                (event.text.lower() == 'cmd' or event.text.lower() == 'список команд') \
                and event.user_id in adm:
            tsh = 'Команды Администратора из Личных Сообщений: \n <fp> - список всех пользователей \n <R~[text]> - ' \
                  'рассылка пользователям. Запрещена для использования!\n' \
                  '<b~[id]/[text]> - бан\n' \
                  'Команды с ЛС пользователя:\n' \
                  '<ad> - добавление в игнор лист(дублёр не работает, для диалогов)\n' \
                  '<ex> - вытаскивание из игнор листа(бан/диалог)'
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('Список команд', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Список участников', color=VkKeyboardColor.PRIMARY)
            print(keyboard.get_keyboard())
            vk.messages.send(
                peer_id=0,
                user_id=event.user_id,
                random_id=random.randint(-2147483648, +2147483648),
                keyboard=keyboard.get_keyboard(),
                message=tsh
            )
        if event.from_me:
            if event.text == 'ex':
                ignor_list.discard(str(event.user_id))
                vkm(event.user_id, 'Диалог с администратором закончился. Пожалуйста, не оффтопьте.')
            elif event.text == 'ad':
                ignor_list.add(str(event.user_id))
                vkm(event.user_id, 'Начался диалог с администратором. По завершению дублёр вернётся.')
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            prod += 1
            print(ti(), event.user_id, event.text)
            text = event.text
            id = event.user_id
            users.add(str(id))
            if text[0] == '!':
                if len(text[1:]) > 6:
                    m = f'Запрос от [id{id}|{user_id_vk(id)}], id: {id}:\n{text[1:]}'
                    if str(id) in ignor_list:
                        m = 'Бан - ' + m
                    for i in adm:
                        vkm(i, m)
                    vkm(id, 'Ваш запрос отправлен, ожидайте. Администратор свяжется с Вами в ближайшее время :)')
                else:
                    vkm(id, '⚠ Ваш запрос отменён. Символов < 6')
            elif id in adm and (text == 'fp' or text == 'Список участников'):
                s = list()
                for i in users:
                    s.append(f' [id{i}|{user_id_vk(i)}]: {i}')
                vkm(id, s)
            elif id in adm and text.lower() == 'kill':
                re = 1 / 0
            elif id in adm and text[0:2] == 'b~':
                id_ban = text[2:text.index('/')]
                ignor_list.add(id_ban)
                print(ti(), id_ban, "- заблокирован, - ", id)
                ds = 'Вас заблокировали по причине: ' + text[text.index('/') + 1:] + '\n До следующего обновления ' \
                                                                                     'системы. '
                sogl = '@id' + id_ban + ' , успешно заблокирован!'
                try:
                    vkm(id_ban, ds)
                    vkm(id, sogl)
                except:
                    vkm(id, 'Ошибочка')
            elif int(id) in adm and text[0:2] == 'R~':
                mes = text[2:] + '\n\n*Получили сообщение, потому что разрешили писать вам. Обещаем писать не часто.'
                print(ti(), users)
                for i in users:
                    try:
                        vkm(i, mes)
                    except:
                        m = 'Косяк с @id' + str(i)
                        vkm(HeadAdmin, m)
                        print(m)
                        users -= set(str(i))
                    print(ti(), 'Рассылка для', i, 'true')
            else:
                if str(id) not in ignor_list and text not in cmdes:
                    vkm(id, text)
except:
    pr('END')
    m = f'{traceback.format_exc()}: ' + str(prod)
    vkm(HeadAdmin, m)
    s = ''
    for i in users:
        s = str(s + i + ",")
    final_text = str(f'{tok}\n{HeadAdmin}\n{Admins[:-1]}\n{s[:-1]}')
    print(ti(), final_text)
    with open("ignor.txt", "w") as file:
        file.write(final_text)
    vkm(HeadAdmin, s)
pr('------')
