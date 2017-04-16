import random
import time

class Player:
    len = 0
    letter = ''

    def __init__(self, name, mode, difficulty):
        self.name = name
        self.mode = mode
        self.difficulty = difficulty
        self.aircraft_carrier = {}
        self.battleship = {}
        self.submarine = {}
        self.cruiser = {}
        self.destroyer = {}
        self.shots = []
        self.targets = []  # potential targets
        self.targeting = False  # computer targeting mode
        self.destroyed = []
        self.ship_list = [self.aircraft_carrier, self.battleship, self.submarine, self.cruiser, self.destroyer]
        self.your_board = [["~"] * 10 for i in range(0, 10)]
        self.enemy_board = [["~"] * 10 for i in range(0, 10)]

    @staticmethod
    def print_board(board):
        for i in board:
            print(' '.join(i))
        return board

    def to_be_placed(self, ship):
        length = 0
        letter = ''
        if ship == self.aircraft_carrier:
            print('\nPlacing ship of length 5')
            length = 5
            letter = 'A'
        elif ship == self.battleship:
            print('\nPlacing ship of length 4')
            length = 4
            letter = 'B'
        elif ship == self.submarine:
            print('\nPlacing ship of length 3')
            length = 3
            letter = 'S'
        elif ship == self.cruiser:
            print('\nPlacing ship of length 3')
            length = 3
            letter = 'C'
        elif ship == self.destroyer:
            print('\nPlacing ship of length 2')
            length = 2
            letter = 'D'
        return length, letter

    def target(self):
        row = int(input('Select Row Coordinate: '))
        col = int(input('Select Column Coordinate: '))
        return row, col

    def get_coordinates(self):
        orientation = input('Select Orientation. V (Vertical) or H (Horizontal): ')
        row, col = self.target()
        return orientation, row, col

    def location_check(self, row, col, length, orientation):
        if orientation.upper() == 'V':
            for i in range(0, length):
                if self.your_board[row + i][col] != '~':
                    return False
        elif orientation.upper() == 'H':
            for i in range(0, length):
                if self.your_board[row][col + i] != '~':
                    return False
        else:
            print('Orientation is Wrong!')
            return False
        return True

    def place_ship(self):
        for ship in self.ship_list:
            placed = False
            hit = False
            length, letter = self.to_be_placed(ship)
            while not placed:
                try:
                    orientation, row, col = self.get_coordinates()
                    if orientation.upper() == 'V':
                        if self.location_check(row, col, length, orientation):
                            for i in range(0, length):
                                self.your_board[row + i][col] = letter
                                ship[(row + i, col)] = hit
                                placed = True
                        else:
                            if self.mode == 1 and self.name == 'Computer':
                                pass
                            else:
                                print('\nTwo ships are overlapping.\n')
                    elif orientation.upper() == 'H':
                        if self.location_check(row, col, length, orientation):
                            for i in range(0, length):
                                self.your_board[row][col + i] = letter
                                ship[(row, col + i)] = hit
                                placed = True
                        else:
                            if self.mode == 1 and self.name == 'Computer':
                                pass
                            else:
                                print('\nTwo ships are overlapping.\n')
                    else:
                        print('\nOnly enter in V or H for the orientation.\n')
                except ValueError:
                    print('\nBoth coordinates should be numbers.\n')
                except IndexError:
                    if self.mode == 1 and self.name == 'Computer':
                        pass
                    else:
                        print('\nYou placed the ship outside of the ocean.\n')
            if self.mode == 1 and self.name == 'Computer':
                pass
            else:
                self.print_board(self.your_board)


    def shoot(self, other):
        hit = True
        fire = False
        print(self.name, 'is shooting.')
        self.print_board(self.enemy_board)
        while not fire:
            try:
                guess_row, guess_col = self.target()
                if (guess_row, guess_col) not in self.shots:
                    #if self.mode == 2:
                    #    time.sleep(1.5)
                    self.shots.append((guess_row, guess_col))
                    # self.enemy_board[guess_row][guess_col] = 'X'
                    # other.your_board[guess_row][guess_col] = 'X'
                    fire = True
                    for ship in other.ship_list:
                        if (guess_row, guess_col) in ship:
                            ship[(guess_row, guess_col)] = hit
                            self.enemy_board[guess_row][guess_col] = 'X'
                            other.your_board[guess_row][guess_col] = 'X'
                            # after ship hit add surrounding area (NSEW) to list of targets
                            self.targeting = True
                            if guess_row - 1 > -1:
                                self.targets.append([guess_row - 1, guess_col])  # North
                            if guess_row + 1 < 10:
                                self.targets.append([guess_row + 1, guess_col])  # South
                            if guess_col - 1 > -1:
                                self.targets.append([guess_row, guess_col - 1])  # East
                            if guess_col + 1 < 10:
                                self.targets.append([guess_row, guess_col + 1])  # West
                            print('\nShip has been hit!')
                            if all(i for i in ship.values()):
                                print('Ship has been sank!')
                                time.sleep(1.2)
                                other.destroyed.append(ship)
                                if self.game_over(other.destroyed):
                                    return False
                            break
                    else:
                        print('Miss!')
                        self.enemy_board[guess_row][guess_col] = 'O'
                        other.your_board[guess_row][guess_col] = 'O'
                else:
                    if self.mode == 2 or self.mode == 1 and self.name == 'Computer':
                        pass
                    else:
                        print('You cannot fire at the same location twice.')
            except ValueError:
                print('\nCoordinates must be numbers!')
            except IndexError:
                print('\nShooting outside of the ocean!')

    def game_over(self, destroyed):
        if len(destroyed) == 5:
            self.print_board(self.enemy_board)
            print("\nGame Over!\n" + self.name + " Wins!")
            return True


class Computer(Player):

    # targeting modes
    def target(self):
        # if mode is easy use random targeting
        if self.difficulty == 1:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            return row, col
        # if mode is medium use targeting mode
        elif self.difficulty == 2:
            if len(self.targets) == 0:
                self.targeting = False
            if self.targeting:
                loc = self.targets.pop()
                return loc[0], loc[1]
            else:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                return row, col
        # if mode is hard use even parity and targeting mode
        elif self.difficulty == 3:
            if len(self.targets) == 0:
                self.targeting = False
            if self.targeting:
                loc = self.targets.pop()
                return loc[0], loc[1]
            else:
                while True:
                    row = random.randint(0, 9)
                    col = random.randint(0, 9)
                    if (row + col) % 2 == 0:
                        return row, col

    # coordinates for boat placement
    def get_coordinates(self):
        if random.randint(0, 1) == 0:
            orientation = 'V'
        else:
            orientation = 'H'

        if self.difficulty == 3:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
        else:
            row, col = self.target()
        return orientation, row, col

    # clear board
    def reset(self):
        self.aircraft_carrier.clear()
        self.battleship.clear()
        self.submarine.clear()
        self.cruiser.clear()
        self.destroyer.clear()
        del self.shots[:]
        del self.destroyed[:]
        del self.ship_list[:]
        del self.your_board[:]
        del self.enemy_board[:]
        del self.targets[:]
        self.targeting = False
        self.ship_list = [self.aircraft_carrier, self.battleship, self.submarine, self.cruiser, self.destroyer]
        self.your_board = [["~"] * 10 for i in range(0, 10)]
        self.enemy_board = [["~"] * 10 for i in range(0, 10)]


def main():

    mode = int(input('(1) Human Vs AI \n(2) AI vs AI\n'))
    difficulty = int(input('Select Difficulty\n(1)Easy\n(2)Medium\n(3)Hard\n'))

    if mode == 1:
         name1 = input('Enter player1\'s name: ')
         name2 = 'Computer'
         Player1 = Player(name1, mode, difficulty)
         Player2 = Computer(name2, mode, difficulty)
         Player1.place_ship()
         Player2.place_ship()
         while True:
             if Player1.shoot(Player2) == False:
                 break
             if Player2.shoot(Player1) == False:
                 break
    elif mode == 2:
        name1 = 'Computer One'
        name2 = 'Computer Two'
        computer1 = Computer(name1, mode, difficulty)
        computer2 = Computer(name2, mode, difficulty)
        computer1.place_ship()
        computer2.place_ship()
        while True:
            if computer1.shoot(computer2) == False:
                computer1.reset()
                computer2.reset()
                break
            if computer2.shoot(computer1) == False:
                computer2.reset()
                computer1.reset()
                break
    else:
        ('Bad input')

if __name__ == '__main__':
    main()