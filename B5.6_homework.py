#сообщения для игроков перед началом игры
def intro():
    print('Игра "крестики - нолики".')
    print("Вводите координаты клеток, которые выбираете для своего хода.")
    print("Координаты нужно вводить в формате двух цифр через пробел в соответствии номеру столбца и строки.")
    print()

#ячейки для хранения прогресса игры
field = [[' ', ' ', ' '] for i in range(3)]

#построение игрового поля
def gamespace():
    print('---------------')
    print(f'* | 0 | 1 | 2 |')
    print('---------------')
    for i in range(3):
        print(f'{i} | {field[i][0]} | {field[i][1]} | {field[i][2]} |')
        print('---------------')
    print()

#ввод и проверка координат ячеек
def input_coords():
    while True:
        coords = input('Введите координаты: ').split()

        if len(coords) != 2:
            print('Введите только два значения координат!!!1')
            continue

        string, coll = coords

        if string.isalpha() or coll.isalpha():
            print('Нужно вести цифры!!!1')
            continue

        string, coll = int(string), int(coll)

        if 0 <= coll <= 2 and 0 <= string <= 2:
            if field[coll][string] == ' ':
                return coll, string
            else:
                print('Ячейка занята, повторите ввод!!!1')
        else:
            print('Введите корректные координаты!!!1')

#комбинации для победы в игре
def get_winner():
    if field[coll][0] == field[coll][1] == field[coll][2] != ' ':
        print(f'Победил "{field[coll][0]}"!!!1')
        return True

    elif field[0][string] == field[1][string] == field[2][string] != ' ':
        print(f'Победил "{field[0][string]}"!!!1')
        return True

    elif field[0][0] == field[1][1] == field[2][2] != ' ':
        print(f'Победил "{field[0][0]}"!!!1')
        return True

    elif field[0][2] == field[1][1] == field[2][0] != ' ':
        print(f'Победил "{field[0][2]}"!!!1')
        return True

    return False


#старт игры отсюда
intro()

steps = 0
while True:
    steps += 1

    gamespace()

    if steps % 2 == 0:
        print('Ходит "0"')
    else:
        print('Ходит "Х"')

    coll, string = input_coords()

    if steps % 2 == 0:
        field[coll][string] = 'O'
    else:
        field[coll][string] = 'X'

    if get_winner():
        break

    if steps == 9:
        print('^^^^^^^^^')
        print('Try again!!!1')
        break

