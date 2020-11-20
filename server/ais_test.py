from pprint import pprint
import openpyxl
from pathlib import Path
import svgwrite
from svgwrite.shapes import Polyline
from svgwrite.mixins import ViewBox
from collections import defaultdict
import sys
import random

import pymysql
from contextlib import closing


class Person:
    def __init__(self, name, status, organisation='Default'):
        self.name = name
        self.status = status
        self.organisation = organisation


class Place:
    def __init__(self, number, status, organisation='Default'):
        self.number = number
        self.status = status
        self.organisation = organisation


# Функция создания зала с промежутками
def gen_shemNone(row_num, col_num, space_col=[], space={}):
    zal = []
    for i in range(row_num):
        ryad = []
        for j in range(col_num):
            if j in space_col:
                ryad.append(None)
            else:
                ryad.append(0)
        zal.append(ryad)

    if len(space) != 0:
        for key in space.keys():
            for value in space.get(key):
                try:
                    zal[key][value] = 8
                except IndexError:
                    continue

    return zal

# Распределние статусов для мест
def gen_shem_on_clNone(gen_shemNone, doclad={}):
    count = 0
    shema = []
    for i in range(len(gen_shemNone)):
        ryad = []
        for j in range(len(gen_shemNone[i])):
            count += 1
            # if ((i <= 2) & ((0 <= j < 3) | (7 <= j < 14) | (18 <= j < 25) | (29 <= j))) & (
            #         gen_shemNone[i][j] is not None):
            #     ryad.append(Place(count, 'doclad'))
            if doclad.get(i) is not None:
                if (j in doclad.get(i)) & (gen_shemNone[i][j] is not None):
                    ryad.append(Place(count, 'doclad'))
                elif gen_shemNone[i][j] is None:
                    ryad.append(None)
                    count -= 1
                else:
                    ryad.append(Place(count, 'gost'))
            elif gen_shemNone[i][j] is None:
                 ryad.append(None)
                 count -= 1
            else:
                ryad.append(Place(count, 'gost'))
        shema.append(ryad)
    return shema


# Функция проверки дистанции до ближайших промежутков
def checkDistNone(gen_shem_on_clNone):
    listNone = []
    for i, ryad in enumerate(gen_shem_on_clNone):
        spisok = []
        spisok.append(0)
        for j, mesto in enumerate(ryad):
            if mesto is None:
                spisok.append(j)
        spisok.append(j)
        listNone.append(spisok)
    return listNone


# Проверка наличия свободных мест
def check_place(shema):
    mesta = 0
    for i in shema:
        mesta += i.count(0)
    return mesta


def groupposadkaNone(spisok, organisation, shema, shema_on_clNone):
    check = checkDistNone(shema_on_clNone)
    #print()
    #print('Список пришедших в групповую рассадку', spisok)

    #print()
    #print('Идет рассадка ', organisation, ' !!!!!!!!!!!!!!!! ')
    #print()
    status_group = convert_list_dict(spisok, key_value=4)
    #print('Список групп-статусов', status_group)
    neubors = []
    for key in status_group.keys():
        count_m = 0
        for i, st in enumerate(shema_on_clNone):
            for j, sd in enumerate(st):
                if sd != None:
                    if (sd.status == key) & (shema[i][j] == 0):
                        count_m += 1
                else:
                    continue
        #print('мест для статуса ', key, ' = ', count_m)
        if count_m > 0:
            full_list = []
            for num_ryad, ryad in enumerate(shema_on_clNone):
                j = 0
                start = check[num_ryad][j]  # Назначаем начало первого промежутка
                if len(check[num_ryad]) > 2:  # Условие для случая отстствия промежутков
                    end = check[num_ryad][j + 1] - 1  # Так как конец ряда выпадает на "None"
                else:
                    end = check[num_ryad][j + 1]

                priority_list = []
                for num, mesto in enumerate(ryad):
                    if mesto is None:  # Если дошли до конца секции то смещаем позиции начала и конца промежутков прохода
                        j += 1
                        start = check[num_ryad][j] + 1
                        if check[num_ryad][j + 1] == (len(ryad) - 1):  # Проверка на последний промежуток
                            end = check[num_ryad][j + 1]
                        else:
                            end = check[num_ryad][j + 1] - 1
                        continue
                    # Проверка на совпадение статусов мест и занято или нет место
                    if (mesto.status == key) & (shema[num_ryad][num] == 0):
                        # Расчитываем индексы удаленности от краев start и end и расчитываем максимальный приоритет
                        left_index = abs(start - num)
                        right_index = abs(end - num)
                        max_priority = min(left_index, right_index)
                        # ДОРАБОТАТЬ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        priority_list.append([num_ryad, num, mesto, max_priority + num_ryad])

                full_list.extend(priority_list)
                priority_list.clear()

            sort_full_list = sorted(full_list, key=lambda item: item[3])

            start_i = sort_full_list[0][0]
            start_j = sort_full_list[0][1]

            replay_index = 0
            iter_index = 0
            for perChar in status_group.get(key):
                if len(neubors) == 0:
                    person = Person(perChar[3], perChar[4], organisation)
                    shema[start_i][start_j] = [person, shema_on_clNone[start_i][start_j].number]
                    replay_index += 1
                    try:
                        if (shema[start_i][start_j - 1] == 0) & (start_j - 1 >= 0):
                            neubors.append(
                                [[start_i, start_j - 1], 1, iter_index, shema_on_clNone[start_i][start_j - 1].status])
                    except IndexError:
                        pass#print('Ошибка индекса №1')
                    try:
                        if (shema[start_i][start_j + 1] == 0) & (start_j + 1 <= len(shema[start_i])):
                            neubors.append(
                                [[start_i, start_j + 1], 1, iter_index, shema_on_clNone[start_i][start_j + 1].status])
                    except IndexError:
                        pass#print('Ошибка индекса №2')
                    try:
                        if (shema[start_i + 1][start_j] == 0) & (start_i + 1 <= len(shema)):
                            neubors.append(
                                [[start_i + 1, start_j], 1, iter_index, shema_on_clNone[start_i + 1][start_j].status])
                    except IndexError:
                        pass#print('Ошибка индекса №3')
                    try:
                        if (shema[start_i - 1][start_j] == 0) & (start_i - 1 >= 0):
                            neubors.append(
                                [[start_i - 1, start_j], 1, iter_index, shema_on_clNone[start_i - 1][start_j].status])
                    except IndexError:
                        pass#print('Ошибка индекса №4')

                    try:
                        if (shema[start_i - 1][start_j + 1] == 0) & (start_i - 1 >= 0) & (
                                start_j + 1 <= len(shema[start_i])):
                            neubors.append([[start_i - 1, start_j + 1], 1, iter_index,
                                            shema_on_clNone[start_i - 1][start_j + 1].status])
                    except IndexError:
                        pass#print('Ошибка индекса №5')
                    try:
                        if (shema[start_i - 1][start_j - 1] == 0) & (start_i - 1 >= 0) & (start_j - 1 >= 0):
                            neubors.append([[start_i - 1, start_j - 1], 1, iter_index,
                                            shema_on_clNone[start_i - 1][start_j - 1].status])
                    except IndexError:
                        pass#print('Ошибка индекса №6')
                    try:
                        if (shema[start_i + 1][start_j + 1] == 0) & (start_i + 1 <= len(shema)) & (
                                start_j + 1 <= len(shema[start_i])):
                            neubors.append([[start_i + 1, start_j + 1], 1, iter_index,
                                            shema_on_clNone[start_i + 1][start_j + 1].status])
                    except IndexError:
                        pass#print('Ошибка индекса №7')
                    try:
                        if (shema[start_i + 1][start_j - 1] == 0) & (start_i + 1 <= len(shema)) & (start_j - 1 >= 0):
                            neubors.append([[start_i + 1, start_j - 1], 1, iter_index,
                                            shema_on_clNone[start_i + 1][start_j - 1].status])
                    except IndexError:
                        pass#print('Ошибка индекса №8')

                    #print('Выбраны: Точка i', start_i, 'Точка j', start_j, 'ее соседи', neubors)

                    iter_index += 1

                    # Вывод для отладки
                    # for i, row in enumerate(vivod(shema)):
                    #     for j, col in enumerate(row):
                    #         try:
                    #             if (i == start_i) & (j == start_j):
                    #                 print(f'\033[5m\033[34m{col}', ' ', end='')
                    #             else:
                    #                 print(f'\033[0m{col}', ' ', end='')
                    #         except TypeError:
                    #             print(f'\033[0m{col}', ' ', end='')
                    #     print()
                    # print()
                else:
                    neubors.sort(key=lambda item: item[2])
                    neubors.sort(key=lambda item: item[1], reverse=True)
                    person = Person(perChar[3], perChar[4], organisation)

                    neubor_index = 0

                    for neubor in neubors:
                        if neubor[3] == perChar[4]:
                            take_pl_neubor = neubors.pop(neubor_index)
                            start_i = take_pl_neubor[0][0]
                            start_j = take_pl_neubor[0][1]
                            #print('Выбраны: Точка i', start_i, 'Точка j', start_j)
                            shema[start_i][start_j] = [person, shema_on_clNone[start_i][start_j].number]
                            iter_index += 1
                            replay_index += 1
                            r1 = [start_i, start_j - 1]
                            r2 = [start_i, start_j + 1]
                            r3 = [start_i + 1, start_j]
                            r4 = [start_i - 1, start_j]
                            l1 = [start_i - 1, start_j + 1]
                            l2 = [start_i - 1, start_j - 1]
                            l3 = [start_i + 1, start_j + 1]
                            l4 = [start_i + 1, start_j - 1]

                            for ind, neubor1 in enumerate(neubors):
                                if r1 or r2 or r3 or r4 or l1 or l2 or l3 or l4 in neubor1:
                                    neubors[ind] = [[neubor1[0][0], neubor1[0][1]], neubor1[1] + 1, iter_index,
                                                    neubor1[3]]
                            temp_data_neub = [neub[0] for neub in neubors]
                            try:
                                if (r1 not in temp_data_neub) & ((shema[start_i][start_j - 1] == 0) & (start_j - 1 >= 0)):
                                    neubors.append(
                                        [[start_i, start_j - 1], 1, iter_index,
                                         shema_on_clNone[start_i][start_j - 1].status])
                            except IndexError:
                                pass#print('Ошибка индекса №1')
                            try:
                                if (r2 not in temp_data_neub) & (
                                        (shema[start_i][start_j + 1] == 0) & (start_j + 1 <= len(shema[start_i]))):
                                    neubors.append(
                                        [[start_i, start_j + 1], 1, iter_index,
                                         shema_on_clNone[start_i][start_j + 1].status])
                            except IndexError:
                                pass#print('Ошибка индекса №2')
                            try:
                                if (r3 not in temp_data_neub) & (
                                        (shema[start_i + 1][start_j] == 0) & (start_i + 1 <= len(shema))):
                                    neubors.append(
                                        [[start_i + 1, start_j], 1, iter_index,
                                         shema_on_clNone[start_i + 1][start_j].status])
                            except IndexError:
                                pass#print('Ошибка индекса №3')
                            try:
                                if (r4 not in temp_data_neub) & (
                                        (shema[start_i - 1][start_j] == 0) & (start_i - 1 >= 0)):
                                    neubors.append(
                                        [[start_i - 1, start_j], 1, 0, shema_on_clNone[start_i - 1][start_j].status])
                            except IndexError:
                                pass#print('Ошибка индекса №4')
                            try:
                                if (l1 not in temp_data_neub) & (
                                        (shema[start_i - 1][start_j + 1] == 0) & (start_i - 1 >= 0) & (
                                        start_j + 1 <= len(shema[start_i]))):
                                    neubors.append([[start_i - 1, start_j + 1], 1, iter_index,
                                                    shema_on_clNone[start_i - 1][start_j + 1].status])
                            except IndexError:
                                pass#print('Ошибка индекса №5')
                            try:
                                if (l2 not in temp_data_neub) & (
                                        (shema[start_i - 1][start_j - 1] == 0) & (start_i - 1 >= 0) & (start_j - 1 >= 0)):
                                    neubors.append([[start_i - 1, start_j - 1], 1, iter_index,
                                                    shema_on_clNone[start_i - 1][start_j - 1].status])
                            except IndexError:
                                pass#print('Ошибка индекса №6')
                            try:
                                if (l3 not in temp_data_neub) & (
                                        (shema[start_i + 1][start_j + 1] == 0) & (start_i + 1 <= len(shema)) & (
                                        start_j + 1 <= len(shema[start_i]))):
                                    neubors.append([[start_i + 1, start_j + 1], 1, iter_index,
                                                    shema_on_clNone[start_i + 1][start_j + 1].status])
                            except IndexError:
                                pass#print('Ошибка индекса №7')
                            try:
                                if (l4 not in temp_data_neub) & (
                                        (shema[start_i + 1][start_j - 1] == 0) & (start_i + 1 <= len(shema)) & (
                                        start_j - 1 >= 0)):
                                    neubors.append([[start_i + 1, start_j - 1], 1, iter_index,
                                                    shema_on_clNone[start_i + 1][start_j - 1].status])
                            except IndexError:
                                pass# print('Ошибка индекса №8')
                            break
                        else:
                            neubor_index += 1

                    if (neubor_index == len(neubors)) & (count_m > 0):
                        groupposadkaNone(status_group.get(key)[replay_index:], organisation, shema, shema_on_clNone)
                        break

                    # Вывод для отладки
                    # for i, row in enumerate(vivod(shema)):
                    #     for j, col in enumerate(row):
                    #         try:
                    #             if (shema[i][j][1] != 0) & (shema[i][j][1] != None):
                    #                 print(f'\033[5m\033[32m{col}', ' ', end='')
                    #             else:
                    #                 print(f'\033[0m{col}', ' ', end='')
                    #         except TypeError:
                    #             print(f'\033[0m{col}', ' ', end='')
                    #     print()
                    # print()
        else:
            # print('Происходит смена статусов так как мест для ', key, 'не осталось')
            if key == 'doclad':
                for record in spisok:
                    record[4] = 'gost'
            elif key == 'gost':
                for record in spisok:
                    record[4] = 'doclad'
            # print('Измененные статусы в списке: ', spisok)
            groupposadkaNone(spisok, organisation, shema, shema_on_clNone)


def fullposadkaNone(name, status, organisation, shema, shema_on_cl):
    check = checkDistNone(shema_on_cl)
    person = Person(name, status, organisation)
    # print(person.name, person.status)
    full_list = []
    for num_ryad, ryad in enumerate(shema_on_cl):
        j = 0
        start = check[num_ryad][j]  # Назначаем начало первого промежутка
        if len(check[num_ryad]) > 2:  # Условие для случая отстствия промежутков
            end = check[num_ryad][j + 1] - 1  # Так как конец ряда выпадает на "None"
        else:
            end = check[num_ryad][j + 1]

        priority_list = []
        for num, mesto in enumerate(ryad):
            if mesto is None:  # Если дошли до конца секции то смещаем позиции начала и конца промежутков прохода
                j += 1
                start = check[num_ryad][j] + 1
                if check[num_ryad][j + 1] == (len(ryad) - 1):  # Проверка на последний промежуток
                    end = check[num_ryad][j + 1]
                else:
                    end = check[num_ryad][j + 1] - 1
                continue
            # Проверка на совпадение статусов мест и занято или нет место
            if (mesto.status == person.status) & (shema[num_ryad][num] == 0):
                # Расчитываем индексы удаленности от краев start и end и расчитываем максимальный приоритет
                left_index = abs(start - num)
                right_index = abs(end - num)
                max_priority = min(left_index, right_index)
                # ДОРАБОТАТЬ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Вариант с учетом индекса удаленности от
                priority_list.append([num_ryad, num, mesto, pow(max_priority, 2) + (num_ryad * num_ryad)])
                # ввести stating (режимы в функцию на основе индекса удаленности)
                # Равномерный вариант
                # priority_list.append([num_ryad, num, mesto, max_priority + num_ryad])

        full_list.extend(priority_list)
        priority_list.clear()

    sort_full_list = sorted(full_list, key=lambda item: item[3])

    if len(sort_full_list) != 0:
        k1 = sort_full_list[0][0]
        k2 = sort_full_list[0][1]
        shema[k1][k2] = [person, sort_full_list[0][2].number]

    # print(f'\033[0mПоздравляем, Ваше место в {k1 + 1} ряду под номером {sort_full_list[0][2].number}')

    # Вывод для отладки
    # for i, row in enumerate(vivod(shema)):
    #     for j, col in enumerate(row):
    #         try:
    #             if shema[i][j][1] == sort_full_list[0][2].number:
    #                 print(f'\033[5m\033[32m{col}', ' ', end='')
    #             else:
    #                 print(f'\033[0m{col}', ' ', end='')
    #         except TypeError:
    #             print(f'\033[0m{col}', ' ', end='')
    #     print()
    # print()


# Функция рассадки
def posadkaNone(name, status, organisation, shema, shema_on_cl):
    if (status == '') | (status == None):
        status = 'gost'
    check = checkDistNone(shema_on_cl)  # Находим все промежутки на схеме
    person = Person(name, status, organisation)
    excellent = False
    # Цикл прохода по рядам
    for num_ryad, ryad in enumerate(shema_on_cl):
        j = 0
        start = check[num_ryad][j]  # Назначаем начало первого промежутка
        if len(check[num_ryad]) > 2:  # Условие для случая отстствия промежутков
            end = check[num_ryad][j + 1] - 1  # Так как конец ряда выпадает на "None"
        else:
            end = check[num_ryad][j + 1]

        priority_list = []
        # Проход по местам
        for num, mesto in enumerate(ryad):
            if mesto is None:  # Если дошли до конца секции то смещаем позиции начала и конца промежутков прохода
                j += 1
                start = check[num_ryad][j] + 1
                if check[num_ryad][j + 1] == (len(ryad) - 1):  # Проверка на последний промежуток
                    end = check[num_ryad][j + 1]
                else:
                    end = check[num_ryad][j + 1] - 1
                continue
            # Проверка на совпадение статусов мест и занято или нет место
            if (mesto.status == person.status) & (shema[num_ryad][num] == 0):
                # Расчитываем индексы удаленности от краев start и end и расчитываем максимальный приоритет
                left_index = abs(start - num)
                right_index = abs(end - num)
                max_priority = min(left_index, right_index)
                priority_list.append([num, mesto, max_priority])

        # Сортируем лист приоритетов
        sort_list = sorted(priority_list, key=lambda item: item[2])

        if len(sort_list) != 0:
            k = sort_list[0][0]
            shema[num_ryad][k] = [person, sort_list[0][1].number]
            excellent = True
            # print(f'\033[0mПоздравляем, Ваше место в {num_ryad + 1} ряду под номером {sort_list[0][1].number}')

            # Вывод с подсветкой (Только для отладки)
            # for i, row in enumerate(vivod(shema)):
            #     for j, col in enumerate(row):
            #         try:
            #             if shema[i][j][1] == sort_list[0][1].number:
            #                 print(f'\033[5m\033[32m{col}', ' ', end='')
            #             else:
            #                 print(f'\033[0m{col}', ' ', end='')
            #         except TypeError:
            #             print(f'\033[0m{col}', ' ', end='')
            #     print()
            # print()
            break

    if not excellent:
        if check_place(shema) != 0:
            if status == 'gost':
                new_status = 'doclad'
                # print(f'Места для {status} закончились, Вас посадят на место {new_status}')
                posadkaNone(name, new_status, organisation, shema, shema_on_cl)

            elif status == 'doclad':
                new_status = 'gost'
                # print(f'Места для {status} закончились, Вас посадят на место {new_status}')
                fullposadkaNone(name, new_status, organisation, shema, shema_on_cl)
        else:
            pass# print('Мест больше нет')


# Вывод свободно/занято
def vivod(q):
    u = []
    for i, k in enumerate(q):
        temp = []
        for t, j in enumerate(k):
            if type(j) == list:
                temp.append(1)
            elif j is None:
                temp.append(None)
            else:
                temp.append(0)
        u.append(temp)
    return u


# Функция поиска
def search(mass, elem):
    temp = []
    for i, row in enumerate(mass):
        for j, col in enumerate(row):
            if col is not None:
                try:
                    try:
                        if int(col[1]) == int(elem):
                            temp.append([col[0].name, col[1]])
                            return temp
                        else:
                            continue
                    except ValueError:
                        if str(col[0].name).lower().find(elem.lower()) != -1:
                            temp.append([col[0].name, col[1]])
                        else:
                            continue
                except TypeError:
                    continue
            else:
                continue
    return temp


# Функция вывода место - имя
def color_vivodSearch(shem, search):
    # print(type(number))
    for i, row in enumerate(vivod(shem)):
        for j, col in enumerate(row):
            dubl = False
            try:
                for k in search:
                    if shem[i][j][1] == k[1]:
                        print(f'\033[40m\033[34m{col}', '\033[0m ', end='')
                        dubl = True
                        break
                if dubl is False:
                    print(f'\033[0m{col}', ' ', end='')
            except TypeError:
                print(f'\033[0m{col}', ' ', end='')
        print()
    print()


# Рассадка людей из Excel файла
# Импорт из Excel
def imp_ex(file_name, list_name, start_diap, end_diap):
    wb = openpyxl.load_workbook(file_name)
    sheet = wb[list_name]
    spisok_uch = list(sheet[start_diap:end_diap])
    return spisok_uch


# Преобразование данных из экселя в список для работы в программе
def convert_data(user_ex):
    gl_list = []
    for i, str in enumerate(user_ex):
        list = []
        for j in range(len(str)):
            list.append(user_ex[i][j].value)
        gl_list.append(list)
    return gl_list


# Преобразование списка в словарь для формирования групп рассадки
def convert_list_dict(list_mass, key_value=5, start_position=0, end_position=5):
    res_dict = defaultdict(list)
    for item in list_mass:
        name = item[key_value]
        value = [i for i in item[start_position:end_position]]
        res_dict[name].append(value)
    return res_dict


# Функция построения графика рассадки в svg
def create_imgsvg(mass, mass_sh, rotRect=5, rotRectChange=5, bias=3, biasChange=3, x_dist=35, y_dist=50, x_startBias=2, color_organisation = False):
    count_in_str = len(mass[0])
    count_in_col = len(mass)
    dwg = svgwrite.Drawing('shem_ras.svg', profile='tiny', viewBox=('0 0 ' + str(count_in_str * (x_dist + 1)) + ' ' + str((count_in_col + 1) * (y_dist + 1))))
    listflang = checkDistNone(mass)

    if len(listflang[0]) >= 3:
        multi = len(listflang[0]) - 2
    else:
        multi = 1
        rotRect = 0
        rotRectChange = 0

    rotRect = rotRect/2 * multi


    #Для окраски организаций
    org = {}
    if color_organisation is True:
        for r in mass:
            for c in r:
                if c != None:
                    try:
                        org.setdefault(c[0].organisation, c[0].organisation)
                        org[c[0].organisation] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    except TypeError:
                        continue
    else:
        for r in mass:
            for c in r:
                if c != None:
                    try:
                        org.setdefault(c[0].organisation, c[0].organisation)
                        org[c[0].organisation] = (255, 165, 0)
                    except TypeError:
                        continue

    for i, row in enumerate(mass):
        y_pix = (i + 0.5) * y_dist
        cell = 1
        start = listflang[i][cell]
        rot = rotRect
        bias_y = bias

        for j, col in enumerate(row):
            x_pix = (j + 0.2) * x_dist
            if (col != 0) & (col != 9) & (col != 8):
                try:
                    name = str(col[0].name)
                    name_sp = name.split()
                    try:
                        #### Start - Для измения угла наклона
                        if start < j:
                            rot -= rotRectChange
                            cell += 1
                            start = listflang[i][cell]

                        # Смещение элементов
                        if rot > 0:
                            bias_y -= biasChange
                        elif rot < 0:
                            bias_y += biasChange
                        #### End - Для измения угла наклона

                        number_len = len(str(col[1])) * 2
                        base_px = 6

                        def sizePx(str, base_px, upp=True):
                            px_dict = {
                                7: '6',
                                8: '5',
                                9: '5',
                                10: '4',
                                11: '4',
                                12: '3',
                                13: '3',
                                14: '3',
                                15: '2',
                                16: '2',
                                17: '2',
                                18: '2',
                                19: '2'
                            }
                            if upp is True:
                                if (len(str) > base_px) & (len(str) <= 14):
                                    base_px = px_dict.get(len(str))
                                elif len(str) > 14:
                                    base_px = 3
                            else:
                                if (len(str) > base_px) & (len(str) <= 19):
                                    base_px = int(px_dict.get(len(str))) + 1
                                elif len(str) > 19:
                                    base_px = 3

                            return base_px


                        dwg.add(dwg.rect((x_pix + x_startBias, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2',
                                         fill='rgb'+str(org.get(col[0].organisation)), stroke_width=1.5,
                                         stroke='black',
                                         transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                   str(35 // 2 + y_pix + 10) + ')'))
                        dwg.add(dwg.rect((x_pix + x_startBias, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2',
                                         fill='rgb'+str(org.get(col[0].organisation)), stroke_width=1.5,
                                         stroke='black',
                                         transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                   str(35 // 2 + y_pix + 10) + ')'))
                        dwg.add(
                            dwg.text(str(col[1]), insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                     font_size='8', fill='green', font_weight='bold'))
                        # insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y)
                        # dwg.add(
                        #     dwg.viewbox(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y, 3000, 300),
                        #     dwg.text(str(col[1]), insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                        #              font_size="8px", fill='green', font_weight='bold'))

                        dwg.add(
                            dwg.text(str(col[0].organisation), insert=(x_pix + 3, y_pix + 18 - bias_y),
                                     font_size=str(sizePx(col[0].organisation, base_px)),
                                     fill='black',
                                     font_weight='bold'))
                        dwg.add(
                            dwg.text(name_sp[0], insert=(x_pix + 3, y_pix + 25 - bias_y),
                                     font_size=str(sizePx(name_sp[0], base_px)),
                                     fill='black',
                                     font_weight='bold'))
                        dwg.add(dwg.text(name_sp[1] + ' ' + name_sp[2], insert=(x_pix + 3, y_pix + 28 - bias_y),
                                         font_size=str(sizePx(name_sp[1] + ' ' + name_sp[2], base_px, upp=False)),
                                         fill='black'))
                    except IndexError:
                        dwg.add(
                            dwg.text(str(col[0].organisation), insert=(x_pix + 3, y_pix + 18 - bias_y), font_size="5px",
                                     fill='black',
                                     font_weight='bold'))
                        dwg.add(dwg.text(name[0], insert=(x_pix + x_startBias + 1, y_pix - bias_y), font_size="6px",
                                         fill='black', font_weight='bold'))
                        dwg.add(
                            dwg.text(str(col[1]), insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                     font_size="8px", fill='green', font_weight='bold'))
                except TypeError:
                    continue
            elif col == 0:
                # Для измения угла наклона (не автоматизировано полностью)
                if start < j:
                    rot -= rotRectChange
                    cell += 1
                    start = listflang[i][cell]

                # Смещение элементов
                if rot > 0:
                    bias_y -= biasChange
                elif rot < 0:
                    bias_y += biasChange

                number_len = len(str(b[i][j].number)) * 2
                dwg.add(
                    dwg.rect((x_pix + 2, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2', fill='red', stroke_width=1.5,
                             stroke='black', transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                       str(35 // 2 + y_pix + 10) + ')'))
                dwg.add(
                    dwg.rect((x_pix + 2, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2', fill='red', stroke_width=1.5,
                             stroke='black', transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                       str(35 // 2 + y_pix + 10) + ')'))
                dwg.add(dwg.text(b[i][j].number, insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                 font_size="8px", fill='black', font_weight='bold'))

            elif col == 8:
                # Для измения угла наклона (не автоматизировано полностью)
                if start < j:
                    rot -= rotRectChange
                    cell += 1
                    start = listflang[i][cell]

                # Смещение элементов
                if rot > 0:
                    bias_y -= biasChange
                elif rot < 0:
                    bias_y += biasChange



            elif col == 9:
                # Для измения угла наклона (не автоматизировано полностью)
                if start < j:
                    rot -= rotRectChange
                    cell += 1
                    start = listflang[i][cell]

                # Смещение элементов
                if rot > 0:
                    bias_y -= biasChange
                elif rot < 0:
                    bias_y += biasChange

                number_len = len(str(b[i][j].number)) * 2
                dwg.add(
                    dwg.rect((x_pix + 2, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2', fill='white', stroke_width=1.5,
                             stroke='black', transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                       str(35 // 2 + y_pix + 10) + ')'))
                dwg.add(
                    dwg.rect((x_pix + 2, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2', fill='white', stroke_width=1.5,
                             stroke='black', transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                       str(35 // 2 + y_pix + 10) + ')'))
                dwg.add(dwg.text(b[i][j].number, insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                 font_size="8px", fill='black', font_weight='bold'))
    dwg.save()


def social_modify(mass):
    for i, str in enumerate(mass):
            for j, col in enumerate(str):
                if mass[i][j] == None:
                    continue
                elif (i % 2 == 0) & (j % 2 == 0) & (mass[i][j] != 8):
                    mass[i][j] = 9
                elif (i % 2 != 0) & (j % 2 != 0) & (mass[i][j] != 8):
                    mass[i][j] = 9
    return mass


with closing(pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='ais',
    charset='utf8mb4',
                        )) as connection:

    with connection.cursor() as cursor:
        query = """
        SELECT
            *
        FROM
            users
        """
        cursor.execute(query)
        for row in cursor:
            print(row)





# sys.argv[1]
social_distance = False
excel_import = True
mass_import = []
row_num = 8
col_num = 29


# social_distance = sys.argv[0]
# excel_import = sys.argv[1]
# mass_import = sys.argv[2]
# row_num = sys.argv[3]
# col_num = sys.argv[4]

a = gen_shemNone(row_num, col_num, space_col=[7, 21], space={7: range(22, 30)})
if social_distance is True:
    a = social_modify(a)

b = gen_shem_on_clNone(a, doclad={
    0: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(range(22, 25)) + list(range(26, 30)),
    1: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(range(22, 25)) + list(range(26, 30)),
    2: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(range(22, 25)) + list(range(26, 30)),
})


if excel_import is True:
    user_ex = imp_ex('База.xlsx', 'Лист1', 'A1', 'F302')
    convert = convert_data(user_ex)
    convert_LD = convert_list_dict(convert)
else:
    user_ex = mass_import
    convert_LD = convert_list_dict(user_ex)


for i in convert_LD.keys():
    if i is None:
        continue
    elif (str(i).lower() == 'default') | (len(convert_LD.get(i)) == 1):
        for j in convert_LD.get(i):
            posadkaNone(j[3], j[4], i, a, b)
    else:
        groupposadkaNone(convert_LD.get(i), i, a, b)

create_imgsvg(a, b, color_organisation=True)

# create_imgpng(a, b, col_num, row_num)

# Программный цикл для отладки работы функции поиска:
# print('Введите номер места или имя чтобы узнать кому оно принадлежит: (0 - Exit)')
# test_num = input()
# while test_num != '0':
#     s_mass = search(a, test_num)
#     if len(s_mass) > 0:
#         for mass in s_mass:
#             print(str(mass[0]) + ' место № ' + str(mass[1]))
#         color_vivodSearch(a, s_mass)
#         print('Введите номер места или имя чтобы узнать кому оно принадлежит: (0 - Exit)')
#         test_num = input()
#     else:
#         print('По таким параметрам никого не найдено')
#         print('Введите номер места или имя чтобы узнать кому оно принадлежит: (0 - Exit)')
#         test_num = input()

for i in b:
    for j in i:
        try:
            if j.status == 'doclad':
                print(f'\033[44m\033[30m{0}', '\033[0m', sep=' ', end='')
            elif j.status == 'gost':
                print(f'\033[45m\033[30m{0}', '\033[0m', sep=' ', end='')
        except AttributeError:
            print(f'\033[0m{None}', '\033[0m', sep=' ', end='')
    print('\033[0m')
print()

print(search(a, '2'))
