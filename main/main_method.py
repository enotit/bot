import random

import vk_api
import requests
import traceback
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime


def pr(s):
    print('-' * 5, s, '-' * 5)


def ti():
    now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    return str(f'[{now}]')


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
[all users THROUGH ',', min 2 users]
'''

pr('START')
with open("ignor.txt", "r") as file:
    tok = str(file.readline())[:-1]
    print(ti(), 'Token:', tok)
    HeadAdmin = int(file.readline())
    print(ti(), 'Main admin:', HeadAdmin)
    Admins = str(file.readline())
    print(ti(), 'All admins team:', Admins, end='')
    users = set(str(file.readline()).split(','))
    print(ti(), 'All connect users:', users)
file.close()

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
rasp = {'Понедельник': 'окно\nэкономика\n анг/нем\nправо\nинформатика\nистория\nнемецкий',
        'Вторник': 'нем\nанг/нем\nистория\nрусский\nлитра\nматематика,',
        'Среда': 'физра\nправо\noбж\nлитра\nрусский\nнемецкий',
        'Четверг': 'экономика\nобщество\nиуп\nистория\nматематика\nбиология\nгеография\nрусский',
        'Пятница': 'нем\nфизра\nфизика\nанг/нем\nматем\nматем\nлитра',
        'Суббота': 'химия\nфизика\nфизра\nастрономия',
        'Расписание': '1 - 8:30 - 9:10\n2 - 9:20 - 10:00\n3 - 10:20 - 11:00\n4 - 11:20 - 12:00\n5 - 12:20 - '
                       '13:00\n6 - 13:10 - 13:50\n7 - 14:00 - 14:40\n8 - 14:45 - 15:25'}
raspi = [i[0] for i in list(rasp.items())]
vkm(HeadAdmin, 'Жив')
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
                    if str(id) in ignor_list:
                        m = 'Бан - Запрос:\n' + text[1:] + ' : @id' + str(id)
                    else:
                        m = 'Запрос:\n' + text[1:] + ' : @id' + str(id)
                    for i in adm:
                        vkm(i, m)
                    vkm(id, 'Ваш запрос отправлен, ожидайте. Администратор свяжется с Вами в ближайшее время :)')
                else:
                    vkm(id, '⚠ Ваш запрос отменён.')
            elif id in adm and (text == 'fp' or text == 'Список участников'):
                s = list()
                for i in users:
                    s.append('@id' + i)
                vkm(id, s)
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
            elif text == 'расп':
                keyboard = VkKeyboard(one_time=False)
                p = False
                for i in raspi:
                    keyboard.add_button(str(i), color=VkKeyboardColor.PRIMARY)
                    if p:
                        keyboard.add_line()
                    p = not p
                vk.messages.send(
                    peer_id=0,
                    user_id=event.user_id,
                    random_id=random.randint(-2147483648, +2147483648),
                    keyboard=keyboard.get_keyboard(),
                    message='Лови кнопки.'
                )
            elif text in raspi:
                vkm(id, str(f'Расписание на {text}:\n{rasp[text]}'))
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
