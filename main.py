import datetime
from datetime import timedelta
import time
from time import sleep
import pygame
import re

pygame.mixer.init()
ding = pygame.mixer.Sound("dingdong.wav")  # инициализация звука


def time_check():  # функция ввода времени
    while True:
        t = input("Время будильника: ")
        t, valid = check_valid_time(t)  # проверка на ошибки
        if valid == False:
            continue  # создает луп
        return t  # ломает луп


def check_valid_time(t):  # фукнция проверки на ошибки
    timeRe = r"\d{2}\:\d{2}"  # формат ввода 2 цифры : 2 цифры
    try:  # на случай ввода 9:20 а не 09:20
        if t[0] != 0 and t[1] == ":":
            t = "0" + t
            return t, check_valid_time(t)[1]  # перепроверить формат ввода
        else:
            return t, re.findall(timeRe, t)[0] == t  # если все в порядке возвращает время
    except:
        return None, False


def current_time(FMT="%H:%M"):  # FMT формат ввода %H - часы %M - минуты, функция настоящего времени
    t = datetime.datetime.now()
    return t.strftime(FMT)


def change_time(t):  # перевод времени в секунды
    t = datetime.datetime.strptime(t, "%H:%M")  # конвертирует в datetime объект
    return t.strftime("%H:%M:%S")  # конвертирует формат 14:30 в формат 14:30:00


def d_time(then, now, FMT="%H:%M:%S"):  # функция времени до будильника (СЕКУНДОМЕР)
    then = datetime.datetime.strptime(then, FMT)
    now = datetime.datetime.strptime(now, FMT)
    tdelta = then - now  # вычисление прошедшего времени
    if tdelta.days < 0:  # проверка на ошибку, когда дней меньше 0
        tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    return tdelta


def alarm(t, FMT="%H:%M:%S"):  # main функция
    while True:
        info = f"Настоящее время: {current_time(FMT)}, Время до будильника: {(d_time(change_time(t), current_time(FMT), FMT))}"
        for idx in range(10):
            print('\r', info, end='')
        if current_time(FMT) == change_time(t):
            ding.play(-1)


if __name__ == "__main__":  # инициализация запуска
    alarm(time_check())
