from replit import db
from replit import clear
from time import sleep
from colorama import Fore
import os
from replit import Database
import sys
from datetime import datetime
import pytz
import random

tz = pytz.timezone('America/New_York')

t = db # Gets rid of the green underline on line 16
database_url = "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2NDU4MjIwNjUsImlhdCI6MTY0NTcxMDQ2NSwiZGF0YWJhc2VfaWQiOiJiZGJhY2Q3OC1hYjZlLTQ1ZWYtYTdiZS0zYTBlZGY3YWJmMzgifQ.iOMFTmGHqVsfKetsVeykAQJz6BcBooa1qmWw2o8zpw_2lNTA9Q0mZUC_SsRKUkNrp11mUOckD5sLzZ12LddsEg"
db = Database(db_url=database_url)

updateurl = False
if updateurl == True:
  print(os.getenv("REPLIT_DB_URL"))
  exit()

print("If you get a big error trying to login/sign up, I need to update the db url, I will notice and do it soon")
print("Press enter to continue")
i = input("")

red = Fore.RED
cyan = Fore.CYAN
green = Fore.LIGHTGREEN_EX
dark_green = Fore.GREEN
yellow = Fore.LIGHTYELLOW_EX
reset = Fore.RESET

def typePrint(text, textSpeed):
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    sleep(textSpeed)

ts = 0.1
mts = 0.05

resetleaderboards = False
if resetleaderboards == True:
  db["1stplacename"] = None
  db["1stplaceWLratio"] = 0
  db["2ndplacename"] = None
  db["2ndplaceWLratio"] = 0
  db["3rdplacename"] = None
  db["3rdplaceWLratio"] = 0

while True:
    clear()
    refresh = False
    loggingin = False
    print(red + "*****************")
    print("*               *")
    print("* " + dark_green +  "Interrogation" + cyan + " *")
    print("*               *")
    print("*****************")
    typePrint(reset + "\n[1] Login\n[2] Create Account\n", mts)
    i = input("")
    if i == "2":
        clear()
        typePrint("What will be your username?\n", mts)
        i = input("")
        if i in db.keys():
            clear()
            typePrint(red + "This username already exists" + reset, mts)
            sleep(2)
        else:
            username = i
            typePrint("What will be your password?\n", mts)
            i = input("")
            db[username] = i
            clear()
            db[username + "friends"] = []
            db[username + "wins"] = 0
            db[username + "playedmatches"] = 0
            db[username + "requests"] = []
            db[username + "play?"] = None
            db[username + "messages"] = []
            db[username + "openmessages?"] = False
            db[username + "blockedusers"] = []
            db[username + "namecolors"] = ["Cyan"]
            db[username + "namecolor"] = Fore.CYAN
            db[username + "namevaribles"] = [Fore.CYAN]
            db[username + "winscreen"] = "You Won!"
            db[username + "losescreen"] = "You Lost!"
            db[username + "coins"] = 0
            db[username + "title"] = ""
            db[username + "winscreens"] = ["You Won!"]
            db[username + "losescreens"] = ["You Lost!"]
            db[username + "titles"] = []
            db["userlist"].append(username)
            typePrint(green + "Account Created!" + reset, mts)
            sleep(2)
    elif i == "1":
        clear()
        typePrint("Username:\n", mts)
        i = input("")
        for x in db.keys():
          if i == x:
            loggingin = True
            clear()
            username = i
            typePrint("Password:\n", mts)
            i = input("")
            if i == db[username]:
                while True:
                    clear()
                    if len(db[username + "requests"]) > 0:
                        typePrint("You have a challenge from " + db[db[username + "requests"][0].split()[0] + "namecolor"] +
                              db[username + "requests"][0].split()[0] + reset + "\n", mts)
                        typePrint("\n[1] Accept\n[2] Deny\n", mts)
                        i = input("")
                        while True:
                            if i == "2":
                                db[username + "play?"] = False
                                clear()
                                db[username + "requests"].pop(0)
                                typePrint(red + "Request Declined" + reset, mts)
                                sleep(2)
                                db[username + "play?"] = None
                                break
                            elif i == "1":
                                server = db[username +
                                            "requests"][0].split()[1]
                                db[username + "requests"].pop(0)
                                db[username + "play?"] = True
                                end = False
                                db[server + "turn"] = "home"
                                db[server + "sd"] = False
                                while True:
                                    db[server + "aready"] = False
                                    while db[server + "reset"] == False:
                                        clear()
                                        print("Loading.")
                                        sleep(0.5)
                                        clear()
                                        print("Loading..")
                                        sleep(0.5)
                                        clear()
                                        print("Loading...")
                                        sleep(0.5)
                                    db[server + "aready"] = True
                                    if db[server + "turn"] == "home":
                                        while db[server + "hq"] == None:
                                            clear()
                                            print("Waiting for question.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for question..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for question...")
                                            sleep(0.5)
                                        db[server + "aready"] = False
                                        clear()
                                        typePrint(db[db[server + "homename"] + "namecolor"] + db[server + "homename"] + reset +
                                              " asked:\n" + db[server + "hq"] + "\n", ts)
                                        typePrint("What's you answer?\n", ts)
                                        i = input("")
                                        db[server + "ar"] = i
                                        while db[server + "rw"] == None:
                                            clear()
                                            print("Waiting for opponent.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent...")
                                            sleep(0.5)
                                        if db[server + "rw"] == "home":
                                            clear()
                                            typePrint(
                                                  "Your answer was " + red + "incorrect" +
                                                  reset, ts)
                                            sleep(3)
                                            if db[server + "sd"] == True:
                                                clear()
                                                typePrint(red + db[db[server + "homename"] + "losescreen"] +
                                                      reset, ts)
                                                sleep(2)
                                                end = True
                                                break
                                            else:
                                                clear()
                                                typePrint(red +
                                                      "You are now at risk" +
                                                      reset, ts)
                                                db[server + "sd"] = True
                                                sleep(2)
                                        else:
                                            clear()
                                            typePrint(
                                                  "Your answer was " + green + "correct" +
                                                  reset, ts)
                                            sleep(2)
                                            if db[server + "sd"]:
                                                typePrint(
                                                    green +
                                                    "You are no longer at risk"
                                                    + reset, ts)
                                                sleep(3)
                                    else:
                                        clear()
                                        typePrint("Ask your question\n", ts)
                                        i = input("")
                                        db[server + "aq"] = i
                                        while db[server + "hr"] == None:
                                            clear()
                                            print("Waiting for opponent.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent...")
                                            sleep(0.5)
                                        clear()
                                        typePrint(db[db[server + "homename"] + "namecolor"] + db[server + "homename"] + reset +
                                              " said:\n" + db[server + "hr"] + reset + "\n", ts)
                                        typePrint("Is the answer correct?\n", ts)
                                        typePrint("\n[1] Correct\n[2] Incorrect\n", ts)
                                        i = input("")
                                        if i == "1":
                                            if db[server + "sd"] == True:
                                                clear()
                                                typePrint(red + db[db[server + "homename"] + "losescreen"] +
                                                      reset, ts)
                                                db[server + "rw"] = "home"
                                                sleep(2)
                                                end = True
                                                break
                                            else:
                                                clear()
                                                typePrint("Opponent is correct", ts)
                                                db[server + "rw"] = "home"
                                                sleep(2)
                                        else:
                                            if not db[server + "sd"]:
                                                clear()
                                                typePrint(green + db[username + "winscreen"] +
                                                      reset, ts)
                                                db[server + "rw"] = "away"
                                                sleep(2)
                                                end = True
                                                break
                                            else:
                                                clear()
                                                typePrint(
                                                    yellow +
                                                    "Both players got the question wong, " +
                                                    "you are no longer at risk."
                                                    + reset, ts)
                                                db[server + "rw"] = "away"
                                                sleep(4)
                                                db[server + "sd"] = False
                            if end:
                                db[server + "hready"] = False
                                db[server + "aready"] = False
                                db[server + "rw"] = None
                                db[server + "hq"] = None
                                db[server + "aq"] = None
                                db[server] = False
                                break
                    while True:
                        clear()
                        if refresh == True:
                          refresh = False
                          break
                        print(
                            "Welcome " + db[username + "namecolor"] + username + reset +
                            "!\nVersion 8.0.0 - Added the ability to have a random opponent\nHave a bug report? A suggestion? Add me to your friends list and message me! Username: Dylan\n\n[1] Play Online\n[2] Search Players\n[3] View Stats\n[4] Reload\n[5] Leaderboards\n[6] Friends List\n[7] Messages (" + str(len(db[username + "messages"])) + ")\n[8] Account Settings\n[9] Shop\n[10] Inventory\n[11] Quit\n\n[?] How to play"
                        )
                        i = input("")
                        if i == "20":
                            clear()
                            i = input("")
                            if i == os.environ['pass']:
                                db["s1iu"] = False
                                db["s2iu"] = False
                                db["s3iu"] = False
                                db["queue"] = []
                                db["queuefinish"]
                                clear()
                                print("servers reset")
                                sleep(2)
                        elif i == "11":
                          clear()
                          typePrint("Bye!\n", mts)
                          exit()
                        elif i == "9":
                          clear()
                          while True:
                            clear()
                            typePrint("Shop\n" + Fore.LIGHTYELLOW_EX + str(db[username + "coins"]) + reset + " coins\n\n", mts)
                            print("[1] Username Colors\n[2] Win screens\n[3] Loss screens\n[4] Titles\n[5] Gamble\n\n[-1] Back")
                            i = input("")
                            if i == "-1":
                              break
                            elif i == "1":
                              while True:
                                clear()
                                print("Shop - Username Colors\nChanges the color of your username\n" + Fore.LIGHTYELLOW_EX + str(db[username + "coins"]) + reset + " coins\n\n[1] " + Fore.BLACK + "Black" + reset + " - 3 coins\n[2] White - 3 coins\n[3] " + Fore.RED + "Red" + reset + " - 5 coins\n[4] " + Fore.LIGHTYELLOW_EX + "Yellow" + reset + " - 5 coins\n[5] " + Fore.MAGENTA + "Magenta" + reset + " - 5 coins\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  buy = True
                                  for color in db[username + "namecolors"]:
                                    if color == "Black":
                                      buy = False
                                  if db[username + "coins"] >= 3 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the black username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "coins"] -= 3
                                      db[username + "namecolors"].append("Black")
                                      db[username + "namevaribles"].append(Fore.BLACK)
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                                elif i == "2":
                                  buy = True
                                  for color in db[username + "namecolors"]:
                                    if color == "White":
                                      buy = False
                                  if db[username + "coins"] >= 3 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the white username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "coins"] -= 3
                                      db[username + "namecolors"].append("White")
                                      db[username + "namevaribles"].append("")
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)  
                                elif i == "3":
                                  buy = True
                                  for color in db[username + "namecolors"]:
                                    if color == "Red":
                                      buy = False
                                  if db[username + "coins"] >= 5 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the red username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "coins"] -= 5
                                      db[username + "namecolors"].append("Red")
                                      db[username + "namevaribles"].append(Fore.RED)
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                                elif i == "4":
                                  buy = True
                                  for color in db[username + "namecolors"]:
                                    if color == "Yellow":
                                      buy = False
                                  if db[username + "coins"] >= 5 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the yellow username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "coins"] -= 5
                                      db[username + "namecolors"].append("Yellow")
                                      db[username + "namevaribles"].append(Fore.LIGHTYELLOW_EX)
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                                elif i == "5":
                                  buy = True
                                  for color in db[username + "namecolors"]:
                                    if color == "Magenta":
                                      buy = False
                                  if db[username + "coins"] >= 5 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the magenta username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "coins"] -= 5
                                      db[username + "namecolors"].append("Magenta")
                                      db[username + "namevaribles"].append(Fore.MAGENTA)
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                            elif i == "2":
                              while True:
                                clear()
                                print("Shop - Win Screens\nChanges the text of the win screen\n" + Fore.LIGHTYELLOW_EX + str(db[username + "coins"]) + reset + " coins\n\n[1] Add a new win screen - 5 coins\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  clear()
                                  typePrint("What do you want your win screen to be? (25 character limit)\n", mts)
                                  i = input("")
                                  if len(i) > 25:
                                    clear()
                                    typePrint(red + "You cannot go over 25 characters" + reset, mts)
                                    sleep(2)
                                  else:
                                    clear()
                                    pwinscreen = i
                                    print("Are you sure you would like to buy this win screen?\n" + pwinscreen + "\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "winscreens"].append(pwinscreen)
                                      db[username + "coins"] -= 5
                                      clear()
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                            elif i == "3":
                              while True:
                                clear()
                                print("Shop - Loss Screens\nChanges the text of your opponents loss screen\n" + Fore.LIGHTYELLOW_EX + str(db[username + "coins"]) + reset + " coins\n\n[1] Add a new loss screen - 10 coins\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  clear()
                                  typePrint("What do you want your loss screen to be? (25 character limit)\n", mts)
                                  i = input("")
                                  if len(i) > 25:
                                    clear()
                                    typePrint(red + "You cannot go over 25 characters" + reset, mts)
                                    sleep(2)
                                  else:
                                    clear()
                                    pwinscreen = i
                                    print("Are you sure you would like to buy this loss screen?\n" + pwinscreen + "\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "losescreens"].append(pwinscreen)
                                      db[username + "coins"] -= 10
                                      clear()
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                            elif i == "4":
                              while True:
                                clear()
                                print("Shop - Titles\nAdds a title next yo your username in your profile" + Fore.LIGHTYELLOW_EX + str(db[username + "coins"]) + reset + " coins\n\n[1] Add a new title - 7 coins\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  clear()
                                  typePrint("What do do you want your title to be? (15 character limit)\n", mts)
                                  i = input("")
                                  if len(i) > 15:
                                    clear()
                                    typePrint(red + "You cannot go over 15 characters" + reset, mts)
                                    sleep(2)
                                  else:
                                    clear()
                                    print("Choose a color\n\n[1] " + red + "Red" + reset + "\n[2] " + dark_green + "Green" + reset + "\n[3] " + cyan + "Cyan" + reset)
                                    pwinscreen = i
                                    i = input("")
                                    if i == "1":
                                      color = Fore.RED
                                    elif i == "2":
                                      color = Fore.GREEN
                                    elif i == "3":
                                      color = Fore.CYAN
                                    clear()
                                    print("Are you sure you would like to buy this title?\n" + color + pwinscreen + reset + "\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      db[username + "titles"].append(" - " + color + pwinscreen + reset)
                                      db[username + "coins"] -= 7
                                      clear()
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                            elif i == "5":
                              clear()
                              print("There is a 1 in 3 chance to double however many coins you bet, put in your bet or type -1 to go back\n" + Fore.LIGHTYELLOW_EX + str(db[username + "coins"]) + reset + "coins")
                              i = int(input())
                              if i == -1:
                                pass
                              elif i > db[username + "coins"]:
                                clear()
                                typePrint("You do not have enough coins for that", mts)
                                sleep(2)
                              else:
                                clear()
                                bet = i
                                winamount = bet * 2
                                number = random.randint(1, 3)
                                db[username + "coins"] -= bet
                                if number == 2:
                                  db[username + "coins"] += winamount
                                  print("You won the bet!\n" + Fore.LIGHTYELLOW_EX + str(winamount) + reset + " coins earned!")
                                  sleep(2)
                                else:
                                  print("You lost the bet, better luck next time")
                                  sleep(2)
                        elif i == "10":
                          clear()
                          print("Inventory\n\n[1] Username Colors\n[2] Win screens\n[3] Loss screens\n[4] Titles\n\n[-1] Back")
                          i = input("")
                          if i == "1":
                            while True:
                              if not len(db[username + "namecolors"]) < 1:
                                clear()
                                count = 0
                                print("Inventory - Name Colors\nCurrently Equipped: " + db[username + "namecolor"] + username + reset)
                                for x in db[username + "namecolors"]:
                                  print("[" + str(count) + "] " + x)
                                  count += 1
                                print("\n[-1] Back")
                                i = int(input())
                                if i == -1:
                                  break
                                else:
                                  db[username + "namecolor"] = db[username + "namevaribles"][i]
                          elif i == "2":
                            while True:
                              clear()
                              print("Inventory - Win Screens\nSelected: " + db[username + "winscreen"] + "\n\n")
                              count = 0
                              for x in db[username + "winscreens"]:
                                print("[" + str(count) + "] " + x)
                                count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              else:
                                db[username + "winscreen"] = db[username + "winscreens"][i]
                          elif i == "3":
                            while True:
                              clear()
                              print("Inventory - Lose Screens\nSelected: " + db[username + "losescreen"] + "\n\n")
                              count = 0
                              for x in db[username + "losescreens"]:
                                print("[" + str(count) + "] " + x)
                                count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              else:
                                db[username + "losescreen"] = db[username + "losescreens"][i]
                          elif i == "4":
                            while True:
                              clear()
                              if len(db[username + "titles"]) < 1:
                                typePrint("You have no titles", mts)
                                sleep(2)
                                break
                              print("Inventory - Titles\nSelected: " + db[username + "title"] + "\n\n[0] None")
                              count = 1
                              for x in db[username + "titles"]:
                                print("[" + str(count) + "]" + x)
                                count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              elif i == 0:
                                db[username + "title"] = ""
                              else:
                                db[username + "title"] = db[username + "titles"][i - 1]
                        elif i == "?":
                          clear()
                          print("How to play: Player 1 asks player 2 a quiz question (not a personal question) If player 2 gets it wrong, they are at risk, player 2 asks player 1 a question, if they get it right, the game continues, but if player 2 was at risk, player 1 wins. Both players get it wrong? game continues. Player 1 gets it wrong without player 2 being at risk? Player 2 wins.\n\n[-1] Back")
                          i = input("")
                          if i == "-1":
                            pass
                        elif i == "8":
                          while True:
                            clear()
                            typePrint("[1] DM Settings\n[2] Blocked Users\n\n[-1] Back\n", mts)
                            i = input("")
                            if i == "-1":
                              break
                            elif i == "1":
                              while True:
                                clear()
                                print("People who can DM you:")
                                if db[username + "openmessages?"] == False:
                                  print("Friends Only")
                                else:
                                  print("Everyone")
                                print("\n[1] Friends Only\n[2] Everyone\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  db[username + "openmessages?"] = False
                                elif i == "2":
                                  db[username + "openmessages?"] = True
                            elif i == "2":
                              while True:
                                clear()
                                count = 0
                                if len(db[username + "blockedusers"]) == 0:
                                  clear()
                                  typePrint("You have no one blocked", mts)
                                  sleep(2)
                                  break
                                for x in db[username + "blockedusers"]:
                                  print("[" + str(count) + "] " + db[x + "namecolor"] + x + reset)
                                print("\n[-1] Back")
                                i = int(input(""))
                                if i == -1:
                                  break
                                elif not i < 0 and i < len(db[username + "blockedusers"]):
                                  clear()
                                  index = i
                                  typePrint("What would you like to do with this user?\n\n[1] Unblock\n\n[-1] Back\n", mts)
                                  i = input("")
                                  if i == "-1":
                                    break
                                  elif i == "1":
                                    clear()
                                    db[username + "blockedusers"].pop(index)
                                    typePrint("User unblocked", mts)
                                    sleep(2)
                                    break
                        elif i == "7":
                          clear()
                          count = 0
                          if len(db[username + "messages"]) < 1:
                            typePrint("You have no messages", mts)
                            sleep(2)
                            break
                          for x in db[username + "messages"]:
                            print("[" + str(count) + "] " + db[username + "messages"][count])
                            count += 1
                          print("[-1] Back\n[-2] Clear messages\n")
                          i = int(input())
                          if i == -1:
                            break
                          if i == -2:
                            clear()
                            db[username + "messages"] = []
                            typePrint("Messages Cleared", mts)
                            sleep(2)
                            break
                          if not i > len(db[username + "messages"]) - 1:
                            clear()
                            mindex = i
                            message = db[username + "messages"][mindex]
                            print("What do you want to do with this message?\n\n[1] Reply\n[2] Delete Message\n[3] Block User\n")
                            i = input("")
                            if i == "1":
                              clear()
                              for x in db[message.split()[0] + "friends"]:
                                if username == x:
                                  fadded = True
                              if not fadded == True and db[message.split()[0] + "openmessages?"] == False:
                                clear()
                                typePrint(red + "This player does not have you added and does not have open messages" + reset, mts)
                                sleep(2)
                                break
                              for x in db[message.split()[0] + "blockedusers"]:
                                if username == x:
                                  clear()
                                  typePrint(red + "This user has you blocked" + reset, mts)
                                  sleep(2)
                                break
                              print("Type your mesage, -1 to go back\n")
                              i = input("")
                              if i == "-1":
                                break
                              else:
                                clear()
                                now = datetime.now(tz)
                                db[message.split()[0] + "messages"].append(username + " (" + now.strftime("%m/%d/%Y %H:%M") + ") - " + i) 
                                typePrint("Message sent to " + db[message.split()[0] + "namecolor"] + message.split()[0] + reset, mts)
                                db[username + "messages"].pop(mindex)
                                sleep(2)
                            elif i == "3":
                              db[username + "blockedusers"].append(message.split()[0])
                            elif i == "2":
                              clear() 
                              db[username + "messages"].pop(mindex)
                              typePrint("Message Deleted", mts)
                              sleep(2)
                        elif i == "6":
                          while True:
                            clear()
                            count = 0
                            if len(db[username + "friends"]) < 1:
                              typePrint(red + "You dont have any friends D:" + reset, mts)
                              sleep(2)
                              break
                            for a in db[username + "friends"]:
                              print("[" + str(count) + "] " + db[a + "namecolor"] + a + reset)
                              count = count + 1
                            typePrint("\n\n[-1] Back\n[-2] Other people that have me added\n", mts)
                            i = int(input())
                            if i == -1:
                              break
                            elif i == -2:
                              clear()
                              print("Loading")
                              people = []
                              for user in db.keys():
                                if "wins" in user and not "winscreen" in user and not "winscreens" in user:
                                  name = user.replace('wins', '')
                                  listperson = True
                                  for friend in db[name + "friends"]:
                                    if username == friend:
                                      for person in db[username + "friends"]:
                                        if person == name:
                                          listperson = False
                                          break
                                      if listperson == True:
                                        people.append(name)
                                        break
                              if len(people) > 0:
                                clear()
                                count = 0
                                for x in people:
                                  print("[" + str(count) + "] " + db[x + "namecolor"] + x + reset)
                                  count += 1
                                print("\n[-1] Back")
                                i = int(input())
                                if i == -1:
                                  clear()
                                else:
                                  name = people[i]
                                  clear()
                                  print(db[name + "namecolor"] + name + reset + "\n\n\nWins - " + str(db[name + "wins"]) + "\n\nLosses - " + str(db[name + "playedmatches"]) + "\n\n[1] Add friend\n\n[-1] Back")
                                  i = input("")
                                  if i == "1":
                                    clear()
                                    canadd = True
                                    for user in db[username + "friends"]:
                                      if name == user:
                                        clear()
                                        typePrint(red + "You already have this person added" + reset, mts)
                                        canadd = False
                                        sleep(2)
                                        break
                                    if canadd == False:
                                      break
                                    clear()
                                    db[username + "friends"].append(name)
                                    typePrint(green + "Friend added" + reset, mts)
                                    sleep(2)
                              else:
                                clear()
                                typePrint("No one else has you added", mts)
                                sleep(2)
                            elif not i > len(db[username + "friends"]) - 1 and not i < 0:
                              clear()
                              findex = i
                              fname = db[username + "friends"][findex]
                              print("Options for " + db[fname + "namecolor"] + db[username + "friends"][i] + reset + "\n\n[1] Message Player\n[2] Remove Friend\n[3] Block User\n\n[-1] Back\n")
                              i = input("")
                              if i == "-1":
                                print("")
                              elif i == "1":
                                if not username in db[fname + "friends"] and db[fname + "openmessages?"] == False:
                                  clear()
                                  typePrint(red + "This player does not have you added and does not have open DMs on" + reset, mts)
                                  sleep(2)
                                  break
                                clear()
                                print("Type your mesage, -1 to go back\n")
                                i = input("")
                                if i == "-1":
                                  break
                                else:
                                  clear()
                                  now = datetime.now(tz) 
                                  db[fname + "messages"].append(username + " (" + now.strftime("%m/%d/%Y %H:%M") + ") - " + i)
                                  typePrint("Message sent to " + db[db[username + "friends"][findex] + "namecolor"] + db[username + "friends"][findex] + reset, mts)
                                  sleep(2)
                              elif i == "2":
                                db[username + "friends"].pop(findex)
                                clear()
                                typePrint("Friend Removed", mts)
                                sleep(2)
                              elif i == "3":
                                db[username + "blockedusers"].append(db[username + "friends"][findex])
                                db[username + "friends"].pop(findex)
                                clear()
                                typePrint("User Blocked", mts)
                                sleep(2)
                            else:
                              clear()
                              typePrint(red + "Invalid input" + reset, mts)
                              sleep(2)
                        elif i == "5":
                          while True:
                            clear()
                            users = []
                            count = 0
                            print("Loading")
                            for user in db.keys():
                              if "wins" in user and not "winscreen" in user and not "winscreens" in user:
                                name = user.replace('wins', '')
                                rounds = db[name + "wins"] + db[name + "playedmatches"]
                                uwins = db[name + "wins"]
                                ulosses = db[name + "playedmatches"]
                                tlosses = db[name + "playedmatches"]
                                users.append([])
                                if ulosses == 0:
                                  tlosses = 1
                                wlratio = rounds * (uwins/tlosses)
                                twlratio = round(uwins/tlosses, 2)
                                users[count].append(round(wlratio, 2))
                                users[count].append(name)
                                users[count].append(rounds)
                                users[count].append(twlratio)
                                count += 1
                            p=1
                            users.sort()
                            clear()
                            for i in range(len(users)-1,-1,-1):
                              if not p > 5:
                                if p == 1:
                                  suffix = "st"
                                elif p == 2:
                                  suffix = "nd"
                                elif p == 3:
                                  suffix = "rd"
                                elif p == 4 or p == 5:
                                  suffix = "th"
                                print(f"{p}{suffix} Place.......... {users[i][1]} - {users[i][0]} points ({users[i][2]} total rounds played, {users[i][3]} win loss ratio)\n")
                                p+=1
                            print("\n[1] Point System\n\n[-1] Back")
                            i = input("")
                            if i == "-1":
                              break
                            elif i == "1":
                              while True:
                                clear()
                                print("points = total rounds played * win loss ratio rounded to the nearest hundreth\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                        elif i == "9":
                          while True:
                            clear()
                            for user in db.keys():
                              if "wins" in user and not "winscreen" in user and not "winscreens" in user:
                                name = user.replace('wins', '')
                                print(name)
                            i = input("")
                            if i == "-1":
                              break
                        elif i == "3":
                            while True:
                                clear()
                                rounds = db[username + "wins"] + db[username + "playedmatches"]
                                points = rounds * (db[username + "wins"] / db[username + "playedmatches"])
                                print(db[username + "namecolor"] + username + reset + db[username + "title"] +
                                      "\n\nRounds won - " +
                                      str(db[username + "wins"]) +
                                      "\n\nRounds lost - " +
                                      str(db[username + "playedmatches"]) + "\n\n" + str(round(points, 2)) + " points\n" +
                                      "\n[1] Point System\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                    break
                                elif i == "1":
                                  while True:
                                    clear()
                                    print("points = total rounds played * win loss ratio rounded to the nearest hundreth\n\n[-1] Back")
                                    i = input("")
                                    if i == "-1":
                                      break
                        elif i == "4":
                            break
                        elif i == "2":
                            clear()
                            typePrint("Player Search\n\n", mts)
                            i = input("")
                            clear()
                            found_users = []
                            count = 0
                            while True:
                              for user in db.keys():
                                if i in user:
                                    if "wins" in user and not "winscreen" in user and not "winscreens" in user:
                                          name = user.replace('wins', '')
                                          found_users.append(name)
                                          print("[" + str(count) + "]" + db[name + "namecolor"] + " " + found_users[count] + reset)
                                          count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              elif not i > len(found_users) and not i < 0:
                                clear()
                                name = found_users[i]
                                print(db[name + "namecolor"] + name + reset + db[name + "title"] + "\n\n\nRounds Won - " + str(db[name + "wins"]) + "\n\nRounds Lost - " + str(db[name + "playedmatches"]) + "\n\n[1] Add friend\n\n[-1] Back")
                                i = input("")
                                if i == "1":
                                  clear()
                                  if not name in db[username + "friends"]:
                                    if name == username:
                                      typePrint(red + "Don't." + reset, ts)
                                      sleep(2)
                                      break
                                    db[username + "friends"].append(name)
                                    typePrint(green + "Friend added" + reset, mts)
                                    sleep(2)
                                    break
                                  else:
                                    clear()
                                    typePrint(red + "You already have this person added" + reset, mts)
                                    sleep(2)
                                    break
                                elif i == "-1":
                                  break
                        elif i == "1":
                            clear()
                            typePrint("Who would you like to play?\n", mts)
                            count = 0
                            for a in db[username + "friends"]:
                                print("[" + str(count) + "] " + db[a + "namecolor"] + a + reset)
                                count = count + 1
                            typePrint("[-1] Back\n[-2] Random opponent (BETA)\n", mts)
                            i = int(input())
                            if i == -1:
                                break
                            elif i == -2:
                              while True:
                                clear()
                                if len(db["queue"]) > 1:
                                  clear()
                                  typePrint("A game is starting, try again in a second")
                                  sleep(2)
                                  break
                                if not db["s1iu"] == True:
                                  server = "s1iu"
                                elif not db["s2iu"] == True:
                                  server = "s2iu"
                                elif not db["s3iu"] == True:
                                  server = "s3iu"
                                else:
                                  clear()
                                  typePrint("Servers are full right now, try again later")
                                if True:
                                  db["queue"].append(username)
                                  if len(db["queue"]) > 1:
                                    while not db["queuefinish"] == True:
                                      clear()
                                      print("Loading")
                                    refresh = True
                                    db["queuefinish"] = False
                                    break
                                  else:
                                    leave = False
                                    print("You are in the queue, wait 10 seconds and see if anyone joins")
                                    sleep(10)
                                    if len(db["queue"]) > 1:
                                      db[db["queue"][1] + "requests"].append(username + " " + server)
                                      away = db["queue"][1]
                                      db["queue"] = []
                                      db["queuefinish"] = True
                                      while db[away +
                                                 "play?"] == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)
                                      if db[away +
                                          "play?"] == True:
                                        db[server +
                                           "awayname"] = db[away]
                                        db[away +
                                           "play?"] = None
                                        db[server + "homename"] = username
                                        db[server + "sd"] = False
                                        db[server + "reset"] = False
                                        db[server] == True
                                        db[server + "turn"] = "away"
                                        while True:
                                            db[server + "hq"] = None
                                            db[server + "aq"] = None
                                            db[server + "hready"] = True
                                            db[server + "hr"] = None
                                            db[server + "ar"] = None
                                            db[server + "rw"] = None
                                            if db[server + "turn"] == "home":
                                                db[server + "turn"] = "away"
                                            else:
                                                db[server + "turn"] = "home"
                                            db[server + "reset"] = True
                                            while db[server +
                                                     "aready"] == False:
                                                clear()
                                                print("Waiting for opponent.")
                                                sleep(0.5)
                                                clear()
                                                print("Waiting for opponent..")
                                                sleep(0.5)
                                                clear()
                                                print(
                                                    "Waiting for opponent...")
                                                sleep(0.5)
                                            db[server + "reset"] = False
                                            if db[server + "turn"] == "home":
                                                clear()
                                                typePrint("Ask your question\n", ts)
                                                i = input("")
                                                db[server + "hq"] = i
                                                while db[server +
                                                         "ar"] == None:
                                                    clear()
                                                    print(
                                                        "Waiting for opponent."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent.."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent..."
                                                    )
                                                    sleep(0.5)
                                                clear()
                                                typePrint(db[db[server + "awayname"] + "namecolor"] + db[server + "awayname"] + reset +
                                                      " said:" + "\n" +
                                                      db[server + "ar"], ts)
                                                typePrint(
                                                    "\n\n[1] Correct\n[2] Incorrect\n", ts
                                                )
                                                i = input("")
                                                if i == "1":
                                                    db[server + "sd"] = False
                                                    clear()
                                                    typePrint(
                                                        "Opponent is correct", ts)
                                                    db[username +
                                                       "playedmatches"] += 1
                                                    db[db[server + "awayname"]
                                                       + "wins"] += 1
                                                    db[db[server + "awayname"]
                                                       + "coins"] += 1
                                                    db[server + "sd"] = False
                                                    db[server + "rw"] = "away"
                                                    sleep(2)
                                                else:
                                                    if db[server +
                                                          "sd"] == True:
                                                        db[server +
                                                           "winner"] = "home"
                                                        db[server +
                                                           "rw"] = "home"
                                                        clear()
                                                        typePrint(db[username + "winscreen"], ts)
                                                        db[db[server +
                                                              "awayname"] +
                                                           "playedmatches"] += 1
                                                        db[username +
                                                           "wins"] += 1
                                                        db[username +
                                                           "coins"] += 5
                                                        sleep(2)
                                                        break
                                                    else:
                                                        db[server +
                                                           "rw"] = "home"
                                                        clear()
                                                        typePrint(
                                                            green +
                                                            "You won this round, " +
                                                            "opponent is now at risk"
                                                            + reset, ts)
                                                        db[db[server +
                                                              "awayname"] +
                                                           "playedmatches"] += 1
                                                        db[username +
                                                           "wins"] += 1
                                                        sleep(2)
                                                        db[username +
                                                           "coins"] += 1
                                            else:
                                                while db[server +
                                                         "aq"] == None:
                                                    clear()
                                                    print(
                                                        "Waiting for question."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for question.."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for question..."
                                                    )
                                                    sleep(0.5)
                                                clear()
                                                typePrint(db[db[server + "awayname"] + "namecolor"] + db[server + "awayname"]  + reset +
                                                      " asked:\n" +
                                                      db[server + "aq"] + "\n", ts)
                                                typePrint("Type your answer\n", ts)
                                                i = input("")
                                                db[server + "hr"] = i
                                                while db[server +
                                                         "rw"] == None:
                                                    clear()
                                                    print(
                                                        "Waiting for opponent."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent.."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent..."
                                                    )
                                                    sleep(0.5)
                                                if db[server + "rw"] == "home":
                                                    clear()
                                                    typePrint(
                                                          "Your answer was " + green + "correct." +
                                                          reset, ts)
                                                    db[db[server + "awayname"]
                                                       + "playedmatches"] += 1
                                                    db[username + "wins"] += 1
                                                    db[username + "coins"] += 1
                                                    sleep(2)
                                                    if db[server +
                                                          "sd"] == True:
                                                        clear()
                                                        typePrint(green +
                                                              db[username + "winscreen"] +
                                                              reset, ts)
                                                        db[username + "coins"] += 5
                                                        sleep(2)
                                                        break
                                                else:
                                                    if db[server +
                                                          "sd"] == False:
                                                        clear()
                                                        typePrint(red +
                                                              db[db[server + "awayname"] + "losescreen"] +
                                                              reset, ts)
                                                        sleep(2)
                                                        db[username +
                                                           "playedmatches"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "wins"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "coins"] += 5
                                                        break
                                                    else:
                                                        clear()
                                                        typePrint(
                                                            "Your answer was " + red + "incorrect, " + reset +
                                                            "opponent is no longer at risk."
                                                            + reset, ts)
                                                        db[username +
                                                           "playedmatches"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "wins"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "coins"] += 1
                                                        sleep(5)
                                                        db[server +
                                                           "sd"] = False
                                      else:
                                        clear()
                                        typePrint(
                                            red +
                                            "The user declined your request" +
                                            reset, mts)
                                        db[away + "play?"] = None
                                        sleep(2)
                                        break
                                    else:
                                      clear()
                                      typePrint(red + "No users found" + reset, mts)
                                      sleep(2)
                                      break
                            else:
                              fname = db[username + "friends"][i]
                              canplay = False
                              for user in db[fname + "friends"]:
                                if username == user:
                                  canplay = True
                              for user in db[fname + "blockedusers"]:
                                if username == user:
                                  canplay = False
                              if not canplay == True:
                                clear()
                                typePrint(red + "This person does not have you added" + reset, mts)
                                sleep(2)
                                break
                              else:
                                if not len(db[db[username + "friends"][i] +
                                              "requests"]) > 0:
                                    if db["s1iu"] == False:
                                        server = "s1iu"
                                        db[db[username + "friends"][i] +
                                           "requests"].append(username + " " +
                                                              server)
                                        clear()
                                        sleep(2)
                                        while db[db[username + "friends"][i] +
                                                 "play?"] == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)
                                    elif db["s2iu"] == False:
                                        server = "s2iu"
                                        db[db[username + "friends"][i] +
                                           "requests"].append(username + " " +
                                                              server)
                                        while db[(username + "friends"[i]) +
                                                 "play?"] == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)
                                    elif db["s3iu"] == False:
                                        server = "s3iu"
                                        db[db[username + "friends"][i] +
                                           "requests"].append(username + " " +
                                                              server)
                                        while db[(username + "friends"[i]) +
                                                 "play?"] == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)            
                                    else:
                                        clear()
                                        typePrint(
                                            "Sorry, our servers the currently full, try again later.", mts
                                        )
                                        break
                                    if db[db[username + "friends"][i] +
                                          "play?"] == True:
                                        db[server +
                                           "awayname"] = db[username +
                                                            "friends"][i]
                                        db[db[username + "friends"][i] +
                                           "play?"] = None
                                        db[server + "homename"] = username
                                        db[server + "sd"] = False
                                        db[server + "reset"] = False
                                        db[server] == True
                                        db[server + "turn"] = "away"
                                        while True:
                                            db[server + "hq"] = None
                                            db[server + "aq"] = None
                                            db[server + "hready"] = True
                                            db[server + "hr"] = None
                                            db[server + "ar"] = None
                                            db[server + "rw"] = None
                                            if db[server + "turn"] == "home":
                                                db[server + "turn"] = "away"
                                            else:
                                                db[server + "turn"] = "home"
                                            db[server + "reset"] = True
                                            while db[server +
                                                     "aready"] == False:
                                                clear()
                                                print("Waiting for opponent.")
                                                sleep(0.5)
                                                clear()
                                                print("Waiting for opponent..")
                                                sleep(0.5)
                                                clear()
                                                print(
                                                    "Waiting for opponent...")
                                                sleep(0.5)
                                            db[server + "reset"] = False
                                            if db[server + "turn"] == "home":
                                                clear()
                                                typePrint("Ask your question\n", ts)
                                                i = input("")
                                                db[server + "hq"] = i
                                                while db[server +
                                                         "ar"] == None:
                                                    clear()
                                                    print(
                                                        "Waiting for opponent."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent.."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent..."
                                                    )
                                                    sleep(0.5)
                                                clear()
                                                typePrint(db[db[server + "awayname"] + "namecolor"] + db[server + "awayname"] + reset +
                                                      " said:" + "\n" +
                                                      db[server + "ar"], ts)
                                                typePrint(
                                                    "\n\n[1] Correct\n[2] Incorrect\n", ts
                                                )
                                                i = input("")
                                                if i == "1":
                                                    db[server + "sd"] = False
                                                    clear()
                                                    typePrint(
                                                        "Opponent is correct", ts)
                                                    db[username +
                                                       "playedmatches"] += 1
                                                    db[db[server + "awayname"]
                                                       + "wins"] += 1
                                                    db[db[server + "awayname"]
                                                       + "coins"] += 1
                                                    db[server + "sd"] = False
                                                    db[server + "rw"] = "away"
                                                    sleep(2)
                                                else:
                                                    if db[server +
                                                          "sd"] == True:
                                                        db[server +
                                                           "winner"] = "home"
                                                        db[server +
                                                           "rw"] = "home"
                                                        clear()
                                                        typePrint(db[username + "winscreen"], ts)
                                                        db[db[server +
                                                              "awayname"] +
                                                           "playedmatches"] += 1
                                                        db[username +
                                                           "wins"] += 1
                                                        db[username +
                                                           "coins"] += 5
                                                        sleep(2)
                                                        break
                                                    else:
                                                        db[server +
                                                           "rw"] = "home"
                                                        clear()
                                                        typePrint(
                                                            green +
                                                            "You won this round, " +
                                                            "opponent is now at risk"
                                                            + reset, ts)
                                                        db[db[server +
                                                              "awayname"] +
                                                           "playedmatches"] += 1
                                                        db[username +
                                                           "wins"] += 1
                                                        sleep(2)
                                                        db[username +
                                                           "coins"] += 1
                                            else:
                                                while db[server +
                                                         "aq"] == None:
                                                    clear()
                                                    print(
                                                        "Waiting for question."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for question.."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for question..."
                                                    )
                                                    sleep(0.5)
                                                clear()
                                                typePrint(db[db[server + "awayname"] + "namecolor"] + db[server + "awayname"]  + reset +
                                                      " asked:\n" +
                                                      db[server + "aq"] + "\n", ts)
                                                typePrint("Type your answer\n", ts)
                                                i = input("")
                                                db[server + "hr"] = i
                                                while db[server +
                                                         "rw"] == None:
                                                    clear()
                                                    print(
                                                        "Waiting for opponent."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent.."
                                                    )
                                                    sleep(0.5)
                                                    clear()
                                                    print(
                                                        "Waiting for opponent..."
                                                    )
                                                    sleep(0.5)
                                                if db[server + "rw"] == "home":
                                                    clear()
                                                    typePrint(
                                                          "Your answer was " + green + "correct." +
                                                          reset, ts)
                                                    db[db[server + "awayname"]
                                                       + "playedmatches"] += 1
                                                    db[username + "wins"] += 1
                                                    db[username + "coins"] += 1
                                                    sleep(2)
                                                    if db[server +
                                                          "sd"] == True:
                                                        clear()
                                                        typePrint(green +
                                                              db[username + "winscreen"] +
                                                              reset, ts)
                                                        db[username + "coins"] += 5
                                                        sleep(2)
                                                        break
                                                else:
                                                    if db[server +
                                                          "sd"] == False:
                                                        clear()
                                                        typePrint(red +
                                                              db[db[server + "awayname"] + "losescreen"] +
                                                              reset, ts)
                                                        sleep(2)
                                                        db[username +
                                                           "playedmatches"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "wins"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "coins"] += 5
                                                        break
                                                    else:
                                                        clear()
                                                        typePrint(
                                                            "Your answer was " + red + "incorrect, " + reset +
                                                            "opponent is no longer at risk."
                                                            + reset, ts)
                                                        db[username +
                                                           "playedmatches"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "wins"] += 1
                                                        db[db[server +
                                                              "awayname"] +
                                                           "coins"] += 1
                                                        sleep(5)
                                                        db[server +
                                                           "sd"] = False
                                    else:
                                        clear()
                                        typePrint(
                                            red +
                                            "The user declined your request" +
                                            reset, mts)
                                        sleep(2)
                                else:
                                    clear()
                                    typePrint(red +
                                          "The user already has a request" +
                                          reset, mts)
                                    sleep(2)
            else:
                clear()
                typePrint(red + "Your password is incorrect" + reset, mts)
                sleep(3)
        else:
          if not loggingin == True:
            clear()
            typePrint(red + "Account not found" + reset, mts)
            sleep(2)
          else:
            clear()
            loggingin = False