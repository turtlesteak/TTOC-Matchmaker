import csv

#separation line to show which section we are in (UI)
def outputLine(word):
    word = word.upper()

    Statement = "\n### " + word + " "

    symbolCount = 64 - len(word)

    for i in range(symbolCount):
        Statement += "#"

    print(Statement)

#Counts player score based on policies selected
def scoreCount(policies):
    #current policies
    fullPolicies = [
        "I understand that the TTOC Crew will organize my match times for me, and will remove me from the competition if I miss my match or if I do not confirm my match time at least 12 hours prior to it.",
        "I understand that players must have over 5000 wins and have 3  month of participation in the TankTrouble Community to compete. Spectators must have over 3 months of participation in the community.",
        "I understand that if a player or spectator misses their match or goes against competition standards, they will not be allowed to participate for the remainder of this year's TTOC.",
        "I understand that chatting and chat-killing is allowed during matches, but I cannot complain about lag.",
        "I understand that I cannot leave a match for more than 10 total minutes.",
        "I understand that if I am suspected of sharing accounts, I will not be allowed to participate in TTOC.",
        "I understand that the spectator is in charge of regulating their match. Only a moderator can overrule them.",
        "I understand that spectators, including substitute spectators, must fill out this form and get approval from the TTOC Crew in order to spectate my match.",
        "I understand that I am applying for the Classic gamemode.",
        "I understand that TTOC was created by purup and bbc, just like TankTrouble.",
        "I understand that any player watching my match can remove me from TTOC.",
        "I understand that I am applying for the Target gamemode.",
        "I understand that my opponent will organize our match time for us."
    ]

    score = 0

    #right policies add points to the score
    if fullPolicies[0] in policies:
        score += 1
    if fullPolicies[1] in policies:
        score += 1
    if fullPolicies[2] in policies:
        score += 1
    if fullPolicies[3] in policies:
        score += 1
    if fullPolicies[4] in policies:
        score += 1
    if fullPolicies[5] in policies:
        score += 1
    if fullPolicies[6] in policies:
        score += 1
    if fullPolicies[7] in policies:
        score += 1
    if fullPolicies[8] in policies:
        score += 1
    
    #wrong policies subtract from the score
    if fullPolicies[9] in policies:
        score -= 1
    if fullPolicies[10] in policies:
        score -= 1
    if fullPolicies[11] in policies:
        score -= 1
    if fullPolicies[12] in policies:
        score -= 1

    return score

#Converts server ping rankings to numbers to allow comparison
def serverRank(atlanta, dallas, fremont, london, newark, singapore, sydney):
    #array of the pings
    serverPing = [atlanta, dallas, fremont, london, newark, singapore, sydney]

    #go through every server to set the rank
    for i in range(len(serverPing)):
        if serverPing[i] == "0 - 50ms":
            serverPing[i] = 1
        
        elif serverPing[i] == "50 - 100ms":
            serverPing[i] = 2
        
        elif serverPing[i] == "100 - 150ms":
            serverPing[i] = 3
        
        elif serverPing[i] == "150 - 200ms":
            serverPing[i] = 4
        
        elif serverPing[i] == "200ms+":
            serverPing[i] = 5

    return serverPing

#Makes sure the player/hybrid has enough time to compete
def entryCheck(fCheck, mCheck, posID, score, week):
    if posID == "As a Player only":
        position = ["Player", 1]
    elif posID == "As a Spectator only":
        position = ["Spectator", 2]
    elif posID == "As a Player and Spectator":
        position = ["Hybrid", 3]
    
    if fCheck != 'y' and mCheck != 'y':
        return [position, False, "failing both checks"]
    elif fCheck != 'y':
        return [position, False, "failing forum check"]
    elif mCheck != 'y':
        return [position, False, "failing mod check"]
        
    #players need 1 hour available a day, 3 hours available for 4 days
    sevenDayCount = 0
    fourDayCount = 0    
    i = 0

    for item in week:
        if i % 2 != 0:
            if item >= 2:
                sevenDayCount += 1
            if item >= 6:
                fourDayCount += 1
        
        i += 1

    if position[1] == 1:
        if sevenDayCount == 7 and fourDayCount >= 4:
            return [position, True, "passed"]
        elif sevenDayCount != 7 and fourDayCount < 4:
            return [position, False, "failing both time requirements"]
        elif sevenDayCount != 7:
            return [position, False, "failing 7 day requirement"]
        elif fourDayCount < 4:
            return [position, False, "failing 4 day requirement"]

    elif position[1] == 2:
        if score >= 7:
            return [position, True, "passed"]
        else: 
            return [position, False, "failing score"]
    
    elif position[1] == 3:
        canBeSpec = False
        canBePlay = False

        if score >= 7:
            canBeSpec = True

        if sevenDayCount == 7 and fourDayCount >= 4:
            canBePlay = True
        elif sevenDayCount != 7 and fourDayCount < 4:
            failCode = 0
        elif sevenDayCount != 7:
            failCode = 1
        elif fourDayCount < 4:
            failCode = 2

        if canBeSpec == True and canBePlay == True:
            return [position, True, "passed"]
        elif canBeSpec == True:
            if failCode == 0:
                return [["Spectator", 2], True, "failing both time requirements"]
            elif failCode == 1:
                return [["Spectator", 2], True, "failing both 7 day requirement"]
            elif failCode == 2:
                return [["Spectator", 2], True, "failing both 4 day requirement"]
        elif canBePlay == True:
            return [["Player", 1], True, "failing score"]
        else:
            return [position, False, "failing score and time"]

#Outputs all players
def search(entries):
    while (True):
        found = False

        outputLine("View")

        print("\n1. All")
        print("2. Name Search")
        print("3. Score Search")
        print("4. Players")
        print("5. Spectators")
        print("6. Hybrids")
        print("0. Exit View\n")
        
        operation = int(input("Enter command: "))

        #view all
        if operation == 1:
            outputLine("All: " + str(len(entries)))
            
            for entry in entries:
                print(entry)
                found = True

        #name search
        elif operation == 2:
            searchTerm = input("Keyword: ")
            
            outputLine("Name Search: " + searchTerm)
            
            print("")

            for entry in entries:
                if searchTerm.upper() in entry.name.upper():
                    print(entry.name)
                    found = True

        #score search
        elif operation == 3:
            scoreThreshold = int(input("Enter minimum score: "))

            outputLine("Score: " + str(scoreThreshold) + "+")

            print("")

            for entry in entries:
                if entry.score >= scoreThreshold:
                    print(entry.name + " (" + str(entry.score) + ")")
                    found = True

        #role search
        elif operation >= 4 and operation <= 6:
            if operation == 4:
                outputLine("Players")
                posID = 1
            elif operation == 5:
                outputLine("Spectators")
                posID = 2
            elif operation == 5:
                outputLine("Hybrids")
                posID = 3
            
            for entry in entries:
                if entry.position[1] == posID or entry.position[1] == 3:
                    print(entry)
                    found = True
        
        #exit
        elif operation == 0:
            return

        else:
            print("Invalid input")
            found = True

        if (found != True):
            print("No entries found.")

def reorder(entries):
    # entry is a list {p1, p2, p3}
    # need to reorder list to be order by score
    count = len(entries)

    # while (count



#Object for individual players
class Entry(object):
    #initializing all of the applicant's information
    def __init__(self, timestamp, name, position, score, schedule, timezone, country, specials, servers):
        self.timestamp = timestamp

        self.name = name

        self.position = position

        self.score = score

        self.country = country

        self.timezone = timezone
        
        self.specials = specials

        self.schedule = schedule

        self.servers = servers

    #default player print statement
    def __str__(self):
        Name = "\nName: " + self.name + "\n"
        
        Position = "Position: " + self.position[0] + "\n"
        
        Score = "Score: " + str(self.score) + "\n"

        Location = "Location: " + self.timezone + ", " + self.country + "\n"

        Atlanta = "  Atl: " + str(self.servers[0])
        Dallas =  "  Dal: " + str(self.servers[1])
        Fremont = "  Fre: " + str(self.servers[2])
        London = "  Ldn: " + str(self.servers[3])
        Newark = "  New: " + str(self.servers[4])
        Singapore = "  Sgp: " + str(self.servers[5])
        Sydney = "  Syd: " + str(self.servers[6])

        Servers = "Servers: \n" + Atlanta + Dallas + Fremont + "\n" + London + Newark + Singapore + "\n" + Sydney + "\n"

        Specials = "Special: " + self.specials + "\n"

        Timestamp = "Submission: " + self.timestamp

        Statement = Name + Position + Score + Location + Servers + Specials + Timestamp

        return Statement

### START OF ENTRY SPLITTING ###
with open("responses.csv", 'r') as responses:
    responses = csv.reader(responses)
    userResponses = []
    i = 0

    for line in responses:
        if i > 0:
            userResponses += [line]
        
        i += 1

entries = []
outputLine("Startup Statistics")
print("")

for entry in userResponses:
    fCheck = entry[0]
    mCheck = entry[1]
    
    timestamp = entry[2]
    name = entry[3]
    posID = entry[4]
    score = scoreCount(entry[5])

    #schedules
    sun = entry[6].split(", ")
    mon = entry[7].split(", ")
    tue = entry[8].split(", ")
    wed = entry[9].split(", ")
    thu = entry[10].split(", ")
    fri = entry[11].split(", ")
    sat = entry[12].split(", ")
    week = [sun, len(sun), mon, len(mon), tue, len(tue), wed, len(wed), thu, len(thu), fri, len(fri), sat, len(sat)]

    timezone = entry[13] 
    country = entry[14]
    specials = entry[15] 

    #servers
    atl = entry[16]
    dal = entry[17]
    fre = entry[18]
    ldn = entry[19]
    new = entry[20]
    sgp = entry[21]
    syd = entry[22]
    servers = serverRank(atl, dal, fre, ldn, new, sgp, syd)
    
    #entry inspection
    check = entryCheck(fCheck, mCheck, posID, score, week)

    position = check[0]
    approved = check[1]
    statement = check[2]

    application = Entry(timestamp, name, position, score, week, timezone, country, specials, servers)

    if approved == True:
        entries.append(application)
    
    if approved == True and statement != "passed":
        print(name + " changed to " + position[0] + " for " + statement)
    elif approved == False:
        print(name + " removed for " + statement)
### END OF ENTRY SPLITTING ###

### START OF MORE STATISTICS ###
totApplications = i - 1
players = []
spectators = []
hybrids = []

for entry in entries:
    if entry.position[1] == 1:
        players.append(entry)
    elif entry.position[1] == 2:
        spectators.append(entry)
    if entry.position[1] == 3:
        players.append(entry)
        hybrids.append(entry)
        spectators.append(entry)

# players = reorder(players)
# spectators = reorder(spectators)

print("\nTotal Applications: " + str(totApplications))
print("Total Approved: " + str(len(entries)))
print("Players: " + str(len(players)))
print("Spectators: " + str(len(spectators)))
print("Hybrids: " + str(len(hybrids)))
### END OF MORE STATISTICS ###

#Command Line UI 
while (True):
    outputLine("Home")
    print("\n1. View Entries")
    print("2. Matchmake")
    print("0. Exit Program\n")

    operation = int(input("Enter command: "))
    
    if operation == 1:
        search(entries)
    elif operation == 2:
        print("\nPending.")
    elif operation == 0:
        print("Exiting program...")
        break
    else:
        print("Invalid input")

    