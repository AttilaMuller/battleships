import random

p1ships = [[1.1, 1.2], [2.3, 2.4, 2.5], [0.0, 1.0, 2.0, 3.0, 4.0, 5.0], [3.5, 4.5, 5.5], [8.5, 8.6, 8.7, 8.8]]

computerattacklist = []  # contains the coordinates where the computer missed
computerhitlist = []  # contains the coordinates where the computer hit a ship


ailasthit = False  # tells if the ai can continue its line of targeting
aihitstreak = []  # the first item of this list is the basis of the targeting behavior

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
        visualize_attacks(eval("row"+str(n)), attacked_hit_list, attacked_list)
        print(n)
        n = n + 1


def ai_attack(aihitstreak):
    global ailasthit
    hit = False
    if not aihitstreak:
        attack = random.randrange(10) + random.randrange(10) / 10
        while attack in computerhitlist or attack in computerattacklist:
            attack = random.randrange(10) + random.randrange(10) / 10
    elif len(aihitstreak) == 1:
        if (round(aihitstreak[0] - 0.1, 1) not in computerattacklist and round((aihitstreak[0] - 0.1) % 1, 1) != 0.9
                and round(aihitstreak[0] - 0.1, 1) not in computerhitlist):
            attack = aihitstreak[0] - 0.1
        elif ((aihitstreak[0] + 1) < 10 and (aihitstreak[0] + 1) not in computerattacklist and 
              (aihitstreak[0] + 1) not in computerhitlist):
            attack = aihitstreak[0] + 1
        elif ((aihitstreak[0] + 0.1) % 1 != 0 and (aihitstreak[0] + 0.1) not in computerattacklist 
              and (aihitstreak[0] + 0.1) not in computerhitlist):
            attack = aihitstreak[0] + 0.1
        elif ((aihitstreak[0] - 1) > 0 and (aihitstreak[0] - 1) not in computerattacklist and 
              (aihitstreak[0] - 1) not in computerhitlist):
            attack = aihitstreak[0] - 1
    elif len(aihitstreak) > 1:
        if ailasthit:  # ha az irány jó, folytatja a sorban lövöldözést
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
        else:  # ha az irány rossz, átugrik a túloldalra
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


while p1ships:
    ai_attack(aihitstreak)
    input("Enter: ")
