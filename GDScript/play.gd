const FUMBLE_CHANCE_FIELD = "FUMBLE_CHANCE"

var GAME = $GAME

func _penaltytrue(roll):
    penalty(roll, True)
func _penaltyfalse(roll):
    penalty(roll, False)
func _QT(_):
    customKey("QT", "QT")
func _breakaway(_):
    customKey("Breakaway", "Breakaway")

const PLAYMAP = {
    '+': funcref(self, softs),
    '-': funcref(self, softs),
    ':': funcref(self, hard),
    'OFF': funcref(_penaltyfalse),
    'DEF': funcref(_penaltytrue),
    'PI': funcref(_penaltytrue),
    'INC': funcref(self, incomplete),
    'QT': funcref(self, _QT),
    'INT': funcref(self, interception),
    'F': funcref(self, fumble),
    'BK': funcref(self, fumble),
    'B': funcref(self, _breakaway)
}


func roll(callout, offensePlay=null): # eg roll('Line Plunge')
    stats = json_reader.readJson("data/teams/"+GAME.team, attribute=GAME.localstance)  # TODO Source from TEAM class
    numRoll = random.random()*100
    #print(stats)
    #print(callout)
    #print(offensePlay)
    if offensePlay is null:
        GAME.rolls[GAME.localstance] = stats[callout][GAME.weightedRoll(GAME.localstance, numRoll)]
    else:
        GAME.rolls[GAME.localstance] = stats[callout][offensePlay][GAME.weightedRoll(GAME.localstance, numRoll)]

func processPlay():
    finalStance = determinePriority()
    if finalStance:
        PLAYMAP[_rolltype(GAME.rolls[finalStance])](GAME.rolls[finalStance])#call resolve
        GAME.boob = GAME.rolls[finalStance].split(" ")[-1] == "*" or GAME.boob
    else:
        soft()


func determinePriority():
    defType = _rolltype(GAME.rolls['Defense'])
    attType = _rolltype(GAME.rolls['Offense'])
    if defType not in GAME.simplePriorityLow:
        return 'Defense'
    elif attType not in GAME.simplePriorityLow:
        return 'Offense'
    else:
        return None


func _rolltype(rollRes, position=0):
    return rollRes.split(" ")[position]


"""
These represent all the different play types that can occur and their resolves.
"""
func soft():
    mod1 = (''.join(GAME.rolls["Defense"].split(" ")[:2]))
    mod2 = (''.join(GAME.rolls["Offense"].split(" ")[:2]))
    if mod2 == "+TD" or mod1 == "+TD":
        GAME.yard = 100
        GAME.TD = True
    else:
        GAME.yard += (int)(mod1)+(int)(mod2)
    if _rolltype(GAME.rolls['Offense'], position=-1) == "*" or _rolltype(GAME.rolls['Defense'], position=-1) == "*":
        GAME.boob = True


func softs(singlePlay):
    mod = (''.join(singlePlay.split(" ")[:2]))
    if mod == "+TD":
        GAME.yard = 100
    else:
        GAME.yard += (int)(mod)
    if singlePlay[-1] == "*":
        GAME.boob = True


func hard(result):
    mod = result.split(" ")[1]
    if mod == "+TD":
        GAME.yard = 100
        return
    GAME.yard += (int)(mod)


func incomplete(result):
    # Incomplete is always considered oob
    GAME.boob = True


func interception(result):
    GAME.yard += (int)(result.split(" ")[1])
    GAME.toggleStance()


func fumble(result):
    if GAME.localstance == "Offense":
        fum = json_reader.readJson("data/teams/"+GAME.team, attribute=FUMBLE_CHANCE_FIELD)
    else:
        fum = json_reader.readJson("data/teams/"+GAME.enemy, attribute=FUMBLE_CHANCE_FIELD)
    GAME.yard += (int)(result.split(" ")[1])
    roll = random.random()*100
    if roll <= fum:
        print("Fumble recovered!")
        return
    print("Fumble lost!")
    GAME.toggleStance()
    GAME.down = 1


func penalty(result, gain):
    if not gain:
        GAME.yard -= (int)(result.split(" ")[1])
    else:
        GAME.yard += (int)(result.split(" ")[1])
    # No down change on penalties
    GAME.down -= 1
    # Penalties are always considered oob
    GAME.boob = True


func customKey(ctype, key):
    print(ctype + "!")
    if GAME.localstance == 'Offense':
        line = json_reader.readJson("data/teams/"+GAME.team, attribute=key)
    else:
        line = json_reader.readJson("data/teams/"+GAME.enemy, attribute=key)
    print(line)
    newRoll = GAME.weightedRoll('Offense', random.random()*100)
    newPlay = line[newRoll]
    print(ctype + " roll: %s" % newPlay)
    PLAYMAP[_rolltype(newPlay)](newPlay)
