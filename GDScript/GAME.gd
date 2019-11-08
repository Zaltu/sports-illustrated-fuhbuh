const STANCES = ['Offense', 'Defense', 'Kick']
const QNAMES = ['1st', '2nd', '3rd', '4th', 'END']

var clock = ['1st', 720]
var simplePriorityLow = ['+', '-']
var score = [0, 0] # (Me, Them)
var conn = null # IP address or connection object for the second player
var localstance = ''
var yard = 40
var boob = False
var TD = False

func weightedRoll(stance, perc):
    numProbTable = json_reader.readJson("data/dice.json")
    for sheetRoll in numProbTable[stance]:
        if numProbTable[stance][numProbTable[stance].index(sheetRoll)+1] > perc:
            #print(sheetRoll, numProbTable[stance].index(sheetRoll))
            return numProbTable[stance].index(sheetRoll)


func setTeam(team):
    self.team = team


func setEnemy(team):
    self.enemy = team


func setState(state):
    self.state = state


func switchYardSide():
    self.yard = 100 - self.yard


func toggleStance():
    if self.localstance == "Offense" or self.localstance == "Kick":
        self.localstance = "Defense"
    else:
        self.localstance = "Offense"
    self.switchYardSide()
    self.down = 1
    self.firstdown = self.yard+10



func turnOver():
    print("Switched sides!")  # Only for CMD mode
    self.down = 1
    self.toggleStance()
    print("Offense is now on the %s yard line." % GAME.yard)  # Only for CMD mode


func clock(star):
    self.clock[1] -= 30 if not star else 10
    if self.clock[1] <= 0:
        print("Changing quarters")  # Only for CMD mode
        self.changeQuarters()
    self.boob = False

func changeQuarters():
    self.clock[0] = self.QNAMES[self.QNAMES.index(self.clock[0])+1]
    if self.clock[0] == 'END':
        self.gameOver()
    self.clock[1] = 720
    if self.clock[0] == src.QNAMES[2]:
        print("Halftime!")
        if self.startingstance == "Offense" && self.localstance == "Offense":
            self.toggleStance()
        self.kickoff()


func gameOver():
    print("Game over")  # Only for CMD mode
    print("Final score: %s to %s" % (self.score[0], self.score[1]))  # Only for CMD mode
    self.end = True


func handleFluff():
    print("")
    if self.firstdown >= 100:
        print("%s and goal on the %s" % (self.QNAMES[self.down-1], self.yard))
    else:
        print("%s and %s on the %s" % (self.QNAMES[self.down-1], self.firstdown-self.yard, self.yard))

    print("Game time: %s" % self.clock)

func handleFluffCall():
    print("Offense callout: %s -> %s" % (self.offplay, self.rolls['Offense']))
    print("Defense callout: %s -> %s" % (self.defplay, self.rolls['Defense']))


func handleTD():
    if self.yard >= 100:
        print("TOUCHDOWN!")  # Only for CMD mode
        self.handleScore()
        self.TD = True


func handleScore():
    if self.localstance == "Offense":
        self.score[0] += 7
    else:
        self.score[1] += 7


func handleDowns():
    if self.yard >= 100:  # TD
        return
    if self.yard >= self.firstdown:
        print("First Down!")  # Only for CMD mode
        self.down = 1
        self.firstdown = self.yard + 10
    else:
        self.down += 1
    if self.down == 5:
        self.turnOver()


func fullTurn():
    self.handleFluff()  # Only for CMD mode
    play.roll(self.callout, offensePlay=self.into if self.localstance == "Defense" else null)
    self.handleFluffCall()  # Only for CMD mode
    play.processPlay()
    self.handleDowns()
    self.handleTD()
    clock(self.boob)


func kickoff():
    print("")  # Only for CMD mode
    self.TD = False
    self.yard = 40
    play.customKey('Kickoff', 'Kickoff')
    self.toggleStance()
    play.customKey('Kickoff Return', 'Kickoff Return')
    self.firstdown = self.yard + 10
    self.down = 1


func punt():
    play.customKey('Punt', 'Punt')
    self.toggleStance()
    play.customKey('Punt Return', 'Punt Return')
    self.firstdown = self.yard + 10
    self.down = 1
    self.handleFluff()
