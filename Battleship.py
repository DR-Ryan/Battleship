import logging
import random
import time

logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class Player:
    len = 0
    letter = ''

    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
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
        orientation = raw_input('Select Orientation. V (Vertical) or H (Horizontal): ')
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
                            print('\nTwo ships are overlapping.\n')
                    elif orientation.upper() == 'H':
                        if self.location_check(row, col, length, orientation):
                            for i in range(0, length):
                                self.your_board[row][col + i] = letter
                                ship[(row, col + i)] = hit
                                placed = True
                        else:
                            print('\nTwo ships are overlapping.\n')
                    else:
                        print('\nOnly enter in V or H for the orientation.\n')
                except ValueError:
                    print('\nBoth coordinates should be numbers.\n')
                except IndexError:
                    print('\nYou placed the ship outside of the ocean.\n')
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
                    self.shots.append((guess_row, guess_col))
                    self.enemy_board[guess_row][guess_col] = 'X'
                    other.your_board[guess_row][guess_col] = 'X'
                    fire = True
                    for ship in other.ship_list:
                        if (guess_row, guess_col) in ship:
                            ship[(guess_row, guess_col)] = hit
                            # after ship hit add surrounding area (NSEW) to list of targets
                            self.targeting = True
                            self.targets.append([guess_row+1, guess_col])  # North
                            self.targets.append([guess_row-1, guess_col])  # South
                            self.targets.append([guess_row, guess_col+1])  # East
                            self.targets.append([guess_row, guess_col-1])  # West
                            print('\nShip has been hit!')
                            if all(i for i in ship.values()):
                                print('Ship has been sank!')
                                self.targeting = False
                                other.destroyed.append(ship)
                                if self.game_over(other.destroyed):
                                    return False
                            break
                    else:
                        pass
                        print('Miss!')
                else:
                    pass
                    print('You cannot fire at the same location twice.')
            except ValueError:
                print('\nCoordinates must be numbers!')
            except IndexError:
                print('\nShooting outside of the ocean!')

    def game_over(self, destroyed):
        if len(destroyed) == 5:
            print('\nGame Over!\n', self.name, 'Wins!')
            return True


class Computer(Player):

    # targeting modes
    def target(self):
        # if mode is easy use random targeting
        if self.mode == 1:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            return row, col
        # if mode is medium use targeting mode
        elif self.mode == 2:
            if self.targeting:
                loc = self.targets.pop()
                return loc[0], loc[1]
            else:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                return row, col
        # if mode is hard use even parity and targeting mode
        elif self.mode == 3:
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

        if self.mode == 3:
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
    # name1 = raw_input('Enter player1\'s name: ')
    # name2 = raw_input('Enter player2\'s name: ')
    mode = int(input('Select Difficulty\n(1)Easy\n(2)Medium\n(3)Hard\n(4)Extreme\n'))
    #
    # Player1 = player(name1, mode)
    # Player2 = computer(name2, mode)
    # Player1.place_ship()
    # Player2.place_ship()
    # while True:
    #     if Player1.shoot(Player2) == False:
    #         break
    #     if Player2.shoot(Player1) == False:
    #         break

    # Gathering information of the effectiveness of all random targeting approach, Yes I know it'll be terrible
    # Uncomment above code in main to play as well as the print statements in the class functions, they were slowing
    # down programming execution when running 100 of thousands of games

    start_time = time.time()
    name1 = 'C1'
    name2 = 'C2'
    computer1 = Computer(name1, mode)
    computer2 = Computer(name2, mode)
    turns = 0
    avg_turn = 0
    shortest_game = 101
    num_of_games = 10
    for i in range(0, num_of_games):
        computer1.place_ship()
        computer2.place_ship()
        while True:
            turns += 1
            if computer1.shoot(computer2) == False:
                computer1.reset()
                computer2.reset()
                avg_turn += turns
                if turns < shortest_game:
                    shortest_game = turns
                turns = 0
                break
            if computer2.shoot(computer1) == False:
                computer2.reset()
                computer1.reset()
                avg_turn += turns
                if turns < shortest_game:
                    shortest_game = turns
                turns = 0
                break
    logging.info("--- Number of games: %s ---" % num_of_games)
    logging.info("--- Took %s seconds to execute ---" % (time.time() - start_time))
    avg_turn /= num_of_games
    logging.info("--- avg amt of turns: %s ---" % avg_turn)
    logging.info("--- shortest game: %s ---" % shortest_game)


if __name__ == '__main__':
    main()
