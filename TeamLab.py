# -*- coding: utf-8 -*-

# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Erika Yao
#               Joss Bhuiyan
#               Julia Felder
#               Elio Nunez Del Arco
# Section:      241
# Assignment:   Final Project
# Date:         23 11 2020

import random


"""
This is the character class.
Attributes:
    health: the amount of health for the character to have in combat
    coordinates: the current location of the character on the map
    symbol: the symbol the character should be represented as on the map
Functions:
    take_damage: decreases the health attribute of the character by 1
    heal: increases the health attribute of the character by 1
"""
class character:
    def __init__(self,health,coordinates,symbol):
        self.health = health
        self.coordinates=coordinates
        self.symbol=symbol
    def take_damage(self):
        self.health-=1
    def heal(self):
        self.health+=1
        
#initializing variables for the game: wall locations on the map, attack options,
#pickup locations, player object and location, monster objects and locations
walls = [[0,0],[0,1],[0,2], [0,3],[0,4],[1,4],[2,4],[2,5],[2,6],[2,7],[3,7],[4,7],[4,6],[4,5],[4,4],[5,4],[6,4],[7,4],[8,4],[9,4],[9,3],[9,2],[8,2],[7,2],[6,2],[6,1],[6,0],[5,0],[4,0],[3,0],[2,0],[1,0],[2,2],[3,2],[4,2]]
attacks=['shield', 'parry', 'strike']
pickups=[[3,3],[5,1],[6,3],[7,3],[8,3]]
dead = False
player=character(6,[1,1],"P  ")

monsters=[character(2,[2,3],'O  '), character(2,[4,1],'O  '), character(4,[5,3],"T  "), character(6,[3,6], "D  ")]


"""
This function prints out the map using the stored location arrays and the
character locations.
"""
def print_map():
    game_map=[["_  " for x in range(10)] for y in range(8)]
    for wall in walls:
        game_map[wall[1]][wall[0]]='W  '
    
    game_map[player.coordinates[1]][player.coordinates[0]]=player.symbol
    for pickup in pickups:
        game_map[pickup[1]][pickup[0]]="H  "
    for monster in monsters:
        game_map[monster.coordinates[1]][monster.coordinates[0]]=monster.symbol
    
    for x in range(7,-1,-1):
        for y in range(0,10):
            print(game_map[x][y],end='')
        print('\n')
    
    
"""
This function attempts to move the character in the given direction, checking
for the validity of the input string as well as the validity of the movement
based on the map.
Parameters:
    direction: the string inputted by the user for movement
"""
def move_player(direction):
    if direction=="up":
        newdir=[player.coordinates[0],player.coordinates[1]+1]
    elif direction=="down":
        newdir=[player.coordinates[0],player.coordinates[1]-1]    
    elif direction=="left":
        newdir=[player.coordinates[0]-1,player.coordinates[1]]
    elif direction=="right":
        newdir=[player.coordinates[0]+1,player.coordinates[1]]
    else:
        print("invalid input")
        return
    
    
    try:
        x=collision(newdir)
    except:
        return
    if x:
        print("collision detected-Invalid Move")
    else:
        monster_collision(newdir)
        pickup_collision(newdir)
        player.coordinates=newdir
  
    
"""
This function checks the given location for a pickup. If the location is the
location of a pickup, the player regains health and the pickup is removed from
the list of pickups.
Parameters:
    coords: the current location to check for a pickup
"""
def pickup_collision(coords):
    for pickup in pickups:
        if pickup==coords:
            player.heal()
            print('you have gained 1 HP. You now have %i HP' %player.health)
            pickups.pop(pickups.index(pickup))


"""
This function checks the given location for a monster. If the location is the
location of a monster, the combat function is triggered with the appropriate
monster object.
Parameters:
    coords: the current location to check for a monster
"""
def monster_collision(coords):
    
    for monster in monsters:
        if monster.coordinates==coords:
            print('combat')
            combat(monster)


"""
This function runs the appropriate combat sequence given a monster object. It
will run combat matchups until either the player or the monster reaches zero
health.
Parameters:
    enemy: the monster object to run the combat sequence with
"""
def combat(enemy):
    if(enemy.symbol=="O  "):
        print("a fearsome ogre has blocked your path")
    elif enemy.symbol=="T  ":
        print("a troll blocks your path")
    elif enemy.symbol=='D  ':
        print("a giant dragon has blocked your path")
    while(player.health!=0 and enemy.health!=0):
        attack_player=input("select your attack (shield, parry, strike) ")
        attack_enemy=attacks[random.randrange(0,3)]
        if attack_player == attack_enemy:
            print("both of you have selected %s. no damage was taken or dealt" %attack_player)
            
        elif attack_player == "shield":
            if attack_enemy == "strike":
                print("you used shield and the enemy used strike. You take 1 damage")
                player.take_damage()
            else:
                print('you used shield and the enemy used parry. You deal 1 damage')
                enemy.take_damage()
        elif attack_player == "parry":
            if attack_enemy == "shield":
                print("you used parry and the enemy used shield. You take 1 damage")
                player.take_damage()
            else:
                print('you used parry and the enemy used strike. You deal 1 damage')
                enemy.take_damage()
        elif attack_player == "strike":
            if attack_enemy == "parry":
                print("you used strike and the enemy used parry. You take 1 damage")
                player.take_damage()
            else:
                print('you used strike and the enemy used shield. You deal 1 damage')
                enemy.take_damage()
        else:
            print("That's not a valid play. Check your spelling!")
    if(enemy.health==0):
        for i in range(0,len(monsters)):
            if enemy.coordinates == monsters[i].coordinates:
                monsters.pop(i)
                break
        print("the monster has been defeated")
        print("you have %i HP remaining" %player.health)
    else:
        print("game over")
        global dead
        dead=True  
            

"""
This function checks the given location for a wall to detect collisions in
movement.
Parameters:
    coords: the location to check for a wall
Returns:
    True if there is a wall at that location
    False if there is no wall at that location
"""
def collision(coords):
    for wall in walls:
        if(coords==wall):
            return True
    return False

#reading in and splitting up the story into sections
story_file = open("story.txt", "r")
story_lines = story_file.readlines()
splits = []
for i in range(len(story_lines)):
    if story_lines[i] == "INTRODUCTION\n":
        splits.append(i)
    elif story_lines[i] == "SUCCESS!\n":
        splits.append(i)
    elif story_lines[i] == "DEFEAT\n":
        splits.append(i)
story = [story_lines[1:splits[1]], story_lines[splits[1] + 1:splits[2]], story_lines[splits[2] + 1:]]

#adding in the user's name to the story
name = input("What is your name? ")
first = story[0][0].split(" ")
first[0] = name
line = ""
for word in first:
    line += word + " "
line = line[:len(line) - 1]
story[0][0] = line
story[1][0:0] = " "
story[1][0] = name + ", \n"
story[2][0:0] = " "
story[2][0] = name + ", \n"

#writing out new story to a file with name included
result_story = open("result.txt", "w")
result_story.write("INTRODUCTION\n")
for line in story[0]:
    result_story.write(line)
result_story.write("\nSUCCESS!\n")
for line in story[1]:
    result_story.write(line)
result_story.write("\nDEFEAT\n")
for line in story[2]:
    result_story.write(line)

#printing out introduction for the game
print()
for line in story[0]:
    print(line)

#loop for the game
while(not dead):
    print_map()
    move_player(input("which way would you like to go (up, down, left, right)?  "))
    if len(monsters) == 0:
        for line in story[1]:
            print(line)
        dead = True

#printing death message if dead
if len(monsters) != 0:
    for line in story[2]:
            print(line)

#closing files
result_story.close()
story_file.close()