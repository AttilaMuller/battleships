import string
import random
import os
import time

'''Messages'''
carrier = "Deploy your carrier!"
battleship = "Deploy your battleship!"
cruiser = "Deploy your cruiser!"
submarine = "Deploy your submarine!"
destroyer = "Deploy your destroyer!"

'''Player Data'''
carrier1 = []
battleship1 = []
cruiser1 = []
submarine1 = []
destroyer1 = []
p1ships = [carrier1, battleship1, cruiser1, submarine1, destroyer1]
p1usedspace = []
p1attacklist = []
p1hitlist = []

'''Coordinates'''
row = [[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
       [0.1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1],
       [0.2, 1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2],
       [0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3, 9.3],
       [0.4, 1.4, 2.4, 3.4, 4.4, 5.4, 6.4, 7.4, 8.4, 9.4],
       [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5],
       [0.6, 1.6, 2.6, 3.6, 4.6, 5.6, 6.6, 7.6, 8.6, 9.6],
       [0.7, 1.7, 2.7, 3.7, 4.7, 5.7, 6.7, 7.7, 8.7, 9.7],
       [0.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8],
       [0.9, 1.9, 2.9, 3.9, 4.9, 5.9, 6.9, 7.9, 8.9, 9.9]]


'''Ships'''
carrierc = []
battleshipc = []
cruiserc = []
submarinec = []
destroyerc = []
computer_ships = [carrierc, battleshipc, cruiserc, submarinec, destroyerc]
computer_usedspace = []
computerattacklist = []
computerhitlist = []
ailasthit = False
aihitstreak = []


def main():

    '''Game start'''
    clear_board()
    print("Welcome to Battleship!\n"
          "User interaction is by typing in coordinates, with lowercase letters, like this: 'a1' or\n"
          "'g10'. First, each player will place their ships one by one on the ocean by deciding\n"
          "to place them horizontally or vertically and entering a starting coordinate, like this:\n"
          "Vertical placement:\n"
          "▨ <- Starting point\n"
          "▨\n"
          "▨\n"
          "▨\n"
          "Horizontal placement:\n"
          "Starting point -> ▨ ▨ ▨ ▨"
          "\n")
    input("Press Enter to continue")
    clear_board()

    '''Player places ships'''
    print("Player 1, choose the coordinates for your fleet!)")
    print_table(p1usedspace)
    print(carrier)
    create_ship(carrier1, 5, p1usedspace)
    print(battleship)
    create_ship(battleship1, 4, p1usedspace)
    print(cruiser)
    create_ship(cruiser1, 3, p1usedspace)
    print(submarine)
    create_ship(submarine1, 3, p1usedspace)
    print(destroyer)
    create_ship(destroyer1, 2, p1usedspace)

    '''AI places ships'''
    computer_create_ship(carrierc, 5, computer_usedspace)
    computer_create_ship(battleshipc, 4, computer_usedspace)
    computer_create_ship(cruiserc, 3, computer_usedspace)
    computer_create_ship(submarinec, 3, computer_usedspace)
    computer_create_ship(destroyerc, 2, computer_usedspace)

    '''Changing turns'''
    while not check_gameover():
        p1_attack()
        if check_gameover():
            break
        ai_attack(aihitstreak)


def convert_input(i):
    ''' Convert user input into floating-point coordinates '''
    a = string.ascii_lowercase.index(i[0])
    b = float(i[1:]) / 10 - 0.1
    c = round((a + b), 1)
    return c


def clear_board():
    ''' Clear the terminal '''
    os.system('clear')


def check_ocean(horizon, coordinate, length):
    ''' Check if a ship with certain length could be fitted on the board
    with given starting coordinates
    '''
    try:
        if isinstance(coordinate, str):
            f = string.ascii_lowercase.index(coordinate[0])
            s = float(coordinate[1:]) - 1
        else:
            f = int(coordinate)
            s = (coordinate - f) * 10
        if horizon == "h" and f + length > 10 or f > 9:
            return False
        elif horizon == "v" and s + length > 10 or s > 9:
            return False
        else:
            return True
    except BaseException:
        return False


def check_usedspace(ship, used_space, length, a, b):
    ''' Check if the new ship's coordinates are already in use, if they are not,
    append them to the new ship's list and used coordinates list
    '''
    if isinstance(b, str):
        b = convert_input(b)
    ship.append(round(b, 1))
    for i in range(1, length):
        if a == "h":
            ship.append(round((b + i), 1))
        else:
            ship.append(round((b + i * 0.1), 1))
    g = list(set(ship) & set(used_space))
    if not g:
        used_space.append(round(b, 1))
        for i in range(1, length):
            if a == "h":
                used_space.append(round((b + i), 1))
            else:
                used_space.append(round((b + i * 0.1), 1))
        return True
    else:
        while ship:
            for i in ship:
                ship.remove(i)
        return False


def computer_create_ship(ship, length, used_space):
    ''' Create ship for the computer.

    Arguments:
    ship -- an empty list, where the coordinates will be appended
    length -- the number of coordinates generated for each ship
    used_space -- list of coordinates where the computer already has ships to avoid collision
    '''
    horizon = ['h', 'v']
    a = random.choice(horizon)
    b = random.randrange(10) + random.randrange(10) / 10
    while not check_ocean(a, b, length) or not check_usedspace(ship, used_space, length, a, b):
        b = random.randrange(10) + random.randrange(10) / 10


def check_horizon(a):
    ''' Check if the player has given valid input for ship alignment. '''
    if a == "v" or a == "h":
        return True
    else:
        return False


def create_ship(ship, length, used_space):
    ''' Create ship for the player.

    Arguments:
    ship -- an empty list, where the coordinates will be appended
    length -- the number of coordinates generated for each ship
    used_space -- list of coordinates where player already has ships to avoid collision
    '''
    a = input("It is " + str(length) + " units long. Enter 'h' to place it "
              "horizontally or 'v' to place it vertically: ")
    while not check_horizon(a):
        a = input("Enter 'h' to place it horizontally or 'v' to place it vertically: ")
    b = input("Give the starting coordinates. Your ship will be placed accordingly: ")
    while not check_ocean(a, b, length) or not check_usedspace(ship, used_space, length, a, b):
        b = input("The ocean is big, but not THAT big. Give other coordinates: ")
    clear_board()
    print_table(used_space)


def p1_attack():
    ''' Ask the user for attack coordinates, calculate the attack, notify user about success '''
    clear_board()
    print("Player 1 board:")
    print_board(p1hitlist, p1attacklist)
    hit = 0
    attack = input("Player 1 shoots at: ")
    while not check_ocean("v", attack, 0) or convert_input(
            attack) in p1attacklist or convert_input(attack) in p1hitlist:
        attack = input("Invalid input - Player 1 shoots at: ")
    attack = convert_input(attack)
    for s in computer_ships:
        if attack in s:
            clear_board()
            print("Hit!")
            s.remove(attack)
            p1hitlist.append(attack)
            hit = 1
            print_board(p1hitlist, p1attacklist)
            time.sleep(3)
        if not s:
            computer_ships.remove(s)
            print("Player 1 destroyed a ship!")
            time.sleep(3)
    if hit == 0:
        clear_board()
        print("Miss!")
        p1attacklist.append(attack)
        print_board(p1hitlist, p1attacklist)
        time.sleep(3)
    if not computer_ships:
        clear_board()
        print("Player one has won!")
        print_board(p1hitlist, p1attacklist)
        time.sleep(3)


def ai_attack(aihitstreak):
    ''' Random attack coordinates until find ship, try to guess and sink ship until ship
    is destroyed, then start again

    aihitstreak -- the list of coordinates where the AI last hit a ship,
    if ship is destroyed, list is emptied
    '''
    clear_board()
    global ailasthit
    hit = False
    if not aihitstreak:
        attack = random.randrange(10) + random.randrange(10) / 10
        while attack in computerhitlist or attack in computerattacklist:
            attack = random.randrange(10) + random.randrange(10) / 10
    elif len(aihitstreak) == 1:
        if (
            round(
                aihitstreak[0] - 0.1,
                1) not in computerattacklist and round(
                (aihitstreak[0] - 0.1) % 1,
                1) != 0.9 and round(
                aihitstreak[0] - 0.1,
                1) not in computerhitlist):
            attack = aihitstreak[0] - 0.1
        elif ((aihitstreak[0] + 1) < 10 and (aihitstreak[0] + 1) not in computerattacklist and
              (aihitstreak[0] + 1) not in computerhitlist):
            attack = aihitstreak[0] + 1
        elif ((aihitstreak[0] + 0.1) % 1 != 0 and (aihitstreak[0] + 0.1) not in computerattacklist and
              (aihitstreak[0] + 0.1) not in computerhitlist):
            attack = aihitstreak[0] + 0.1
        elif ((aihitstreak[0] - 1) > 0 and (aihitstreak[0] - 1) not in computerattacklist and
              (aihitstreak[0] - 1) not in computerhitlist):
            attack = aihitstreak[0] - 1
    elif len(aihitstreak) > 1:
        if ailasthit:
            if round(aihitstreak[0] - aihitstreak[1], 1) == -0.1:
                attack = round(aihitstreak[-1] + 0.1, 1)
                guessnextmove = round(attack + 0.1)
            elif round(aihitstreak[0] - aihitstreak[1], 1) == 1:
                attack = round(aihitstreak[-1] - 1, 1)
                guessnextmove = round(attack - 1, 1)
            elif round(aihitstreak[0] - aihitstreak[1], 1) == 0.1:
                attack = round(aihitstreak[-1] - 0.1, 1)
                guessnextmove = round(attack - 0.1, 1)
            elif round(aihitstreak[0] - aihitstreak[1], 1) == -1:
                attack = round(aihitstreak[-1] + 1, 1)
                guessnextmove = round(attack + 1, 1)
            if (guessnextmove < 0 or guessnextmove > 9.9 or guessnextmove in computerattacklist or
                    guessnextmove in computerhitlist or round(attack % 1, 1) == 0 or round(attack % 1, 1) == 0.9):
                ailasthit = False
        else:
            if round(aihitstreak[0] - aihitstreak[1], 1) == 0.1:
                attack = aihitstreak[0] + 0.1
                del aihitstreak[1:]
            elif round(aihitstreak[0] - aihitstreak[1], 1) == -1:
                attack = aihitstreak[0] - 1
                del aihitstreak[1:]
    attack = round(attack, 1)
    for ship in p1ships:
        if attack in ship:
            print("The computer hit your ship!")
            ship.remove(attack)
            computerhitlist.append(attack)
            aihitstreak.append(attack)
            hit = True
            ailasthit = True
        if not ship:
            clear_board()
            p1ships.remove(ship)
            del aihitstreak[:]
            print("Your ship was destroyed!")
            ailasthit = False
    if not hit:
        print("The computer missed!")
        computerattacklist.append(attack)
        ailasthit = False
    if not p1ships:
        print("The computer has won!")
    print_board(computerhitlist, computerattacklist)
    time.sleep(3)


def visualize_ships(row, table):
    n = 0
    temprow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while n < len(table):
        for z in [z for z, x in enumerate(row) if x == table[n] or x == "▨"]:
            temprow[z] = "▨"
        n = n + 1
    for z in [z for z, x in enumerate(temprow) if x != "▨"]:
        temprow[z] = "⬜"
    temprow = " ".join(temprow)
    print(temprow, end=' ')


def print_table(table):
    print("A B C D E F G H I J")
    n = 1
    while n < 11:
        visualize_ships(eval("row" + "[" + str(n-1) + "]"), table)
        print(n)
        n = n + 1


def check_gameover():
    ''' Check if any player's fleet is destroyed '''
    if not p1ships or not computer_ships:
        return True
    else:
        return False


def visualize_attacks(row, attacked_hit_list, attacked_list):
    d = 0
    k = 0
    temprow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while k < len(attacked_hit_list):
        for z in [z for z, x in enumerate(row) if x == attacked_hit_list[k]]:
            temprow[z] = "◉"
        k = k + 1
    while d < len(attacked_list):
        for z in [z for z, x in enumerate(row) if x == attacked_list[d]]:
            temprow[z] = "⭘"
        d = d + 1
    for z in [z for z, x in enumerate(temprow) if x == 0]:
        temprow[z] = "⬜"
    temprow = " ".join(temprow)
    print(temprow, end=' ')


def print_board(attacked_hit_list, attacked_list):
    print("A B C D E F G H I J")
    n = 1
    while n < 11:
        visualize_attacks(eval("row" + "[" + str(n-1) + "]"), attacked_hit_list, attacked_list)
        print(n)
        n = n + 1

main()
