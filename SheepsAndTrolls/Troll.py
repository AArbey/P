import random


class TrollClass:
    def __init__(self, name, health, difficultyFactorTroll):
        self.name = name
        self.health = difficultyFactorTroll * health
        self.normal_damage = 20
        self.super_damage = 60
        self.super_number_Troll = 0

    def normal_attack(self, opponent):
        damage_dealt = self.normal_damage
        opponent.take_damage(damage_dealt)

    def super_attack(self, opponent):
        damage_dealt = self.normal_damage
        opponent.take_damage(damage_dealt)

    def take_damage(self, damage_dealt):
        self.health -= damage_dealt

    def is_alive(self):
        if self.health <= 0:
            return False
        else:
            return True

    def action(self, opponent):
        random_num_Troll = random.randint(0, 100)
        if self.super_number_Troll == 0:
            if random_num_Troll <= 50:
                self.normal_attack(opponent)
                print("The troll attacked you with a normal attack, you now have " + str(opponent.health) + " health.")

            elif random_num_Troll <= 100:
                self.super_attack(opponent)
                self.super_number_Troll = 1
                print("The troll attacked you with a super attack, you now have " + str(opponent.health) + " health.")

        elif self.super_number_Troll == 1:
            print("The Troll didn't attack you, as he was too tired.")
            self.super_number_Troll = 0
