from random import randint


# Создаем собственные классы исключений
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Выбранная клетка находится за пределами игрового поля!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "В эту клетку выстрел уже производился!"


class BoardWrongShipException(BoardException):
    pass


# Создаем класс точки
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


# Создаем класс корабля
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow # начальная координата
        self.l = l # длина корабля
        self.o = o # ориентация корабля на игровом поле
        self.lives = l

    @ property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


# создаем класс доски
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0 # количество пораженных кораблей
        self.field = [["\033[36m\u2022\033[0m"] * size for _ in range(size)] # заполнение поля
        self.busy = [] # занятые клетки
        self.ships = [] # список кораблей

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |" + "\n---------------------------"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |" + "\n---------------------------"

        if self.hid:
            res = res.replace("\u25a0", "\033[36m\u2022\033[0m") # сокрытие кораблей противника
        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "\033[32m\033[1m\u29DB\033[0m" # контуры корабля
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in ship.dots:
            self.field[d.x][d.y] = "\033[30m\u25a0\033[0m" # символ корабля
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Стрельба по доске
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "\033[31m\033[1mX\033[0m" # попадание
                if ship.lives == 0:
                    self.contour(ship, verb=True)
                    self.count += 1
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль поврежден!")
                    return True

        self.field[d.x][d.y] = "\033[33m\033[1mT\033[0m" # промах
        print("Промах!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


# Создаем класс "Игрок"
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


# Создаем класс "игрок-компьютер"
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход противника: {d.x + 1} {d.y + 1}")
        return d


# Создаем класс "игрок-пользователь"
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Введите две координаты!")
                continue

            x, y = cords
            if not(x.isdigit()) or not(y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


# Создаем класс "Игра"
class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        # Приветствие
        print("\033[1m\033[3m--------------------")
        print("  Добро пожаловать  ")
        print("       в игру       ")
        print("   \"Морской бой\"")
        print("--------------------\033[0m")
        print("Формат ввода: x y")
        print("x - номер строки")
        print("y - номер столбца")
        print("--------------------")
        print("Игровые обозначения: ")
        print("\033[36m\u2022\033[0m - значок заполнения поля")
        print("\033[30m\u25a0\033[0m - значок корабля")
        print("\033[31m\033[1mX\033[0m - попадание")
        print("\033[33m\033[1mT\033[0m - промах")
        print("\033[32m\033[1m\u29DB\033[0m - контуры корабля")
        print("--------------------")
        print("\033[1m    \033[4mПравила игры\033[0m")
        print()
        print(''' \033[3mВ случае промаха или
 уничтожения корабля
 право хода переходит
к противнику. В случае
 повреждения корабля 
следует дополнительный
        ход.\033[0m''')

    def print_boards(self):
        print("-" * 20)
        print()
        print("Ваше игровое поле: ")
        print()
        print(self.us.board)
        print("-" * 20)
        print()
        print("Игровое поле противника: ")
        print()
        print(self.ai.board)
        print("-" * 20)

    # Игровой цикл
    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("Орудия к бою!")
                repeat = self.us.move()

            else:
                print("Противник наводит орудия! ")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("Вы выиграли!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("Ваш противник выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()

