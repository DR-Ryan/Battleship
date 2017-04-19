import random
import time
import pygame

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
            # if self.mode == 1 and self.name == 'Computer':
            #     pass
            # else:
            #     self.print_board(self.your_board)


    def shoot(self, other):
        hit = True
        fire = False
        print(self.name, 'is shooting.')
        #self.print_board(self.enemy_board)
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






def visualized(Player, Other):
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (510, 255)
    width = 20
    height = 20

    # Set the margin of the screen
    margin = 5

# Set the grid up
    screen = pygame.display.set_mode(size)
    screen2 = pygame.display.set_mode(size)
    pygame.display.set_caption(Player.name)

    # Loop until the user clicks the close button.
    done = False

    # Variables to make BS work

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                m_col = pos[0] // (width + margin)
                m_row = pos[1] // (height + margin)
                if Player.enemy_board[m_row][m_col] == "~":
                    Player.enemy_board[m_row][m_col] = "0"
                else:
                    grid[m_row][m_col] = "X"
                print("Row: ", m_row , "Column: ", m_col)

        # --- Game logic should go here
        if Player.shoot(Other) == False:
            Player.reset()
            Other.reset()
            done = True
        if Other.shoot(Player) == False:
            Other.reset()
            Player.reset()
            done = True
        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
        screen2.fill(BLACK)
        color = WHITE
        # --- Drawing code should go here
        for column in range(0,10):
            for row in range(0,10):
                if Player.your_board[row][column] == "A" or Player.your_board[row][column] == "B" or \
                                Player.your_board[row][column] == "S" or Player.your_board[row][column] == "C" or\
                                Player.your_board[row][column] == "D":
                    color = GREEN
                elif Player.your_board[row][column] == 'O':
                    color = BLUE
                elif Player.your_board[row][column] == 'X':
                    color = RED
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, [260 + column * (width + margin),
                                                 margin + row * (height + margin),
                                                 width, height])
        for column in range(0, 10):
            for row in range(0, 10):
                if Player.enemy_board[row][column] == "A" or Player.enemy_board[row][column] == "B" or \
                    Player.enemy_board[row][column] == "S" or Player.enemy_board[row][column] == "C" or \
                    Player.enemy_board[row][column] == "D":
                    color = GREEN
                elif Player.enemy_board[row][column] == 'O':
                    color = BLUE
                elif Player.enemy_board[row][column] == 'X':
                    color = RED
                else:
                    color = WHITE
                pygame.draw.rect(screen2, color, [margin + column * (width + margin),
                                                 margin + row * (height + margin),
                                                 width, height])
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(30)
        time.sleep(1)
        # done = True
    # Close the window and quit.
    pygame.quit()


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
             visualized(Player1, Player2)
             # if Player1.shoot(Player2) == False:
             #     break
             # if Player2.shoot(Player1) == False:
             #     break
    elif mode == 2:
        name1 = 'Computer One'
        name2 = 'Computer Two'
        computer1 = Computer(name1, mode, difficulty)
        computer2 = Computer(name2, mode, difficulty)
        computer1.place_ship()
        computer2.place_ship()
        while True:
            visualized(computer1, computer2)
            # if computer1.shoot(computer2) == False:
            #     computer1.reset()
            #     computer2.reset()
            #     break
            # if computer2.shoot(computer1) == False:
            #     computer2.reset()
            #     computer1.reset()
            #     break
            # print("About to wait")
            break
    else:
        print('Bad input')

if __name__ == '__main__':
    main()