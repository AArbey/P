from Sheeps import SheepClass
from Troll import TrollClass
import random

print("Welcome to Sheep and Troll!")
print("In this game, you will fight against a giant Troll, who is guarding a bridge.")
print("Your team will be composed of 1 to 10 sheep, and your goal is to kill the troll before your team dies.")
print("You will have three attack options: Normal, Super, and defense.")
print("Good Luck!")
print("")
print("")

difficulty = input("Choose your difficulty: Easy, Medium, and Hard: ")
DifficultyFactor = 1.0
if difficulty == "Easy" or difficulty == "easy":
    DifficultyFactor = 0.6
elif difficulty == "Medium" or difficulty == "medium":
    DifficultyFactor = 1.0
elif difficulty == "Hard" or difficulty == "hard":
    DifficultyFactor = 1.4

player_list = []
name_list = ["Ted", "Tom", "Jerry", "Alan", "Andrea", "Ashton", "Bryan", "Caitlin", "Colby", "Luis"]

sheep_Total_Health = 0
sheep_Total_Health_2 = 0

random_num_Main = random.randint(1, 10)

for Number_Of_Sheep in range(0, random_num_Main):
    sheep = SheepClass(name_list.pop(0))
    player_list.append(sheep)
    sheep_Total_Health += sheep.health
    sheep_Total_Health_2 = sheep_Total_Health

print("You have "+str(Number_Of_Sheep)+" sheep.")
name_list = ["Ted", "Tom", "Jerry", "Alan", "Andrea", "Ashton", "Bryan", "Caitlin", "Colby", "Luis"]

troll = TrollClass("TrolliTheTroll", sheep_Total_Health, DifficultyFactor)

number = 0

while sheep_Total_Health_2 > 0 and troll.health > 0:
    for i in range(0, random_num_Main):
        sheep25 = SheepClass(name_list[i])
        sheep25.action(troll)
        if troll.health < 0:
            print("Well Done! You killed the Giant Troll")
            print("You have " + str(random_num_Main) + " sheep left.")
            break
        troll.action(sheep25)
        if sheep25.health < 0:
            print("Oh no! " + sheep25.name + " died against the giant Troll!")
            name_list.pop(i)
            number = 1
        else:
            number = 0
        print("You have " + str(random_num_Main) + " sheep left.")

    if number == 1:
        random_num_Main -= 1

    name_list = ["Ted", "Tom", "Jerry", "Alan", "Andrea", "Ashton", "Bryan", "Caitlin", "Colby", "Luis"]
    for x in range(0, random_num_Main):
        sheep25 = SheepClass(name_list.pop(0))
        sheep_Total_Health_2 = sheep_Total_Health_2 + sheep25.health
    name_list = ["Ted", "Tom", "Jerry", "Alan", "Andrea", "Ashton", "Bryan", "Caitlin", "Colby", "Luis"]
