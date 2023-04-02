class Character:
    def __init__(self, name, hp, xp_gained, attack, defense, magic=0):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack
        self.defense_power = defense
        self.magic = magic
        self.xp_gained = xp_gained
        self.xp = 0
        self.level = 1

    def is_dead(self):
        if self.hp <= 0: return True    # Returns true if health is <= 0 (dead)
        return False

    def attack(self, other_character):  # Function for simulating attacks
        if self.is_dead(): print(self.name, 'cannot attack because he/she is dead.')    # Prevents attacking if attacker is already dead (applies to party)
        elif other_character.is_dead(): # Skips attack if opponent is dead (this avoids killing already dead opponents)
            pass
        else:
            damage = self.attack_power - other_character.defense_power  # Damage calculation
            if damage < 0: damage = 0   # When enemy defense is higher than character attack, sets damage to 0 to avoid dealing negative damage and healing enemy
            other_character.hp -= damage
            print(" -", self.name, 'does', damage, 'damage to', other_character.name)
            if other_character.hp <= 0: # Checks if character is dead after attack
                other_character.hp = 0
                print("\n     ", self.name, "has SLAIN", other_character.name + "!\n")
                self.gain_xp(other_character.xp_gained) # Call gain_xp function on character who killed enemy
            

    def heal(self, party):
        if self.is_dead(): print(self.name, 'cannot heal because he/she is dead.')
        else:
            for party_member in party:  # Iterate through each member in party
                if not party_member.is_dead():
                    party_member.hp += self.magic   # Heal party member
                    if party_member.hp > party_member.max_hp:   # Prevents healing above max hp
                        party_member.hp = party_member.max_hp
                    print(" -", self.name, 'heals', self.magic, 'hp for', party_member.name)
    
    def gain_xp(self, xp):
        levels = [2,3,4,5,6]
        level_min_xp = [100,200,300,400,500]
        level_attack_gain = [5.0,2.5,2.5,2.5,2.5]
        level_defense_gain = [2.5,2.5,2.5,2.5,2.5]
        level_magic_gain = [2.0,1.0,2.0,2.0,2.0]
        leveltracker = self.level   # Holds value for current level

        self.xp += xp   # Add xp to pool
        print("\t  {} gained {}xp".format(self.name, xp))
        for i in level_min_xp[self.level-1:]:   # Iterates through minimum xp requirement for each level beyond current
            if self.xp >= i:    # Checks if xp is greater than minimum xp for next level
                self.level = levels[level_min_xp.index(i)] # set new level
                self.attack_power += level_attack_gain[level_min_xp.index(i)]   # add attack stat upgrade
                self.defense_power += level_defense_gain[level_min_xp.index(i)] # add defense stat upgrade
                self.magic += level_magic_gain[level_min_xp.index(i)]   # add magic stat upgrade
        if self.level > leveltracker:  #allows us to check if xp gain constitutes a level up (you can't level up beyond 6)
            print("    {} has leveled up to level {}!".format(self.name, self.level))

    def __str__(self):
        if self.is_dead(): return '{}: [DEAD]'.format(self.name)    # Displays [Dead] if character health is 0
        else: return '{}: (HP: {}, XP: {}, Level: {}, Attack: {}, Defense: {})'.format(self.name,
                        self.hp, self.xp, self.level, self.attack_power, self.defense_power)    # Output all character stat parameters


def checkWin(party, enemies):
    counterParty = 0
    counterEnemies = 0

    for i in party:
        if i.is_dead(): counterParty += 1   # Count number of dead party members
    for i in enemies:
        if i.is_dead(): counterEnemies += 1 # Count number of dead enemies

    if counterParty == len(party):  # Check if all allies are dead
        print("\n   All party members are dead. You lose.")
    elif counterEnemies == len(enemies):    # Check if all monsters are dead
        print("\n   All enemies are dead. You are victorious!")


def battleLoop(party, enemies):
    round = 1
    for enemy in enemies:   # Iterates through each enemy in enemies, jumps to next index once current enemy is dead
        while not enemy.is_dead() and not (party[0].is_dead() and party[1].is_dead() and party[2].is_dead()):   # Loops while enemy is alive and atleast one ally is alive
            print("\n    ===============================\n    |      ==[ Round:",round," ]==      |\n    ===============================")
            print("\t", enemy.name, "approaches!\n")

            # Execute Party Moves
            for member in party: # Party Move: iterates through each party member and attacks enemy (or heals in Glinda's case)
                if not enemy.is_dead(): # Concludes battle early if a party member kills enemy
                    if member.name == "Glinda": member.heal(party)    # Statement to ensure Glinda can only heal
                    else: member.attack(enemy)   # Party member attacks monster
            
            # Execute Monster Moves
            for member in party: # Enemy Move: iterates through each party member and attacks them
                if not enemy.is_dead(): # Skips attack function call to avoid multiple attack attempts & messages when monster is already dead
                    enemy.attack(member) # Monster attacks party member

            # Display Character Status
            print("\n    ----------------\n    | -[ Status ]- |\n    ----------------")
            print("     + Allies: +")
            for n in party: print("\t +", n)    # Print all party member statuses
            print("     ~ Enemies: ~")
            for n in enemies: print("\t ~", n)  # Print all monster statuses

            round += 1  # Increment round
    
    # While loop exits if all allies are dead or all enemies are dead
    checkWin(party, enemies)    # Once all enemies/allies are dead call method to check which side won (is alive)


def sampleRPG_Game():
    # Parameters: 'name', 'hp', 'xp', 'attack', 'defense', 'magic'
    krogg = Character('Krogg', 180, 0, 20, 20)
    glinda = Character('Glinda', 120, 0, 5, 20, 5)
    geoffrey = Character('Geoffrey', 150, 0, 15, 15)
    party = [krogg, geoffrey, glinda]
    enemy1 = Character('Spider 1', 50, 100, 10, 1)
    enemy2 = Character('Spider 2', 50, 100, 10, 1)
    enemy3 = Character('Wolf 1', 100, 250, 15, 5)
    enemy4 = Character('Wolf 2', 100, 250, 15, 5)
    enemy5 = Character('Bear 1', 200, 350, 20, 10)
    enemy6 = Character('Bear 2', 200, 350, 20, 10)
    enemy7 = Character('Red Dragon', 300, 800, 30, 20)
    enemy8 = Character('Blue Dragon', 400, 1000, 35, 20)
    enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8]
    
    battleLoop(party, enemies)  # Execute battle loop

if __name__ == "__main__":
    sampleRPG_Game()