#!/usr/bin/python3

import string

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

row1 = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
row2 = [0.1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1]
row3 = [0.2, 1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2]
row4 = [0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3, 9.3]
row5 = [0.4, 1.4, 2.4, 3.4, 4.4, 5.4, 6.4, 7.4, 8.4, 9.4]
row6 = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
row7 = [0.6, 1.6, 2.6, 3.6, 4.6, 5.6, 6.6, 7.6, 8.6, 9.6]
row8 = [0.7, 1.7, 2.7, 3.7, 4.7, 5.7, 6.7, 7.7, 8.7, 9.7]
row9 = [0.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
row10 = [0.9, 1.9, 2.9, 3.9, 4.9, 5.9, 6.9, 7.9, 8.9, 9.9]

carrier2 = []  # 5 units long
battleship2 = []  # 4 units long
cruiser2 = []  # 3 units long
submarine2 = []  # 3 units long
destroyer2 = []  # 2 units long
p2ships = [carrier2, battleship2, cruiser2, submarine2, destroyer2]
p2usedspace = []
p2attacklist = []
p2hitlist = []

'''Functions'''


def check_horizon(a):
    if a == "v" or a == "h":
        return True
    else:
        return False


def convert_input(i):
    a = string.ascii_lowercase.index(i[0])
    b = float(i[1:]) / 10 - 0.1
    c = round((a + b), 1)
    return c


def check_ocean(c, i, o):
    try:
        f = string.ascii_lowercase.index(i[0])
        s = float(i[1:]) - 1
        if c == "h" and f + o > 10:
            return False
        elif f > 9:
            return False
        elif c == "v" and s + o > 10:
            return False
        elif s > 9:
            return False
        else:
            return True
    except BaseException:
        return False


def check_usedspace(s, u, l, a, b):
    b = convert_input(b)
    s.append(round(b, 1))
    if a == "h":
        for i in range(1, l):  # That's one, and lowercase l
            s.append(round((b + i), 1))
    else:
        for i in range(1, l):
            s.append(round((b + i * 0.1), 1))
    g = list(set(s) & set(u))
    if not g:
        u.append(round(b, 1))
        if a == "h":
            for i in range(1, l):  # That's one, and lowercase l
                u.append(round((b + i), 1))
        else:
            for i in range(1, l):
                u.append(round((b + i * 0.1), 1))
        return True
    else:
        for i in s:
            s.remove(i)
        return False


def create_ship(s, l, u):
    ''' Creates s-type ship with l length in u space '''
    a = input("It is " + str(l) + " units long. Enter 'h' to place it "
              "horizontally or 'v' to place it vertically: ")
    while not check_horizon(a):
        a = input("Enter 'h' to place it horizontally or 'v' to place it vertically: ")
    b = input("Give the starting coordinates. Your ship will be placed accordingly: ")
    while not check_ocean(a, b, l) or not check_usedspace(s, u, l, a, b):
        b = input("The ocean is big, but not THAT big. Give other coordinates: ")
    print_table(u)


def p2_attack():
    print("Player 2 board:")
    print_board(p2hitlist, p2attacklist)
    hit = 0
    attack = input("Player 2 shoots at: ")
    while not check_ocean("v", attack, 0) or convert_input(
            attack) in p2attacklist or convert_input(attack) in p2hitlist:
        attack = input("Invalid input - Player 2 shoots at: ")
    attack = convert_input(attack)
    for s in p1ships:
        if attack in s:
            print("Hit!")
            s.remove(attack)
            p2hitlist.append(attack)
            hit = 1
        if not s:
            p1ships.remove(s)
            print("Player 2 destroyed a ship!")
    if hit == 0:
        print("Miss!")
        p2attacklist.append(attack)
    if not p1ships:
        print("Player two has won!")


def p1_attack():
    print("Player 1 board:")
    print_board(p1hitlist, p1attacklist)
    hit = 0
    attack = input("Player 1 shoots at: ")
    while not check_ocean("v", attack, 0) or convert_input(
            attack) in p2attacklist or convert_input(attack) in p2hitlist:
        attack = input("Invalid input - Player 1 shoots at: ")
    attack = convert_input(attack)
    for s in p2ships:
        if attack in s:
            print("Hit!")
            s.remove(attack)
            p1hitlist.append(attack)
            hit = 1
        if not s:
            p2ships.remove(s)
            print("Player 1 destroyed a ship!")
    if hit == 0:
        print("Miss!")
        p1attacklist.append(attack)
    if not p2ships:
        print("Player one has won!")


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
        visualize_ships(eval("row" + str(n)), table)
        print(n)
        n = n + 1


def check_gameover():
    if not p1ships or not p2ships:
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
        visualize_attacks(eval("row" + str(n)), attacked_hit_list, attacked_list)
        print(n)
        n = n + 1


'''Game begins'''

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
print("\n" * 4)


'''Player 1 deploys the ships'''
print("Player 1, choose the coordinates for your fleet! (Player 2, please look away now! :) )")
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

print("\n" * 40)

'''Player 2 deploys the ships'''
print("Player 2, choose the coordinates for your fleet! (Player 1, please look away now! :) )")
print_table(p2usedspace)
print(carrier)
create_ship(carrier2, 5, p2usedspace)
print(battleship)
create_ship(battleship2, 4, p2usedspace)
print(cruiser)
create_ship(cruiser2, 3, p2usedspace)
print(submarine)
create_ship(submarine2, 3, p2usedspace)
print(destroyer)
create_ship(destroyer2, 2, p2usedspace)

print("\n" * 40)

'''Time for battle!'''

input("The battle begins! Take turns at shooting your missiles!\n"
      "\nPress Enter to continue")

while not check_gameover():
    p1_attack()
    if check_gameover():
        break
    p2_attack()
