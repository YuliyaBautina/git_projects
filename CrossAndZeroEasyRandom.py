import random
# Приветствие
print("--------------------")
print("  Добро пожаловать  ")
print("       в игру       ")
print(" \"Крестики-нолики\"")
print("--------------------")

# Создание игрового поля
field = [[" "] * 3 for i in range(3)]

# Вывод игрового поля на печать
def show():
    print()
    print("   Игровое поле")
    print()
    print(f"  | 0 | 1 | 2 |")
    print(" --------------")
    for i in range(3):
        row_info = " | ".join(field[i])
        print(f"{i} | {row_info} |")
        print(" --------------")


show()


def pl_turn():
    while True:
        print()
        coords = input("Ваш ход. Введите номер выбранных строки и столбца в формате x y: ").split()
        if len(coords) != 2:
            print("Введите две координаты выбранной клетки!")
            continue

        x, y = coords
        if not (x.isdigit()) or not (y.isdigit()):
            print("Координаты выбранной клетки поля должны быть целыми числами!")
            continue

        x, y = int(x), int(y)

        if 0 <= x <= 2 and 0 <= y <= 2:
            if field[x][y] == " ":
                field[x][y] = "x"
                return
            else:
                print("Выбранная клетка поля занята!")
        else:
            print("Некорректный номер клетки поля. Повторите ввод.")


def cpu_turn():
    cpu_list = [[0, 1, 2], [0, 1, 2]]
    while True:
        x = random.choice(cpu_list[0])
        y = random.choice(cpu_list[1])
        print()
        print(f"Ход противника. Выбранные координаты: {x} {y}")
        if field[x][y] == " ":
            field[x][y] = "0"
            return
        else:
            print("Выбранная клетка поля занята! Повторите ход!")


# Проверка выигрышного кода
def win_check():

    win_coord = [((0, 0), (0, 1), (0, 2)),
                 ((1, 0), (1, 1), (1, 2)),
                 ((2, 0), (2, 1), (2, 2)),
                 ((0, 2), (1, 1), (2, 0)),
                 ((0, 0), (1, 1), (2, 2)),
                 ((0, 0), (1, 0), (2, 0)),
                 ((0, 1), (1, 1), (2, 1)),
                 ((0, 2), (1, 2), (2, 2))]
    for coord in win_coord:
        a = coord[0]
        b = coord[1]
        c = coord[2]
        if field[a[0]][a[1]] == field[b[0]][b[1]] == field[c[0]][c[1]] != " ":
            print(f"Выиграл {field[a[0]][a[1]]}")
            if field[a[0]][a[1]] == "x":
                print("Вы победили!")

            elif field[a[0]][a[1]] == "0":
                print("Ваш противник победил!")

            return True
    return False


num = 0
while True:
    num += 1
    if num == 10:
        show()
        print("Ничья!")
        break
    elif num % 2 == 1:
        pl_turn()
        show()
        if win_check():
            break

    elif num % 2 == 0:
        cpu_turn()
        show()
        if win_check():
            break

