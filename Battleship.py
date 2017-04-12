import logging
import random

logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class player:
    len = 0
    letter = ''

    def __init__(self, name):
        self.name = name
        self.aircraft_carrier = {}
        self.battleship = {}
        self.submarine = {}
        self.cruiser = {}
        self.destroyer = {}
        self.shots = []
        self.destroyed = []
        self.ship_list = [self.aircraft_carrier, self.battleship, self.submarine, self.cruiser, self.destroyer]
        self.your_board = [["~"] * 10 for i in range(0, 10)]
        self.enemy_board = [["~"] * 10 for i in range(0, 10)]

    def print_board(self, board):
        for i in board:
            print(' '.join(i))
            logging.info(' '.join(i))
        return board

    def to_be_placed(self, ship):
        if ship == self.aircraft_carrier:
            print('\nPlacing ship of length 5')
            logging.info('Placing ship of length 5')
            len = 5
            letter = 'A'
        elif ship == self.battleship:
            print('\nPlacing ship of length 4')
            logging.info('Placing ship of length 4')
            len = 4
            letter = 'B'
        elif ship == self.submarine:
            print('\nPlacing ship of length 3')
            logging.info('Placing ship of length 3')
            len = 3
            letter = 'S'
        elif ship == self.cruiser:
            print('\nPlacing ship of length 3')
            logging.info('Placing ship of length 3')
            len = 3
            letter = 'C'
        elif ship == self.destroyer:
            print('\nPlacing ship of length 2')
            logging.info('Placing ship of length 2')
            len = 2
            letter = 'D'
        logging.info(len)
        logging.info(letter)
        return (len, letter)

    def get_coordinates(self):
        orientation = input('Select orientation. V (Vertical) or H (Horizontal): ')
        row = int(input('Select Row Coordinate: '))
        col = int(input('Select Column Coordinate: '))
        return (orientation, row, col)

    def location_check(self,row, col, len, orientation):
        if orientation.upper() == 'V':
            for i in range(0, len):
                if self.your_board[row + i][col] != '~':
                    return False
        elif orientation.upper() == 'H':
            for i in range(0, len):
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
            len, letter = self.to_be_placed(ship)
            while placed == False:
                try:
                    orientation, row, col = self.get_coordinates()
                    if orientation.upper() == 'V':
                        if self.location_check(row, col, len, orientation) == True:
                            for i in range(0, len):
                                self.your_board[row + i][col] = letter
                                ship[(row + i, col)] = hit
                                placed = True
                        else:
                            print('\nTwo ships are overlapping.\n')
                    elif orientation.upper() == 'H':
                        if self.location_check(row, col, len, orientation) == True:
                            for i in range(0, len):
                                self.your_board[row][col + i] = letter
                                ship[(row,col + i)] = hit
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
        while fire == False:
            try:
                guess_row = int(input('Select Row coordinate: '))
                guess_col = int(input('Select Column coordinate: '))
                logging.info(guess_row)
                logging.info(guess_col)
                if (guess_row, guess_col) not in self.shots:
                    self.shots.append((guess_row, guess_col))
                    self.enemy_board[guess_row][guess_col] = 'X'
                    other.your_board[guess_row][guess_col] = 'X'
                    fire = True
                    for ship in other.ship_list:
                        if (guess_row, guess_col) in ship:
                            ship[(guess_row,guess_col)] = hit
                            print('\nShip has been hit!')
                            if all(i == True for i in ship.values()) == True:
                                print('Ship has been sank!')
                                logging.info('Ship has been sank!')
                                other.destroyed.append(ship)
                                if self.game_over(other.destroyed) == True:
                                    return False
                                else:
                                    break
                            else:
                                break
                    else:
                        print('Miss!')
                else:
                    logging.info('You cannot fire at the same location twice.')
                    print('You cannot fire at the same location twice.')
            except ValueError:
                print('\nCoordinates must be numbers!')
            except IndexError:
                print('\nShooting outside of the ocean!')

    def game_over(self, destroyed):
        if len(destroyed) == 5:
            print('\nGame Over!')
            print(self.name, 'Wins!')
            return True

class computer(player):

    def get_coordinates(self):
        if random.randint(0, 1) == 0:
            orientation = 'V'
        else:
            orientation = 'H'

        row = random.randint(0, 9)
        col = random.randint(0, 9)
        return (orientation, row, col)

def main():
    #name1 = input('Enter player1\'s name: ')
    name2 = input('Enter player2\'s name: ')
    #Player1 = player(name1)
    Player2 = computer(name2)
    # Player1.place_ship()
    Player2.place_ship()
    # while True:
    #     if Player1.shoot(Player2) == False:
    #         break
    #     if Player2.shoot(Player1) == False:
    #         break


if __name__ == '__main__':
    main()