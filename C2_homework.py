from random import randint

# COORD_EMPTY = ')'
# COORD_FAIL = 'T'
# COORD_HIT = 'X'
# COORD_SHIP = 'S'

#хранение данных о координатах в новом типе данных
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Coord ({self.x, self.y})"


# классы исключений
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return 'Point is out of board!'

class BoardUsedException(BoardException):
    def __str__(self):
        return 'Point already used!'

class BoardWrongShipException(BoardException):
    pass


#класс корабля
class WarShip:
    def __init__(self, bow, lenght, o):
        self.bow = bow
        self.lenght = lenght
        self.o = o
        self.lives = lenght                     #длинна корабля в клетках равна количеству жизней

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Coord(cur_x, cur_y))

        return ship_dots

    # стрелянные точки
    def shooten(self, shot):
        return shot in self.dots


#игровое поле
class Battleground:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.count = 0
        self.field = [ ['O'] * size for _ in range(size) ]
        self.busy = []
        self.warships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # запрет на установку кораблей рядом
    def ship_perimeter(self, ship, verb = False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:           #ship_dots - точки, в которых расположен корабль   **************
            for dx, dy in near:
                cur = Coord(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:                                          #if verb == True
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    #добавить корабль
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:  #если точка за пределами доски или уже занята - исключение
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"         #замена пустой точки в self.field из init на квадрат(часть корабля)
            self.busy.append(d)                #добавить в список занятых точек точку с частью корабля

        self.warships.append(ship)
        self.ship_perimeter(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)  #добавить стреляную точку в список занятых точек

        for ship in self.warships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.ship_perimeter(ship, verb = True)
                    print("Enemy`s ship was destroyed!")
                    return False
                else:
                    print("Enemy`s ship was injured!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Fail shot!")
        return False

    def beginning(self):
        self.busy = []


#базовый класс игрока
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def step(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class YourEnemy(Player):
    def ask(self):
        d = Coord(randint(0, 5), randint(0, 5))
        print(f"Enemy`s step: {d.x + 1} {d.y + 1}")
        return d

    def step(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat

            except BoardException as e:
                print(e)


class Human(Player):
    def ask(self):
        while True:
            points = input("Your time: ").split()
            if len(points) != 2:
                print("There must be only 2 points!")
                continue

            x, y = points

            if not (x.isdigit()) and not (y.isdigit()):
                print("Input digits!")
                continue

            x, y = int(x), int(y)

            return Coord(x-1, y-1)




class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.make_board()
        co = self.make_board()
        co.hid = True

        self.computer = YourEnemy(co, pl)
        self.admin = Human(pl, co)

    def make_board(self):
        board = None
        while board is None:                              #цикл для гарантированного создания доски
            board = self.try_board()
        return board

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Battleground(size = self.size)
        attempts = 0
        for lenght in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = WarShip(Coord(randint(0, self.size), randint(0, self.size)), lenght, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.beginning()
        return board

    def intro(self):
        print("Морской бой. Формат ввода: x y:")
        print(" x - номер строки")
        print(" y - номер столбца")

    def game_logic(self):
        num = 0
        while True:
            print("-" * 20)
            print("Human:")
            print(self.admin.board)
            print("-" * 20)
            print("Computer:")
            print(self.computer.board)
            print("-" * 20)

            if num % 2 == 0:
                print("Time of Human.")
                repeat = self.admin.step()
            else:
                print("Time of Your Enemy.")
                repeat = self.computer.step()


            if repeat:
                num -= 1

            if self.computer.board.count == 7:
                print("You Win!")
                break

            if self.admin.board.count == 7:
                print("Your Enemy Wins!")
                break
            num += 1

    def start(self):
        self.intro()
        self.game_logic()


g = Game()
g.start()





# if __name__ = '__main__':
