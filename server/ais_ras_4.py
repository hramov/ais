from pprint import pprint
import openpyxl
from pathlib import Path
import svgwrite
from svgwrite.shapes import Polyline
from svgwrite.mixins import ViewBox
from collections import defaultdict
import sys
import random
import json
from flask import jsonify

import pymysql
from contextlib import closing


class Person:
    def __init__(self, user_id, name, status, organisation='Default'):
        self.user_id = user_id
        self.name = name
        self.status = status
        self.organisation = organisation


class Place:
    def __init__(self, number, status, organisation='Default'):
        self.number = number
        self.status = status
        self.organisation = organisation


class Premise:
    def __init__(self, row_num, col_num, space_col=[], space={}, doclad={}):
        self.row_num = row_num
        self.col_num = col_num
        self.space_col = space_col
        self.space = space
        self.doclad = doclad


    # Функция создания зала с промежутками
    def gen_shemNone(self):
        zal = []
        for i in range(self.row_num):
            ryad = []
            for j in range(self.col_num):
                if j in self.space_col:
                    ryad.append(None)
                else:
                    ryad.append(0)
            zal.append(ryad)

        if len(self.space) != 0:
            for key in self.space.keys():
                for value in self.space.get(key):
                    try:
                        if zal[key][value] != None:
                            zal[key][value] = 8
                        else:
                            continue
                    except IndexError:
                        continue

        self.shemNone = zal
        return zal


    # Распределние статусов для мест
    def gen_shem_on_clNone(self, shemNone):
        count = 0
        shema = []
        for i in range(len(shemNone)):
            ryad = []
            for j in range(len(shemNone[i])):
                count += 1
                if self.doclad.get(i) is not None:
                    if (j in self.doclad.get(i)) & (shemNone[i][j] is not None):
                        ryad.append(Place(count, 'doclad'))
                    elif shemNone[i][j] is None:
                        ryad.append(None)
                        count -= 1
                    elif shemNone[i][j] == 8:
                        ryad.append(None)
                        count -= 1
                    else:
                        ryad.append(Place(count, 'gost'))
                elif shemNone[i][j] is None:
                    ryad.append(None)
                    count -= 1
                elif shemNone[i][j] == 8:
                    ryad.append(None)
                    count -= 1
                else:
                    ryad.append(Place(count, 'gost'))
            shema.append(ryad)

        self.shem_on_clNone = shema
        return shema


    # Социальная дистанция
    def social_modify(self, shemNone):
        for i, str in enumerate(shemNone):
            for j, col in enumerate(str):
                if shemNone[i][j] == None:
                    continue
                elif (i % 2 == 0) & (j % 2 == 0) & (shemNone[i][j] != 8):
                    shemNone[i][j] = 9
                elif (i % 2 != 0) & (j % 2 != 0) & (shemNone[i][j] != 8):
                    shemNone[i][j] = 9
        return shemNone

    # Функция проверки дистанции до ближайших промежутков
    def checkDistNone(self, shem_on_clNone):
        listNone = []
        for i, ryad in enumerate(shem_on_clNone):
            spisok = []
            spisok.append(0)
            for j, mesto in enumerate(ryad):
                if mesto is None:
                    spisok.append(j)
            spisok.append(j)
            listNone.append(spisok)
        return listNone

    # Проверка наличия свободных мест
    def check_place(self, shemNone):
        mesta = 0
        for i in shemNone:
            mesta += i.count(0)
        return mesta


    def groupposadkaNone(self, spisok, organisation, shemNone, shem_on_clNone):
        check = self.checkDistNone(shem_on_clNone)
        status_group = convert_list_dict(spisok, key_value=4)
        if self.check_place(shemNone) > 0:
            # print('Список групп-статусов', status_group)
            neubors = []
            for key in status_group.keys():
                count_m = 0
                for i, st in enumerate(shem_on_clNone):
                    for j, sd in enumerate(st):
                        if sd != None:
                            if (sd.status == key) & (shemNone[i][j] == 0):
                                count_m += 1
                        else:
                            continue
                # print('мест для статуса ', key, ' = ', count_m)
                replay_index = 0
                iter_index = 0
                if count_m > 0:
                    full_list = []
                    for num_ryad, ryad in enumerate(shem_on_clNone):
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
                            if (mesto.status == key) & (shemNone[num_ryad][num] == 0):
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

                    for perChar in status_group.get(key):
                        if len(neubors) == 0:
                            person = Person(perChar[0], perChar[3], perChar[4], organisation)
                            shemNone[start_i][start_j] = [person, shem_on_clNone[start_i][start_j].number]
                            replay_index += 1
                            try:
                                if (shemNone[start_i][start_j - 1] == 0) & (start_j - 1 >= 0):
                                    neubors.append(
                                        [[start_i, start_j - 1], 1, iter_index,
                                         shem_on_clNone[start_i][start_j - 1].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №1')
                            try:
                                if (shemNone[start_i][start_j + 1] == 0) & (start_j + 1 <= len(shemNone[start_i])):
                                    neubors.append(
                                        [[start_i, start_j + 1], 1, iter_index,
                                         shem_on_clNone[start_i][start_j + 1].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №2')
                            try:
                                if (shemNone[start_i + 1][start_j] == 0) & (start_i + 1 <= len(shemNone)):
                                    neubors.append(
                                        [[start_i + 1, start_j], 1, iter_index,
                                         shem_on_clNone[start_i + 1][start_j].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №3')
                            try:
                                if (shemNone[start_i - 1][start_j] == 0) & (start_i - 1 >= 0):
                                    neubors.append(
                                        [[start_i - 1, start_j], 1, iter_index,
                                         shem_on_clNone[start_i - 1][start_j].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №4')

                            try:
                                if (shemNone[start_i - 1][start_j + 1] == 0) & (start_i - 1 >= 0) & (
                                        start_j + 1 <= len(shemNone[start_i])):
                                    neubors.append([[start_i - 1, start_j + 1], 1, iter_index,
                                                    shem_on_clNone[start_i - 1][start_j + 1].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №5')
                            try:
                                if (shemNone[start_i - 1][start_j - 1] == 0) & (start_i - 1 >= 0) & (start_j - 1 >= 0):
                                    neubors.append([[start_i - 1, start_j - 1], 1, iter_index,
                                                    shem_on_clNone[start_i - 1][start_j - 1].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №6')
                            try:
                                if (shemNone[start_i + 1][start_j + 1] == 0) & (start_i + 1 <= len(shemNone)) & (
                                        start_j + 1 <= len(shemNone[start_i])):
                                    neubors.append([[start_i + 1, start_j + 1], 1, iter_index,
                                                    shem_on_clNone[start_i + 1][start_j + 1].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №7')
                            try:
                                if (shemNone[start_i + 1][start_j - 1] == 0) & (start_i + 1 <= len(shemNone)) & (
                                        start_j - 1 >= 0):
                                    neubors.append([[start_i + 1, start_j - 1], 1, iter_index,
                                                    shem_on_clNone[start_i + 1][start_j - 1].status])
                            except IndexError:
                                pass  # print('Ошибка индекса №8')

                            iter_index += 1

                        else:
                            neubors.sort(key=lambda item: item[2])
                            neubors.sort(key=lambda item: item[1], reverse=True)
                            person = Person(perChar[0], perChar[3], perChar[4], organisation)

                            neubor_index = 0

                            for neubor in neubors:
                                if neubor[3] == perChar[4]:
                                    take_pl_neubor = neubors.pop(neubor_index)
                                    start_i = take_pl_neubor[0][0]
                                    start_j = take_pl_neubor[0][1]
                                    # print('Выбраны: Точка i', start_i, 'Точка j', start_j)
                                    shemNone[start_i][start_j] = [person, shem_on_clNone[start_i][start_j].number]
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
                                        if (r1 not in temp_data_neub) & (
                                                (shemNone[start_i][start_j - 1] == 0) & (start_j - 1 >= 0)):
                                            neubors.append(
                                                [[start_i, start_j - 1], 1, iter_index,
                                                 shem_on_clNone[start_i][start_j - 1].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №1')
                                    try:
                                        if (r2 not in temp_data_neub) & (
                                                (shemNone[start_i][start_j + 1] == 0) & (start_j + 1 <= len(shemNone[start_i]))):
                                            neubors.append(
                                                [[start_i, start_j + 1], 1, iter_index,
                                                 shem_on_clNone[start_i][start_j + 1].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №2')
                                    try:
                                        if (r3 not in temp_data_neub) & (
                                                (shemNone[start_i + 1][start_j] == 0) & (start_i + 1 <= len(shemNone))):
                                            neubors.append(
                                                [[start_i + 1, start_j], 1, iter_index,
                                                 shem_on_clNone[start_i + 1][start_j].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №3')
                                    try:
                                        if (r4 not in temp_data_neub) & (
                                                (shemNone[start_i - 1][start_j] == 0) & (start_i - 1 >= 0)):
                                            neubors.append(
                                                [[start_i - 1, start_j], 1, 0,
                                                 shem_on_clNone[start_i - 1][start_j].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №4')
                                    try:
                                        if (l1 not in temp_data_neub) & (
                                                (shemNone[start_i - 1][start_j + 1] == 0) & (start_i - 1 >= 0) & (
                                                start_j + 1 <= len(shemNone[start_i]))):
                                            neubors.append([[start_i - 1, start_j + 1], 1, iter_index,
                                                            shem_on_clNone[start_i - 1][start_j + 1].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №5')
                                    try:
                                        if (l2 not in temp_data_neub) & (
                                                (shemNone[start_i - 1][start_j - 1] == 0) & (start_i - 1 >= 0) & (
                                                start_j - 1 >= 0)):
                                            neubors.append([[start_i - 1, start_j - 1], 1, iter_index,
                                                            shem_on_clNone[start_i - 1][start_j - 1].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №6')
                                    try:
                                        if (l3 not in temp_data_neub) & (
                                                (shemNone[start_i + 1][start_j + 1] == 0) & (start_i + 1 <= len(shemNone)) & (
                                                start_j + 1 <= len(shemNone[start_i]))):
                                            neubors.append([[start_i + 1, start_j + 1], 1, iter_index,
                                                            shem_on_clNone[start_i + 1][start_j + 1].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №7')
                                    try:
                                        if (l4 not in temp_data_neub) & (
                                                (shemNone[start_i + 1][start_j - 1] == 0) & (start_i + 1 <= len(shemNone)) & (
                                                start_j - 1 >= 0)):
                                            neubors.append([[start_i + 1, start_j - 1], 1, iter_index,
                                                            shem_on_clNone[start_i + 1][start_j - 1].status])
                                    except IndexError:
                                        pass  # print('Ошибка индекса №8')
                                    break
                                else:
                                    neubor_index += 1

                            if (neubor_index == len(neubors)) & (count_m > 0):
                                self.groupposadkaNone(status_group.get(key)[replay_index:], organisation, shemNone, shem_on_clNone)
                                break

                else:
                    # print('Происходит смена статусов так как мест для ', key, 'не осталось')
                    spisok = status_group.get(key)[replay_index:]
                    if key == 'doclad':
                        for record in spisok:
                            record[4] = 'gost'
                    elif key == 'gost':
                        for record in spisok:
                            record[4] = 'doclad'
                    # print('Измененные статусы в списке: ', spisok)
                    self.groupposadkaNone(spisok, organisation, shemNone, shem_on_clNone)


    def fullposadkaNone(self, user_id, name, status, organisation, shemNone, shem_on_clNone):
        check = self.checkDistNone(shem_on_clNone)
        person = Person(user_id, name, status, organisation)
        # print(person.name, person.status)
        full_list = []
        for num_ryad, ryad in enumerate(shem_on_clNone):
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
                if (mesto.status == person.status) & (shemNone[num_ryad][num] == 0):
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
            shemNone[k1][k2] = [person, sort_full_list[0][2].number]

    # Функция рассадки
    def posadkaNone(self, user_id, name, status, organisation, shemNone, shem_on_clNone):
        if (status == '') | (status == None):
            status = 'gost'

        check = self.checkDistNone(shem_on_clNone)
        person = Person(user_id, name, status, organisation)
        excellent = False
        # Цикл прохода по рядам
        # for i in shemNone:
        #     for j in i:
        #         try:
        #             print(j.status)
        #         except:
        #             pass
        for num_ryad, ryad in enumerate(shem_on_clNone):
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
                if (mesto.status == person.status) & (shemNone[num_ryad][num] == 0):
                    # Расчитываем индексы удаленности от краев start и end и расчитываем максимальный приоритет
                    left_index = abs(start - num)
                    right_index = abs(end - num)
                    max_priority = min(left_index, right_index)
                    priority_list.append([num, mesto, max_priority])

            # Сортируем лист приоритетов
            sort_list = sorted(priority_list, key=lambda item: item[2])

            if len(sort_list) != 0:
                k = sort_list[0][0]
                shemNone[num_ryad][k] = [person, sort_list[0][1].number]
                excellent = True

                break

        if not excellent:
            if self.check_place(self.shemNone) != 0:
                if status == 'gost':
                    new_status = 'doclad'
                    # print(f'Места для {status} закончились, Вас посадят на место {new_status}')
                    self.posadkaNone(user_id, name, new_status, organisation, shemNone, shem_on_clNone)

                elif status == 'doclad':
                    new_status = 'gost'
                    # print(f'Места для {status} закончились, Вас посадят на место {new_status}')
                    self.fullposadkaNone(user_id, name, new_status, organisation, shemNone, shem_on_clNone)
            else:
                pass  # print('Мест больше нет')

    # Функция поиска
    def search(self, gen_shemNone, elem):
        temp = []
        for i, row in enumerate(gen_shemNone):
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


    # Функция поиска по id
    def search_id(self, gen_shemNone, user_id):
        ret = []
        section = 1
        for i, row in enumerate(gen_shemNone):
            for j, col in enumerate(row):
                if col is not None:
                    try:
                        if int(col[0].user_id) == int(user_id):
                            ret.append([{'row_user': i + 1, 'col_user': j + 1, 'section': section}])
                            return ret
                        else:
                            continue
                    except TypeError:
                        continue
                else:
                    section += 1
                    continue
        return ret



    # Функция построения графика рассадки в svg
    def create_imgsvg(self, shemNone, shem_on_clNone, name_img, rotRect=5, rotRectChange=5, bias=3, biasChange=3, x_dist=35,
                      y_dist=50, x_startBias=2, color_organisation=False, highliter=None):

        count_in_str = len(shemNone[0])
        count_in_col = len(shemNone)
        dwg = svgwrite.Drawing(str(name_img)+'.svg', profile='tiny', viewBox=(
                '0 0 ' + str(count_in_str * (x_dist + 1)) + ' ' + str((count_in_col + 1) * (y_dist + 1))))
        listflang = self.checkDistNone(shemNone)

        if len(listflang[0]) >= 3:
            multi = len(listflang[0]) - 2
        else:
            multi = 1
            rotRect = 0
            rotRectChange = 0

        rotRect = rotRect / 2 * multi

        # Для окраски организаций
        org = {}
        if color_organisation is True:
            for r in shemNone:
                for c in r:
                    if c != None:
                        try:
                            org.setdefault(c[0].organisation, c[0].organisation)
                            org[c[0].organisation] = (
                                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        except TypeError:
                            continue
        else:
            for r in shemNone:
                for c in r:
                    if c != None:
                        try:
                            org.setdefault(c[0].organisation, c[0].organisation)
                            org[c[0].organisation] = (255, 165, 0)
                        except TypeError:
                            continue

        for i, row in enumerate(shemNone):
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
                            if highliter is None:
                                dwg.add(dwg.rect((x_pix + x_startBias, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2',
                                                 fill='rgb' + str(org.get(col[0].organisation)), stroke_width=1.5,
                                                 stroke='black',
                                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                           str(35 // 2 + y_pix + 10) + ')'))
                                dwg.add(dwg.rect((x_pix + x_startBias, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2',
                                                 fill='rgb' + str(org.get(col[0].organisation)), stroke_width=1.5,
                                                 stroke='black',
                                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                           str(35 // 2 + y_pix + 10) + ')'))
                                dwg.add(
                                    dwg.text(str(col[1]),
                                             insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                             font_size='8', fill='green', font_weight='bold'))

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
                                                 font_size=str(
                                                     sizePx(name_sp[1] + ' ' + name_sp[2], base_px, upp=False)),
                                                 fill='black'))
                            else:
                                if shemNone[i][j][0].user_id == highliter:
                                    dwg.add(dwg.rect((x_pix + x_startBias, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2',
                                                     fill='rgb(6, 147, 186)', stroke_width=1.5,
                                                     stroke='black',
                                                     transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                               str(35 // 2 + y_pix + 10) + ')'))
                                    dwg.add(dwg.rect((x_pix + x_startBias, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2',
                                                     fill='rgb(6, 147, 186)', stroke_width=1.5,
                                                     stroke='black',
                                                     transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                               str(35 // 2 + y_pix + 10) + ')'))
                                    dwg.add(
                                        dwg.text(str(col[1]),
                                                 insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                                 font_size='8', fill='green', font_weight='bold'))

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
                                                     font_size=str(
                                                         sizePx(name_sp[1] + ' ' + name_sp[2], base_px, upp=False)),
                                                     fill='black'))
                                else:
                                    dwg.add(
                                        dwg.rect((x_pix + x_startBias, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2',
                                                 fill='rgb' + str(org.get(col[0].organisation)), stroke_width=1.5,
                                                 stroke='black',
                                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                           str(35 // 2 + y_pix + 10) + ')'))
                                    dwg.add(
                                        dwg.rect((x_pix + x_startBias, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2',
                                                 fill='rgb' + str(org.get(col[0].organisation)), stroke_width=1.5,
                                                 stroke='black',
                                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                                           str(35 // 2 + y_pix + 10) + ')'))
                                    dwg.add(
                                        dwg.text(str(col[1]),
                                                 insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                                 font_size='8', fill='green', font_weight='bold'))

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
                                    dwg.add(
                                        dwg.text(name_sp[1] + ' ' + name_sp[2], insert=(x_pix + 3, y_pix + 28 - bias_y),
                                                 font_size=str(
                                                     sizePx(name_sp[1] + ' ' + name_sp[2], base_px, upp=False)),
                                                 fill='black'))
                        except IndexError:
                            dwg.add(
                                dwg.text(str(col[0].organisation), insert=(x_pix + 3, y_pix + 18 - bias_y),
                                         font_size="5px",
                                         fill='black',
                                         font_weight='bold'))
                            dwg.add(
                                dwg.text(name[0], insert=(x_pix + x_startBias + 1, y_pix - bias_y), font_size="6px",
                                         fill='black', font_weight='bold'))
                            dwg.add(
                                dwg.text(str(col[1]),
                                         insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
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

                    number_len = len(str(shem_on_clNone[i][j].number)) * 2
                    dwg.add(
                        dwg.rect((x_pix + 2, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2', fill='rgb(179, 179, 179)',
                                 stroke_width=1.5,
                                 stroke='black',
                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                           str(35 // 2 + y_pix + 10) + ')'))
                    dwg.add(
                        dwg.rect((x_pix + 2, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2', fill='rgb(179, 179, 179)',
                                 stroke_width=1.5,
                                 stroke='black',
                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                           str(35 // 2 + y_pix + 10) + ')'))
                    dwg.add(
                        dwg.text(shem_on_clNone[i][j].number,
                                 insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
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

                    number_len = len(str(shem_on_clNone[i][j].number)) * 2
                    dwg.add(
                        dwg.rect((x_pix + 2, y_pix + 10 - bias_y), (35, 35), rx='2', ry='2', fill='white',
                                 stroke_width=1.5,
                                 stroke='black',
                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                           str(35 // 2 + y_pix + 10) + ')'))
                    dwg.add(
                        dwg.rect((x_pix + 2, y_pix + 35 - bias_y), (35, 10), rx='2', ry='2', fill='white',
                                 stroke_width=1.5,
                                 stroke='black',
                                 transform='rotate(' + str(rot) + ',' + str(35 // 2 + x_pix + 2) + ',' +
                                           str(35 // 2 + y_pix + 10) + ')'))
                    dwg.add(
                        dwg.text(shem_on_clNone[i][j].number,
                                 insert=(x_pix + 20 - number_len - (rot // 2), y_pix + 43 - bias_y),
                                 font_size="8px", fill='black', font_weight='bold'))
        dwg.save()

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


# Результат рассадки на отправку (список)
def resp_data(shemNone):
    export_data = []
    for i, row in enumerate(shemNone):
        for j, col in enumerate(row):
            if col is not None:
                try:
                    export_data.append([col[0].user_id, col[0].name, i + 1, j + 1, col[1]])
                except TypeError:
                    pass
    return export_data


# Результат рассадки на отправку (json) - json.dumps
# def json_ser(export_data):
#     return json.dumps({data[0]: {'name': data[1],
#                                  'row': data[2],
#                                  'place_in_row': data[3],
#                                  'place_in_premise': data[4]} for data in export_data})


# # Результат рассадки на отправку (json) - jsonify
def json_ser(export_data):
    return jsonify({data[0]: {'name': data[1],
                                 'row': data[2],
                                 'place_in_row': data[3],
                                 'place_in_premise': data[4]} for data in export_data})




# Response(json.dumps(js),  mimetype='application/json')

# with closing(pymysql.connect(
#     host='localhost',
#     user='root',
#     password='',
#     db='ais',
#     charset='utf8mb4',
#                         )) as connection:
#
#     with connection.cursor() as cursor:
#         query = """
#         SELECT
#             *
#         FROM
#             users
#         """
#         cursor.execute(query)
#         for row in cursor:
#             print(row)


# social_distance = sys.argv[0]
# excel_import = sys.argv[1]
# mass_import = sys.argv[2]
# row_num = sys.argv[3]
# col_num = sys.argv[4]
#
# if __name__ == "__main__":
#     social_distance = False
#     excel_import = True
#     mass_import = []
#
#
#     if excel_import is True:
#         user_ex = imp_ex('База.xlsx', 'Лист1', 'A1', 'F302')
#         convert = convert_data(user_ex)
#         convert_LD = convert_list_dict(convert)
#     else:
#         user_ex = mass_import
#         convert_LD = convert_list_dict(user_ex)
#
#     prem = Premise(8, 29, space_col=[10, 21], space={7: list(range(22, 30))},
#                    doclad={
#                        0: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(range(22, 25)) + list(range(26, 30)),
#                        1: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(range(22, 25)) + list(range(26, 30)),
#                        2: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(range(22, 25)) + list(range(26, 30)),
#                    })
#
#     prem.gen_shemNone()
#
#     if social_distance is True:
#         prem.social_modify(prem.shemNone)
#     prem.gen_shem_on_clNone(prem.shemNone)
#
#
#     for i in convert_LD.keys():
#         if i is None:
#             continue
#         elif (str(i).lower() == 'default') | (len(convert_LD.get(i)) == 1):
#             for j in convert_LD.get(i):
#                 prem.posadkaNone(j[3], j[4], i, prem.shemNone, prem.shem_on_clNone)
#         else:
#             prem.groupposadkaNone(convert_LD.get(i), i, prem.shemNone, prem.shem_on_clNone)
#
#     prem.create_imgsvg(prem.shemNone, prem.shem_on_clNone, color_organisation=False)
