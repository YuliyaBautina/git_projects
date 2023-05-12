# Приветствие
print("\033[1m\033[3m--------------------")
print("  Добро пожаловать  ")
print("       в игру       ")
print(" \"Крестики-нолики\"")
print("--------------------\033[0m")

# Создание игрового поля
field = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]


# Вывод игрового поля на печать
def show():
    print()
    print("   Игровое поле")
    print()
    print(f"   |   |   |   |")
    print(" ---------------")
    print(f"   | \033[32m{field[0]}\033[0m | \033[32m{field[1]}\033[0m | \033[32m{field[2]}\033[0m |")
    print(" ---------------")
    print(f"   | \033[32m{field[3]}\033[0m | \033[32m{field[4]}\033[0m | \033[32m{field[5]}\033[0m |")
    print(" ---------------")
    print(f"   | \033[32m{field[6]}\033[0m | \033[32m{field[7]}\033[0m | \033[32m{field[8]}\033[0m |")
    print(" ---------------")


show()


# Ход игрока
def pl_turn():
    while True:
        print()
        x = input("Ваш ход. Введите номер выбранной клетки поля от 1 до 9: ")

        if not (x.isdigit()):
            print("Номер выбранной клетки поля должен быть целым числом!")
            continue

        x = int(x)

        if 1 <= x <= 9:
            if field[x - 1] != "\033[36m0\033[0m" and field[x - 1] != "\033[31mX\033[0m":
                field[x - 1] = "\033[31mX\033[0m"
                return
            else:
                print("Выбранная клетка поля занята!")
        else:
            print("Номер выбранной клетки поля не должен быть больше 9 или меньше 1. Повторите ввод!")


# Определение выигрышных комбинаций
win_coord = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8],
             [0, 3, 6],
             [1, 4, 7],
             [2, 5, 8],
             [0, 4, 8],
             [2, 4, 6]]


# Проверка комбинаций компьютером
def cpu_check_line(sum_0, sum_x):
    step = ""
    for line in win_coord:
        o = 0
        x = 0
        for j in range(0, 3):
            if field[line[j]] == "\033[36m0\033[0m":
                o += 1
            if field[line[j]] == "\033[31mX\033[0m":
                x += 1

        if o == sum_0 and x == sum_x:
            for j in range(0, 3):
                if field[line[j]] != "\033[36m0\033[0m" and field[line[j]] != "\033[31mX\033[0m":
                    step = field[line[j]]
    return step


# Ход компьютера
def step_field(step):
    ind = field.index(step)
    field[ind] = "\033[36m0\033[0m"


# Выбор хода компьютером
def cpu_choice():
    step = ""

    # 1) центр пуст, то занимаем центр
    if field[4] != "\033[31mX\033[0m" and field[4] != "\033[36m0\033[0m":
        step = "5"

        # 2) если центр занят, то занимаем первую ячейку
    if step == "":
        if field[0] != "\033[31mX\033[0m" and field[0] != "\033[36m0\033[0m":
            step = "1"

            # 3) если на какой либо из победных линий 2 свои фигуры и 0 чужих - ставим
    if step == "":
        step = cpu_check_line(2, 0)

    # 4) если на какой либо из победных линий 2 чужие фигуры и 0 своих - ставим
    if step == "":
        step = cpu_check_line(0, 2)

        # 5) если 1 фигура своя и 0 чужих - ставим
    if step == "":
        step = cpu_check_line(1, 0)

    # 6) если 1 фигура чужая и 0 своих - ставим
    if step == "":
        step = cpu_check_line(0, 1)

    return step


# Проверка выигрышного кода
def win_check():
    win_coord = [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8],
                 [0, 3, 6],
                 [1, 4, 7],
                 [2, 5, 8],
                 [0, 4, 8],
                 [2, 4, 6]]
    for coord in win_coord:
        a = coord[0]
        b = coord[1]
        c = coord[2]
        if field[a] == field[b] == field[c] == "\033[31mX\033[0m":
            print(f"Выиграл {field[a]}")
            print("Вы победили!")
            return True

        elif field[a] == field[b] == field[c] == "\033[36m0\033[0m":
            print(f"Выиграл {field[a]}")
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
        step = cpu_choice()
        if step != "":
            step_field(step)
            print()
            print(f"Ход компьютера. Номер выбранной клетки поля: {step}")
        show()
        if win_check():
            break
