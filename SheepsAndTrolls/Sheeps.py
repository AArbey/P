import random
from Troll import TrollClass


class SheepClass:
    def __init__(self, name):
        Random_Number_Health = random.randint(30, 80)
        self.name = name
        self.health = Random_Number_Health
        self.normal_damage = 15
        self.super_damage = 45
        self.defense_damage = 7.5
        self.super_number_sheep = False

    def normal_attack(self, opponent):
        damage_dealt = self.normal_damage
        opponent.take_damage(damage_dealt)

    def super_attack(self, opponent):
        damage_dealt = self.super_damage
        opponent.take_damage(damage_dealt)

    def defense_attack(self, opponent):
        damage_dealt = self.defense_damage
        opponent.take_damage(damage_dealt)

    def take_damage(self, damage_dealt):
        self.health -= damage_dealt

    def get_stats(self):
        print("Health: " + str(self.health))
        print(" ")

    def is_alive(self):
        if self.health <= 0:
            return False
        else:
            return True

    def action(self, opponent):
        if self.super_number_sheep == False:
            actions = input("What do you want " + self.name + " to do? ")

            if actions == "Normal" or actions == "normal":
                self.normal_attack(opponent)
                print("You just attacked the giant troll, but he also did! The troll has " + str(opponent.health) + " health.")
                print("You have " + str(self.health) + " health.")

            elif actions == "Super" or actions == "super":
                self.super_attack(opponent)
                self.super_number_sheep = True
                print("You just attacked the giant troll, but he also did! The troll has " + str(
                    opponent.health) + " health.")
                print("You have " + str(self.health) + " health.")
                
            elif actions == "Defense" or actions == "defense":
                self.normal_attack(opponent)
                print("You just attacked the giant troll, but he also did! The troll has " + str(
                    opponent.health) + " health.")
                print("You have " + str(self.health) + " health.")

        else:
            print("You can't attack now, as you used you super attack during the last round.")
            self.super_number_sheep = False

        # elif self.super_number_sheep ==550 1:
        #     print("You can't attack now, as you used you super attack during the last round.")
        #     self.super_number_sheep = 0
