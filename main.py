from replit import clear
from time import sleep
from colorama import Fore
import os
import sys
from datetime import datetime
import pytz
import random
import socket
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
  
# Use a service account.
cred = credentials.Certificate('interrogation-376013-729a2ea8db0e.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

IPAddr = socket.gethostbyname(socket.gethostname())

tz = pytz.timezone('America/New_York')

callback_done = threading.Event()
def on_snapshot(doc_snapshot, changes, read_time):
  for doc in doc_snapshot:
    print("updated")
  callback_done.set()

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
  db.collection(u'Leaderboard').document(u'stats').set({
    u'1stPlaceName' : u'Empty',
    u'1stPlaceWLRatio' : 0,
    u'2stPlaceName' : u'Empty',
    u'2stPlaceWLRatio' : 0,
    u'3stPlaceName' : u'Empty',
    u'3stPlaceWLRatio' : 0
  })

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
        username_taken = False
        users = db.collection(u'users').stream()
        for user in users:
          try:
            if i == user.get(u'username'):
              username_taken = True
          except:
            pass
        if username_taken == True:
            clear()
            typePrint(red + "This username already exists" + reset, mts)
            sleep(2)
        else:
            username = i
            typePrint("What will be your password?\n", mts)
            i = input("")
            clear()
            adding_user = db.collection(u'users').document(username)
            adding_user.set({
              u'username' : username,
              u'password' : i,
              u'friends' : [],
              u'wins' : 0,
              u'playedmatches' : 0,
              u'requests' : None,
              u'play' : None,
              u'messages' : [],
              u'openmessages' : False,
              u'blockedusers' : [],
              u'namecolors' : [u'Cyan'],
              u'namecolor' : Fore.CYAN,
              u'namevaribles' : [Fore.CYAN],
              u'winscreen' : u'You won!',
              u'losescreen' : u'You Lost!',
              u'coins' : 0,
              u'title' : u"",
              u'winscreens' : [u'You Won'],
              u'losescreens' : [u'You Lost'],
              u'titles' : [],
              u'ip' : IPAddr
            })
            typePrint(green + "Account Created!" + reset, mts)
            sleep(2)
    elif i == "1":
        clear()
        typePrint("Username:\n", mts)
        i = input("")
        for x in db.collection(u'users').stream():
          if i == x.get(u'username'):
            loggingin = True
            clear()
            username = i
            typePrint("Password:\n", mts)
            i = input("")
            if i == x.get(u'password'):
                try:
                  t = x.get(u'ip')
                except:
                  x = db.collection(u'users').document(username)
                  x.update({u'ip' : IPAddr})
                b = db.collection(u'bannedusers').stream()
                for r in b:
                  if r == b.get("username"):
                    clear()
                    typePrint(red + "You are currently banned from Interrogation, you may or may not be unbanned soon, check punishments.md for more information.\n" + reset, ts)
                    b.get(u'ip').append(IPAddr)
                    sleep(5)
                    exit()
                while True:
                    clear()
                    user_ref = db.collection(u'users').document(username)
                    user = user_ref.get()
                    requests = user.get(u'requests') 
                    if not requests == None:
                        opponent = db.collection(u'users').document(requests.split()[0]).get()
                        typePrint("You have a challenge from " + opponent.get(u'namecolor') + opponent.get(u'username') +
                              reset + "\n", mts)
                        typePrint("\n[1] Accept\n[2] Deny\n", mts)
                        i = input("")
                        while True:
                            if i == "2":
                                user_ref.update({u'play' : False})
                                clear()
                                user_ref.update({u'requests' : None})
                                typePrint(red + "Request Declined" + reset, mts)
                                sleep(2)
                                user_ref.update({u'play' : None})
                                user = user_ref.get()
                                break
                            elif i == "1":
                                server_ref = db.collection(u'servers').document(requests.split()[1])
                                server = server_ref.get()
                                user_ref.update({u'requests' : None})
                                user_ref.update({u'play' : True})
                                end = False
                                server_ref.update({u'turn' : u'p1'})
                                server_ref.update({u'sd' : False})
                                server = server_ref.get()
                                while True:
                                    server_ref.update({u'p2ready' : False})
                                    server = server_ref.get()
                                    while server.get(u'reset') == False:
                                        clear()
                                        print("Loading.")
                                        sleep(0.5)
                                        clear()
                                        print("Loading..")
                                        sleep(0.5)
                                        clear()
                                        print("Loading...")
                                        sleep(0.5)
                                        server = server_ref.get()
                                    server_ref.update({u'p2ready' : True})
                                    server = server_ref.get()
                                    if server.get(u'turn') == "p1":
                                        while server.get(u'p1quest') == None:
                                            clear()
                                            print("Waiting for question.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for question..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for question...")
                                            sleep(0.5)
                                            server = server_ref.get()
                                        server_ref.update({u'p2ready' : False})
                                        server = server_ref.get()
                                        clear()
                                        opponent_ref = db.collection(u'users').document(server.get(u'p1name'))
                                        opponent = opponent_ref.get()
                                        typePrint(opponent.get(u'namecolor') + server.get(u'p1name') + reset +
                                              " asked:\n" + server.get(u'p1quest') + "\n", ts)
                                        typePrint("What's your answer?\n", ts)
                                        i = input("")
                                        server_ref.update({u'p2ans' : i})
                                        server = server_ref.get()
                                        while server.get(u'roundwon') == None:
                                            clear()
                                            print("Waiting for opponent.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent...")
                                            sleep(0.5)
                                            server = server_ref.get()
                                        if server.get(u'roundwon') == "p1":
                                            clear()
                                            typePrint(
                                                  "Your answer was " + red + "incorrect" +
                                                  reset, ts)
                                            sleep(3)
                                            if server.get(u'roundwon') == True:
                                                clear()
                                                typePrint(red + opponent.get(u'losescreen') +
                                                      reset, ts)
                                                sleep(2)
                                                end = True
                                                break
                                            else:
                                                clear()
                                                typePrint(red +
                                                      "You are now at risk" +
                                                      reset, ts)
                                                server_ref.update({u'sd' : True})
                                                sleep(2)
                                        else:
                                            clear()
                                            typePrint(
                                                  "Your answer was " + green + "correct" +
                                                  reset, ts)
                                            sleep(2)
                                            server = server_ref.get()
                                            if server.get(u'sd'):
                                                typePrint(
                                                    green +
                                                    "You are no longer at risk"
                                                    + reset, ts)
                                                sleep(3)
                                    else:
                                        clear()
                                        typePrint("Ask your question\n", ts)
                                        i = input("")
                                        server_ref.update({u'p2quest' : i})
                                        server = server_ref.get()
                                        while server.get(u'p1ans') == None:
                                            clear()
                                            print("Waiting for opponent.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for opponent...")
                                            sleep(0.5)
                                            server = server_ref.get()
                                        clear()
                                        typePrint(opponent.get(u'namecolor') + server.get('p1name') + reset +
                                              " said:\n" + server.get(u'p1ans') + reset + "\n", ts)
                                        typePrint("Is the answer correct?\n", ts)
                                        typePrint("\n[1] Correct\n[2] Incorrect\n", ts)
                                        i = input("")
                                        if i == "1":
                                            server = server_ref.get()
                                            if server.get(u'sd') == True:
                                                clear()
                                                typePrint(red + opponent.get(u'losescreen') +
                                                      reset, ts)
                                                server_ref.update({u'roundwon': u'p1'})
                                                server_ref.update({u'winner' : u'p1'})
                                                sleep(2)
                                                end = True
                                                break
                                            else:
                                                clear()
                                                typePrint("Opponent is correct", ts)
                                                server_ref.update({u'roundwon': u'p1'})
                                                sleep(2)
                                        else:
                                            server = server_ref.get()
                                            if not server.get(u'sd'):
                                                clear()
                                                typePrint(green + user.get(u'winscreen') +
                                                      reset, ts)
                                                server_ref.update({u'roundwon': u'p2'})
                                                server_ref.update({u'winner' : u'p2'})
                                                sleep(2)
                                                end = True
                                                break
                                            else:
                                                server = server_ref.get()
                                                clear()
                                                typePrint(
                                                    yellow +
                                                    "Both players got the question wong, " +
                                                    "you are no longer at risk."
                                                    + reset, ts)
                                                server_ref.update({u'roundwon': u'p2'})
                                                sleep(4)
                                                server_ref.update({u'sd': False})
                            if end:
                                server = server_ref.get()
                                server_ref.update({u'p1ready' : False})
                                server_ref.update({u'p2ready' : False})
                                server_ref.update({u'roundwon' : None})
                                server_ref.update({u'p1ans' : None})
                                server_ref.update({u'p2ans' : None})
                                server_ref.update({u'inuse' : False})
                                break
                    while True:
                        clear()
                        if refresh == True:
                          refresh = False
                          break
                        msg_ref = None
                        msgs = []
                        def collect_messages(Return):
                          global msg_ref, user_ref, msgs, user
                          
                          msg_ref = user_ref.get().get(u'messages')
                          msgs = []
                          for msg in msg_ref:
                            try:
                              msgs.append(msg)
                            except:
                              pass

                          if Return:
                            return msgs
                        collect_messages(False)
                        user = db.collection(u'users').document(username).get()
                        print(
                            "Welcome " + user.get(u'namecolor') + username + reset +
                            "!\nVersion 9.0.1 - Database update! Interrogation should be available at all times! Please message me about any errors you get, added a small feature to request server reset\nHave a bug report? A suggestion? Add me to your friends list and message me! Username: Kreis\n\n[1] Play Online\n[2] Search Players\n[3] View Stats\n[4] Refresh\n[5] Leaderboards\n[6] Friends List\n[7] Messages (" + str(len(msgs)) + ")\n[8] Account Settings\n[9] Shop\n[10] Inventory\n[11] Quit\n[12] Request server reset(if you our someone else stopped the program and/or exited the tab while in a match)\n\n[?] How to play"
                        )
                        i = input("")
                        if i == "20":
                            clear()
                            i = input("")
                            if i == os.environ['pass']:
                              while True:
                                clear()
                                print("[1] Reset Servers\n[2] Banned Users\n[3] Ban a user\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                if i == "1":
                                  db.collection(u'servers').document('s1').update({u'inuse' : False})
                                  db.collection(u'servers').document('s2').update({u'inuse' : False})
                                  #db.collection(u'servers').document('s3').update({u'inuse' : False})
                                  db.collection(u'servers').document('queue').update({u'currentq' : []})
                                  db.collection(u'servers').document('queue').update({u'finish' : False})
                                  clear()
                                  print("servers reset")
                                  sleep(2)
                                elif i == "2":
                                  while True:
                                    clear()
                                    count = 0
                                    banned = []
                                    for f in db.collection(u'users').document(u'bannedusers').get():
                                      banned.append(f)
                                    for x in banned:
                                      print("[" + str(count) + "] " + x)
                                      count += 1
                                    print("\n[-1] Back")
                                    i = int(input())
                                    if i == -1:
                                      break
                                    else:
                                      clear()
                                      tempname = banned[i]
                                      print(banned[i] + "\n\n[1] Unban\n\n[-1] Back")
                                      x = input("")
                                      if x == "-1":
                                        pass
                                      elif x == "1":
                                        banned.pop(i)
                                        db.collection(u'users').document(u'banned').update({u'bannedusers' : banned})
                                        break
                                elif i == "3":
                                  clear()
                                  print("Which user would you like to ban? Type -1 to go back")
                                  i = input("")
                                  if i == "-1":
                                    pass
                                  else:
                                    try:
                                      db.collection(u'users').document('banned').update({u'bannedusers' : [i]})
                                      clear()
                                      print("User banned")
                                      sleep(3)
                                    except:
                                      clear()
                                      print("User not found")
                                      sleep(3)
                        elif i == "11":
                          clear()
                          typePrint("Bye!\n", mts)
                          exit()
                        elif i == "12":
                          now = datetime.now(tz)
                          db.collection(u'users').document(u'Kreis').update({u'messages' : db.collection(u'users').document(u'Kreis').get().get(u'messages') + [user.get(u'username') + " (" + now.strftime("%m/%d/%Y %H:%M") + ") - " + "Requested server reset"]})
                        elif i == "9":
                          clear()
                          bought = False
                          while True:
                            clear()
                            user = user_ref.get()
                            typePrint("Shop\n" + Fore.LIGHTYELLOW_EX + str(user.get(u'coins')) + reset + " coins\n\n", mts)
                            print("[1] Username Colors\n[2] Win screens\n[3] Loss screens\n[4] Titles\n[5] Gamble\n\n[-1] Back")
                            i = input("")
                            if i == "-1":
                              break
                            elif i == "1":
                              while True:
                                clear()
                                user = user_ref.get()
                                print("Shop - Username Colors\nChanges the color of your username\n" + Fore.LIGHTYELLOW_EX + str(user.get(u'coins')) + reset + " coins\n\n[1] " + Fore.BLACK + "Black" + reset + " - 3 coins\n[2] White - 3 coins\n[3] " + Fore.RED + "Red" + reset + " - 5 coins\n[4] " + Fore.LIGHTYELLOW_EX + "Yellow" + reset + " - 5 coins\n[5] " + Fore.MAGENTA + "Magenta" + reset + " - 5 coins\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  buy = True
                                  user = user_ref.get()
                                  for color in user.get(u'namecolors'):
                                    if color == "Black":
                                      buy = False
                                  if user.get(u'coins') >= 3 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the black username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      user_ref.update({u'coins' : user.get(u'coins') - 3})
                                      user_ref.update({u'namecolors' : user.get(u'namecolors') + [u'Black']})
                                      user_ref.update({u'namevaribles' : user.get(u'namevaribles') + [Fore.BLACK]})
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                                      bought = True
                                      break
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                                elif i == "2":
                                  buy = True
                                  for color in user.get(u'namecolors'):
                                    if color == "White":
                                      buy = False
                                  if user.get(u'coins') >= 3 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the white username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      user_ref.update({u'coins' : user.get(u'coins') - 3})
                                      user_ref.update({u'namecolors' : user.get(u'namecolors') + [u"White"]})
                                      user_ref.update({u'namevaribles': user.get(u'namevaribles') + [Fore.WHITE]})
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                                      bought = True
                                      break
                                    user = user_ref.get()
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)  
                                elif i == "3":
                                  buy = True
                                  for color in user.get(u'namecolors'):
                                    if color == "Red":
                                      buy = False
                                  if user.get('coins') >= 5 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the red username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      user_ref.update({u'coins' : user.get(u'coins') - 5})
                                      user_ref.update({u'namecolors' : user.get(u'namecolors') + [u"Red"]})
                                      user_ref.update({u'namevaribles' : user.get(u'namevaribles') + [Fore.RED]})
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                                      bought = True
                                      break
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                                elif i == "4":
                                  buy = True
                                  for color in user.get(u'namecolros'):
                                    if color == "Yellow":
                                      buy = False
                                  if user.get(u'coins') >= 5 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the yellow username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      user_ref.update({u'coins' : user.get(u'coins') - 5})
                                      user_ref.update({u'namecolors' : user.get(u'namecolors') + [u"Yellow"]})
                                      user_ref.update({u'namevaribles' : user.get(u'namevaribles') + [Fore.YELLOW]})
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                                      bought = True
                                      break
                                    user = user_ref.get()
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                                elif i == "5":
                                  buy = True
                                  for color in user.get(u'namecolors'):
                                    if color == "Magenta":
                                      buy = False
                                  if user.get(u'coins') >= 5 and buy == True:
                                    clear()
                                    print("Are you sure you want to buy the magenta username color?\n\n[y] Yes\n[n] No")
                                    i = input("")
                                    if i == "n":
                                      pass
                                    elif i == "y":
                                      clear()
                                      user_ref.update({u'coins' : user.get(u'coins') - 5})
                                      user_ref.update({u'namecolors' : user.get(u'namecolors') + [u"Magenta"]})
                                      user_ref.update({u'namevaribles' : user.get(u'namevaribles') + [Fore.MAGENTA]})
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                                      bought = True
                                      break
                                    user = user_ref.get()
                                  else:
                                    clear()
                                    typePrint(red + "You cannot buy this item" + reset, mts)
                                    sleep(2)
                            elif i == "2":
                              while True:
                                clear()
                                print("Shop - Win Screens\nChanges the text of the win screen\n" + Fore.LIGHTYELLOW_EX + str(user.get(u'coins')) + reset + " coins\n\n[1] Add a new win screen - 5 coins\n\n[-1] Back")
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
                                      user_ref.update({u'winscreens' : user.get(u'winscreens') + [pwinscreen]})
                                      user_ref.update({u'coins' : user.get(u'coins') - 5})
                                      clear()
                                      typePrint(green + "Item Bought" + reset, mts)
                                      sleep(2)
                                      bought = True
                                      user = user_ref.get()
                            elif i == "3":
                              while True:
                                user = user_ref.get()
                                clear()
                                print("Shop - Loss Screens\nChanges the text of your opponents loss screen\n" + Fore.LIGHTYELLOW_EX + str(user.get(u'coins')) + reset + " coins\n\n[1] Add a new loss screen - 10 coins\n\n[-1] Back")
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
                                      user_ref.update({u'losescreens' : user.get(u'losescreens') + [pwinscreen]})
                                      user_ref.update({u'coins' : user.get(u'coins') - 10})
                                      clear()
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                            elif i == "4":
                              while True:
                                clear()
                                print("Shop - Titles\nAdds a title next to your username in your profile" + Fore.LIGHTYELLOW_EX + str(user.get(u'coins')) + reset + " coins\n\n[1] Add a new title - 7 coins\n\n[-1] Back")
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
                                      user_ref.update({u'titles' : user.get(u'titles') + [" - " + color + pwinscreen + reset]})
                                      user_ref.update({u'coins' : user.get(u'coins') - 7})
                                      typePrint(green + "Item Bought" + reset, mts)
                                      user = user_ref.get()
                                      sleep(2)
                            elif i == "5":
                              clear()
                              print("There is a 1 in 3 chance to double however many coins you bet, put in your bet or type -1 to go back\n" + Fore.LIGHTYELLOW_EX + str(user.get(u'coins')) + reset + " coins")
                              i = int(input())
                              if i == -1:
                                pass
                              elif i > user.get(u'coins'):
                                clear()
                                typePrint("You do not have enough coins for that", mts)
                                sleep(2)
                              else:
                                clear()
                                bet = i
                                winamount = bet * 2
                                number = random.randint(1, 3)
                                user_ref.update({u'coins' : user.get(u'coins') - bet})
                                user = user_ref.get()
                                if number == 2:
                                  user_ref.update({u'coins' : user_ref.get(u'coins') + winamount})
                                  print("You won the bet!\n" + Fore.LIGHTYELLOW_EX + str(winamount) + reset + " coins earned!")
                                  sleep(2)
                                  user = user_ref.get()
                                else:
                                  print("You lost the bet, better luck next time")
                                  sleep(2)
                                  user = user_ref.get()
                        elif i == "10":
                          clear()
                          print("Inventory\n\n[1] Username Colors\n[2] Win screens\n[3] Loss screens\n[4] Titles\n\n[-1] Back")
                          i = input("")
                          user = user_ref.get()
                          if i == "1":
                            while True:
                              user = user_ref.get()
                              if not len(user.get(u'namecolors')) < 1:
                                clear()
                                count = 0
                                print("Inventory - Name Colors\nCurrently Equipped: " + user.get(u'namecolor') + username + reset)
                                for x in user.get(u'namecolors'):
                                  print("[" + str(count) + "] " + x)
                                  count += 1
                                print("\n[-1] Back")
                                i = int(input())
                                if i == -1:
                                  break
                                else:
                                  user_ref.update({u'namecolor' : user.get(u'namevaribles')[i]})
                                  user = user_ref.get()
                          elif i == "2":
                            user = user_ref.get()
                            while True:
                              clear()
                              print("Inventory - Win Screens\nSelected: " + user.get(u'winscreen') + "\n\n")
                              count = 0
                              for x in user.get(u'winscreens'):
                                print("[" + str(count) + "] " + x)
                                count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              else:
                                user_ref.update({u'winscreen' : user.get(u'winscreens')[i]})
                                user = user_ref.get()
                          elif i == "3":
                            user = user_ref.get()
                            while True:
                              clear()
                              print("Inventory - Lose Screens\nSelected: " + user.get(u'losescreen') + "\n\n")
                              count = 0
                              for x in user.get(u'losescreens'):
                                print("[" + str(count) + "] " + x)
                                count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              else:
                                user_ref.update({u'losescreen' : user.get(u'losescreens')[i]})
                                user = user_ref.get()
                          elif i == "4":
                            user = user_ref.get()
                            while True:
                              clear()
                              if len(user.get(u'titles')) < 1:
                                typePrint("You have no titles", mts)
                                sleep(2)
                                break
                              print("Inventory - Titles\nSelected: " + user.get(u'title') + "\n\n[0] None\n[-1] Back")
                              count = 1
                              for x in user.get(u'titles'):
                                print("[" + str(count) + "]" + x)
                                count += 0
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              elif i == 0:
                                user_ref.update({u'title': ""})
                                user = user_ref.get()
                              else:
                                user_ref.update({u'title' : user.get(u'titles')[i]})
                                user = user_ref.get()
                        elif i == "?":
                          clear()
                          print("How to play: Player 1 asks player 2 a quiz question (not a personal question) If player 2 gets it wrong, they are at risk, player 2 asks player 1 a question, if they get it right, the game continues, but if player 2 was at risk, player 1 wins. Both players get it wrong? game continues. Player 1 gets it wrong without player 2 being at risk? Player 2 wins.\n\n[-1] Back")
                          i = input("")
                          if i == "-1":
                            pass
                        elif i == "8":
                          done = False
                          while True:
                            clear()
                            user = user_ref.get()
                            if done == True:
                              break
                            typePrint("[1] DM Settings\n[2] Blocked Users\n\n[-1] Back\n", mts)
                            i = input("")
                            if i == "-1":
                              break
                            if i == "1":
                              while True:
                                clear()
                                print("People who can DM you:")
                                if user.get(u'openmessages') == False:
                                  print("Friends Only")
                                else:
                                  print("Everyone")
                                print("\n[1] Friends Only\n[2] Everyone\n\n[-1] Back")
                                i = input("")
                                if i == "-1":
                                  break
                                elif i == "1":
                                  user_ref.update({u'openmessages' : False})
                                  user = user_ref.get()
                                elif i == "2":
                                  user_ref.update({u'openmessages' : True})
                                  user = user_ref.get()
                            elif i == "2":
                              while True:
                                user = user_ref.get()
                                clear()
                                count = 0
                                if len(user.get(u'blockedusers')) == 0:
                                  clear()
                                  typePrint("You have no one blocked", mts)
                                  sleep(2)
                                  break
                                for x in user.get(u'blockedusers'):
                                  print("[" + str(count) + "] " + db.collection(u'users').document(x).get().get(u'namecolor') + x + reset)
                                print("\n[-1] Back")
                                i = int(input(""))
                                if i == -1:
                                  break
                                elif not i < 0 and i < len(user.get(u'blockedusers')):
                                  clear()
                                  index = i
                                  typePrint("What would you like to do with this user?\n\n[1] Unblock\n\n[-1] Back\n", mts)
                                  i = input("")
                                  if i == "-1":
                                    break
                                  elif i == "1":
                                    clear()
                                    new_blocked = user.get(u'blockedusers')
                                    new_blocked.pop(index)
                                    user_ref.update({"blockedusers" : new_blocked})
                                    typePrint("User unblocked", mts)
                                    sleep(2)
                                    user = user_ref.get()
                        elif i == "7":
                          user = user_ref.get()
                          clear()
                          count = 0
                          if len(user.get(u'messages')) < 1:
                            typePrint("You have no messages", mts)
                            sleep(2)
                            break
                          for x in user.get(u'messages'):
                            print("[" + str(count) + "] " + user.get(u'messages')[count])
                            count += 1
                          print("[-1] Back\n[-2] Clear messages\n")
                          i = int(input())
                          if i == -1:
                            break
                          if i == -2:
                            clear()
                            user_ref.update({"messages" : []})
                            typePrint("Messages Cleared", mts)
                            sleep(2)
                            user = user_ref.get()
                          if not i > len(user.get(u'messages')) - 1:
                            clear()
                            mindex = i
                            message = user.get(u'messages')[mindex]
                            print("What do you want to do with this message?\n\n[1] Reply\n[2] Delete Message\n[3] Block User\n")
                            i = input("")
                            if i == "1":
                              clear()
                              for x in db.collection(u'users').document(message.split()[0]).get().get(u'friends'):
                                if username == x:
                                  fadded = True
                              if not fadded == True and db.collection(u'users').document(message.split()[0]).get().get(u'openmessages') == False:
                                clear()
                                typePrint(red + "This player does not have you added and does not have open DMs" + reset, mts)
                                sleep(2)
                                break
                              for x in db.collection(u'users').document(message.split()[0]).get(u'blockedusers'):
                                if username == x:
                                  clear()
                                  typePrint(red + "This user has you blocked" + reset, mts)
                                  sleep(2)
                                break
                              messenger_ref = db.collection(u'users').document(message.split()[0])
                              messenger = messenger_ref.get()
                              print("Type your mesage, -1 to go back\n")
                              i = input("")
                              if i == "-1":
                                break
                              else:
                                clear()
                                now = datetime.now(tz)
                                messenger_ref.update({u'messages' : messenger.get(u'messages') + [user.get(u'username') + " (" + now.strftime("%m/%d/%Y %H:%M") + ") - " + i]})
                                typePrint("Message sent to " + messenger.get(u'namecolor') + message.split()[0] + reset, mts)
                                new_messages = user.get(u'messages')
                                new_messages.pop(mindex)
                                user_ref.update({u'messages' : new_messages})
                                sleep(2)
                                user = user_ref.get()
                            elif i == "3":
                              user_ref.update({u'blockedusers' : user.get(u'blockedusers') + [message.split()[0]]})
                              user = user_ref.get()
                            elif i == "2":
                              clear()
                              new_messages = user.get(u'messages')
                              new_messages.pop(mindex)
                              user_ref.update({u'messages' : new_messages})
                              typePrint("Message Deleted", mts)
                              user = user_ref.get()
                              sleep(2)
                        elif i == "6":
                          while True:
                            user = user_ref.get()
                            clear()
                            count = 0
                            if len(user.get(u'friends')) < 1:
                              typePrint(red + "You dont have any friends D:" + reset, mts)
                              sleep(2)
                              break
                            for a in user.get(u'friends'):
                              print("[" + str(count) + "] " + db.collection(u'users').document(a).get().get(u'namecolor') + db.collection(u'users').document(a).get().get(u'username') + reset)
                              count = count + 1
                            typePrint("\n\n[-1] Back\n[-2] Other people that have me added\n", mts)
                            i = int(input())
                            if i == -1:
                              break
                            elif i == -2:
                              clear()
                              print("Loading")
                              people = []
                              for ruser in db.collection(u'users').stream():
                                if not "banned" in ruser.get(u'username'):
                                  listperson = True
                                  for friend in ruser.get(u'friends'):
                                    if user.get(u'username') == friend:
                                      for person in user.get(u'friends'):
                                        if person == ruser.get(u'username'):
                                          listperson = False
                                          break
                                      if listperson == True:
                                        people.append(ruser.get(u'username'))
                                        break
                              if len(people) > 0:
                                clear()
                                count = 0
                                for x in people:
                                  ruser = db.collection(u'users').document(x).get()
                                  print("[" + str(count) + "] " + ruser.get(u'namecolor') + ruser.get(u'username') + reset)
                                  count += 1
                                print("\n[-1] Back")
                                i = int(input())
                                if i == -1:
                                  clear()
                                else:
                                  ruser_ref = db.collection(u'users').document(people[i])
                                  ruser = ruser_ref.get()
                                  clear()
                                  print(ruser.get(u'namecolor') + ruser.get(u'username') + reset + "\n\n\nWins - " + str(ruser.get(u'wins')) + "\n\nLosses - " + str(ruser.get(u'playedmatches')) + "\n\n[1] Add friend\n\n[-1] Back")
                                  i = input("")
                                  if i == "1":
                                    clear()
                                    canadd = True
                                    for rruser in user.get('friends'):
                                      if rruser == ruser.get(u'username'):
                                        clear()
                                        typePrint(red + "You already have this person added" + reset, mts)
                                        canadd = False
                                        sleep(2)
                                        break
                                    if canadd == False:
                                      break
                                    clear()
                                    user_ref.update({u'friends' : user.get('friends') + [ruser.get(u'username')]})
                                    user = user_ref.get()
                                    typePrint(green + "Friend added" + reset, mts)
                                    sleep(2)
                              else:
                                clear()
                                typePrint("No one else has you added", mts)
                                sleep(2)
                            elif not i > len(user.get(u'friends')) - 1 and not i < 0:
                              clear()
                              findex = i
                              fname = user.get(u'friends')[findex]
                              ruser_ref = db.collection(u'users').document(fname)
                              ruser = ruser_ref.get()
                              print("Options for " + ruser.get(u'namecolor') + ruser.get(u'username') + reset + "\n\n[1] Message Player\n[2] Remove Friend\n[3] Block User\n\n[-1] Back\n")
                              i = input("")
                              if i == "-1":
                                print("")
                              elif i == "1":
                                if not user.get(u'username') in ruser.get(u'friends') and ruser.get(u'openmessages') == False:
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
                                  ruser_ref.update({u'messages' : ruser.get(u'messages') + [user.get(u'username') + "(" + now.strftime("%m/%d/%Y %H:%M") + ") - " + i]})
                                  typePrint("Message sent to " +  ruser.get(u'namecolor') + ruser.get(u'username') + reset, mts)
                                  user = user_ref.get()
                                  sleep(2)
                              elif i == "2":
                                new_friends = user.get(u'friends')
                                new_friends.pop(findex)
                                user_ref.update({u'friends' : new_friends})
                                user = user_ref.get()
                                clear()
                                typePrint("Friend Removed", mts)
                                sleep(2)
                              elif i == "3":
                                user_ref.update({u'blockedusers' : [user.get(u'blockedusers') + user.get(u'friends')[findex]]})
                                new_friends = user.get(u'friends')
                                new_friends.pop(findex)
                                user_ref.update({u'friends' : new_friends})
                                user = user_ref.get()
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
                            for ruser in db.collection(u'users').stream():
                              ruser = ruser.get(u'username')
                              if not "banned" in ruser:
                                ruser_ref = db.collection(u'users').document(ruser)
                                ruser = ruser_ref.get()
                                rounds = ruser.get(u'wins') + ruser.get(u'playedmatches')
                                uwins = ruser.get(u'wins')
                                ulosses = ruser.get(u'playedmatches')
                                tlosses = ruser.get(u'playedmatches')
                                users.append([])
                                if ulosses == 0:
                                  tlosses = 1
                                wlratio = rounds * (uwins/tlosses)
                                twlratio = round(uwins/tlosses, 2)
                                users[count].append(round(wlratio, 2))
                                users[count].append(ruser.get(u'username'))
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
                            for ruser in db.collection(u'users').stream():
                              ruser_ref = ruser
                              ruser = ruser_ref.get()
                              print(ruser.get(u'username'))
                            i = input("")
                            if i == "-1":
                              break
                        elif i == "3":
                            while True:
                                clear()
                                losses = user.get(u'playedmatches')
                                if losses == 0:
                                  losses += 1
                                rounds = user.get(u'wins') + user.get(u'playedmatches')
                                points = rounds * (user.get(u'wins')) / losses
                                print(user.get(u'namecolor') + user.get(u'username') + reset + user.get(u'title') +
                                      "\n\nRounds won - " +
                                      str(user.get(u'wins')) +
                                      "\n\nRounds lost - " +
                                      str(user.get(u'playedmatches')) + "\n\n" + str(round(points, 2)) + " points\n" +
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
                              for ruser in db.collection(u'users').stream():
                                if i in ruser.get(u'username'):
                                    if not "banned" in ruser.get(u'username'):
                                          found_users.append(ruser.get(u'username'))
                                          print("[" + str(count) + "]" + ruser.get(u'namecolor') + " " + found_users[count] + reset)
                                          count += 1
                              print("\n[-1] Back")
                              i = int(input())
                              if i == -1:
                                break
                              elif not i > len(found_users) and not i < 0:
                                clear()
                                ruser_ref = db.collection(u'users').document(found_users[i])
                                ruser = ruser_ref.get()
                                print(ruser.get(u'namecolor') + ruser.get(u'username') + reset + ruser.get(u'title') + "\n\n\nRounds Won - " + str(ruser.get(u'wins')) + "\n\nRounds Lost - " + str(ruser.get(u'playedmatches')) + "\n\n[1] Add friend\n\n[-1] Back")
                                i = input("")
                                if i == "1":
                                  clear()
                                  if not ruser.get(u'username') in user.get(u'friends'):
                                    if ruser.get(u'username') == user.get(u'username'):
                                      typePrint(red + "Don't." + reset, ts)
                                      sleep(2)
                                      break
                                    user_ref.update({u'friends': user.get(u'friends') + [ruser.get(u'username')]})
                                    user = user_ref.get()
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
                            for a in user.get(u'friends'):
                                x = db.collection(u'users').document(a).get()
                                print("[" + str(count) + "] " + x.get(u'namecolor') + x.get(u'username') + reset)
                                count = count + 1
                            typePrint("[-1] Back\n[-2] Random opponent\n", mts)
                            i = int(input())
                            if i == -1:
                                break
                            elif i == -2:
                              while True:
                                clear()
                                if len(db.collection(u'servers').document(u'queue').get().get(u'queue')) > 1:
                                  clear()
                                  typePrint("A game is starting, refresh and try again", mts)
                                  sleep(2)
                                  break
                                if not db.collection(u'servers').document(u's1').get().get(u'inuse') == True:
                                  server_ref = db.collection(u'servers').document(u's1')
                                  server = server_ref.get()
                                elif not db.collection(u'servers').document(u's2').get().get(u'inuse') == True:
                                  server_ref = db.collection(u'servers').document(u's2')
                                  server = server_ref.get()
                                elif not db.collection(u'servers').document(u's3').get().get(u'inuse') == True:
                                  server_ref = db.collection(u'servers').document(u's3')
                                  server = server_ref.get()
                                else:
                                  clear()
                                  typePrint("Servers are full right now, try again later")
                                if True:
                                  db.collection(u'servers').document(u'queue').update({u'queue' : db.collection(u'servers').document(u'queue').get().get(u'queue') + [user.get(u'username')]})
                                  queue_ref = db.collection(u'servers').document(u'queue')
                                  queue = queue_ref.get()
                                  if len(queue.get(u'queue')) > 1:
                                    while not queue.get(u'finish') == True:
                                      clear()
                                      print("Loading")
                                      queue = queue_ref.get()
                                    typePrint(green + "Game has been found! Accept the challenge you will recive to play." + reset, mts)
                                    sleep(2)
                                    refresh = True
                                    user = user_ref.get()
                                    while user.get(u'requests') == None:
                                      print("Loading.")
                                      sleep(0.5)
                                      print("Loading..")
                                      sleep(0.5)
                                      print("Loading...")
                                      sleep(0.5)
                                      user = user_ref.get()
                                    queue_ref.update({u'finish' : False})
                                    queue = queue_ref.get()
                                    break
                                  else:
                                    leave = False
                                    print("You are in the queue, wait 10 seconds and see if anyone joins")
                                    sleep(10)
                                    queue = queue_ref.get()
                                    if len(queue.get(u'queue')) > 1:
                                      ruser_ref = db.collection(u'users').document(queue.get(u'queue')[1])
                                      ruser = ruser_ref.get()
                                      ruser_ref.update({u'requests' : user.get(u'username') + " " + server.get(u'id')})
                                      queue_ref.update({u'queue' : []})
                                      queue_ref.update({u'finish' : True})
                                      while ruser.get(u'play') == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)
                                            ruser = ruser_ref.get()
                                      if ruser.get(u'play'):
                                        server_ref.update({u'p2name' : ruser.get(u'username')})
                                        ruser_ref.update({u'play' : False})
                                        server_ref.update({u'p1name' : user.get(u'username')})
                                        server_ref.update({u'sd' : False})
                                        server_ref.update({u'reset' : False})
                                        server_ref.update({u'inuse' : True})
                                        server_ref.update({u'turn' : u'p2'})
                                        server = server_ref.get()
                                        while True:
                                            server_ref.update({u'p1quest' : None})
                                            server_ref.update({u'p2quest' : None})
                                            server_ref.update({u'p1ready' : True})
                                            server_ref.update({u'p1ans' : None})
                                            server_ref.update({u'p2ans' : None})
                                            server_ref.update({u'roundwon' : None})
                                            server = server_ref.get()
                                            if server.get(u'turn') == "p1":
                                                server_ref.update({u'turn' : u'p2'})
                                            else:
                                                server_ref.update({u'turn' : u'p1'})
                                            server_ref.update({u'reset' : True})
                                            while server.get(u'p2ready') == False:
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
                                                server = server_ref.get()
                                            server_ref.update({u'reset' : False})
                                            server = server_ref.get()
                                            if server.get(u'turn') == "p1":
                                                clear()
                                                typePrint("Ask your question\n", ts)
                                                i = input("")
                                                server_ref.update({u'p1quest' : i})
                                                while server.get(u'p2ans') == None:
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
                                                    server = server_ref.get()
                                                clear()
                                                server = server_ref.get()
                                                typePrint(ruser.get(u'namecolor') + ruser.get(u'username') + reset +
                                                      " said:" + "\n" +
                                                      server.get(u'p2ans'), ts)
                                                typePrint(
                                                    "\n\n[1] Correct\n[2] Incorrect\n", ts
                                                )
                                                i = input("")
                                                server = server_ref.get()
                                                if i == "1":
                                                    user = user_ref.get()
                                                    ruser = ruser_ref.get()
                                                    server_ref.update({u'sd' : False})
                                                    clear()
                                                    typePrint(
                                                        "Opponent is correct", ts)
                                                    user_ref.update({u'playedmatches' : user.get(u'playedmatches') + 1})
                                                    ruser_ref.update({u'wins' : ruser.get(u'wins') + 1})
                                                    ruser_ref.update({u'coins' : ruser.get(u'coins') + 2})
                                                    server_ref.update({u'roundwon' : 'p2'})
                                                    server = server_ref.get()
                                                    sleep(2)
                                                else:
                                                    server = server_ref.get()
                                                    user = user_ref.get()
                                                    ruser = ruser_ref.get()
                                                    if server.get(u'sd') == True:
                                                        server_ref.update({u'winner' : 'p1'})
                                                        server_ref.update({u'roundwon' : 'p1'})
                                                        clear()
                                                        typePrint(user.get(u'winscreen'), ts)
                                                        ruser_ref.update({u'playedmatches' : ruser.get(u'playedmatches') + 1})
                                                        user_ref.update({u'wins' : user.get(u'wins') + 1})
                                                        user_ref.update({u'coins' : user.get(u'coins') + 5})
                                                        sleep(2)
                                                        break
                                                    else:
                                                        server = server_ref.get()
                                                        server_ref.update({u'roundwon' : 'p1'})
                                                        ruser = ruser_ref.get()
                                                        user = user_ref.get()
                                                        clear()
                                                        typePrint(
                                                            green +
                                                            "You won this round, " +
                                                            "opponent is now at risk"
                                                            + reset, ts)
                                                        ruser_ref.update({u'playedmatches' : ruser.get(u'playedmatches') + 1})
                                                        user_ref.update({u'wins' : user.get(u'wins') + 1})
                                                        server_ref.update({u'roundwon' : u'p1'})
                                                        sleep(2)
                                                        user_ref.update({u'coins' : user.get(u'coins') + 2})
                                            else:
                                                server = server_ref.get()
                                                ruser = ruser_ref.get()
                                                user = user_ref.get()
                                                while server.get(u'p2quest'):
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
                                                    server = server_ref.get()
                                                clear()
                                                server = server_ref.get()
                                                typePrint(ruser.get(u'namecolor') + ruser.get(u'username')  + reset +
                                                      " asked:\n" +
                                                      server.get(u'p2quest') + "\n", ts)
                                                typePrint("Type your answer\n", ts)
                                                i = input("")
                                                server_ref.update({u'p1ans' : i})
                                                server = server_ref.get()
                                                while server.get(u'roundwon') == None:
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
                                                    server = server_ref.get()
                                                if server.get(u'roundwon') == "p1":
                                                    clear()
                                                    typePrint(
                                                          "Your answer was " + green + "correct." +
                                                          reset, ts)
                                                    ruser_ref.update({u'playedmatches' : ruser.get(u'playedmatches') + 1})
                                                    user_ref.update({u'wins' : user.get(u'wins') + 1})
                                                    user_ref.update({u'coins' : user.get(u'coins') + 2})
                                                    sleep(2)
                                                    server = server_ref.get()
                                                    user = user_ref.get()
                                                    if server.get(u'sd') == True:
                                                        clear()
                                                        typePrint(green +
                                                              user.get(u'winscreen') +
                                                              reset, ts)
                                                        user_ref.update({u'coins' : user.get(u'coins') + 5})
                                                        sleep(2)
                                                        break
                                                else:
                                                    server = server_ref.get()
                                                    user = user_ref.get()
                                                    ruser = ruser_ref.get()
                                                    if server.get(u'sd') == False:
                                                        clear()
                                                        typePrint(red +
                                                              ruser.get(u'losescreen') +
                                                              reset, ts)
                                                        sleep(2)
                                                        user_ref.update({u'playedmatches' : user.get(u'playedmatches') + 1})
                                                        ruser_ref.update({u'wins' : ruser.get(u'wins') + 1})
                                                        server_ref.update({u'roundwon' : 'p2'})
                                                        server_ref.update({u'winner' : 'p2'})
                                                        ruser_ref.update({u'coins' : ruser.get(u'coins') + 5})
                                                        break
                                                    else:
                                                        clear()
                                                        user = user_ref.get()
                                                        ruser = ruser_ref.get()
                                                        typePrint(
                                                            "Your answer was " + red + "incorrect, " + reset +
                                                            "opponent is no longer at risk."
                                                            + reset, ts)
                                                        user_ref.update({u'playedmatches' : user.get(u'playedmatches') + 1})
                                                        ruser_ref.update({u'wins' : ruser.get(u'wins') + 1})
                                                        server_ref.update({u'roundwon' : 'p2'})
                                                        ruser_ref.update({u'coins' : ruser.get(u'coins') + 2})
                                                        sleep(5)
                                                        server_ref.update({u'sd' : False})
                                        server_ref.update({u'inuse' : False})
                                        server_ref.update({u'p1ready' : False})
                                        server_ref.update({u'p2ready' : False})
                                        server_ref.update({u'reset' : False})
                                      else:
                                        clear()
                                        typePrint(
                                            red +
                                            "The user declined your request" +
                                            reset, mts)
                                        ruser_ref.update({u'play' : False})
                                        sleep(2)
                                        break
                                    else:
                                      clear()
                                      queue_ref.update({u'queue' : []})
                                      typePrint(red + "No users found" + reset, mts)
                                      sleep(2)
                                      break
                            else:
                              ruser_ref = db.collection(u'users').document(user.get(u'friends')[i])
                              ruser = ruser_ref.get()
                              canplay = False
                              for x in ruser.get(u'friends'):
                                if user.get(u'username') == x:
                                  canplay = True
                              for x in ruser.get(u'blockedusers'):
                                if user.get(u'username') == x:
                                  canplay = False
                              if not canplay == True:
                                clear()
                                typePrint(red + "This person does not have you added" + reset, mts)
                                sleep(2)
                                break
                              else:
                                if ruser.get(u'requests') == None:
                                    if db.collection(u'servers').document(u's1').get().get(u'inuse') == False:
                                        server_ref = db.collection(u'servers').document(u's1')
                                        server = server_ref.get()
                                        ruser_ref.update({u'requests' : user.get(u'username') + " " + server.get(u'id')})
                                        clear()
                                        sleep(2)
                                        ruser = ruser_ref.get()
                                        while ruser.get(u'play') == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)
                                            ruser = ruser_ref.get()
                                    elif db.collection(u'servers').document(u's2').get().get(u'inuse') == False:
                                        server_ref = db.collection(u'servers').document(u's2')
                                        server = server_ref.get()
                                        ruser_ref.update({u'requests' : user.get(u'username') + " " + server.get(u'id')})
                                        ruser = ruser_ref.get()
                                        while ruser.get(u'play') == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5)
                                            ruser = ruser_ref.get()
                                    elif db.collection(u'servers').document(u's2').get().get(u'inuse') == False:
                                        server_ref = db.collection(u'servers').document(u's3')
                                        server = server_ref.get()
                                        ruser_ref.update({u'requests' : user.get(u'username') + " " + server.get(u'id')})
                                        ruser = ruser_ref.get()
                                        while ruser.get(u'play') == None:
                                            clear()
                                            print("Waiting for response.")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response..")
                                            sleep(0.5)
                                            clear()
                                            print("Waiting for response...")
                                            sleep(0.5) 
                                            ruser = ruser_ref.get()
                                    else:
                                        clear()
                                        typePrint(
                                            "Sorry, the servers the currently full, please try again later.", mts
                                        )
                                        break
                                    if ruser.get(u'play') == True:
                                        server_ref.update({u'p2name' : ruser.get(u'username')})
                                        ruser = ruser_ref.get()
                                        ruser_ref.update({u'play' : None})
                                        server_ref.update({u'p1name' : user.get(u'username')})
                                        server_ref.update({u'sd' : False})
                                        server_ref.update({u'reset' : False})
                                        server_ref.update({u'inuse' : True})
                                        server_ref.update({u'turn' : 'p2'})
                                        while True:
                                            server_ref.update({u'p1quest' : None})
                                            server_ref.update({u'p2quest' : None})
                                            server_ref.update({u'p1ready' : True})
                                            server_ref.update({u'p1ans' : None})
                                            server_ref.update({u'p2ans' : None})
                                            server_ref.update({u'roundwon' : None})
                                            server_ref.update({u'winner' : None})
                                            server = server_ref.get()
                                            if server.get(u'turn') == "p1":
                                                server_ref.update({u'turn' : 'p2'})
                                            else:
                                                server_ref.update({u'turn' : 'p1'})
                                            server_ref.update({u'reset' : True})
                                            server = server_ref.get()
                                            while server.get(u'p2ready') == False:
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
                                                server = server_ref.get()
                                            server_ref.update({u'reset' : False})
                                            server = server_ref.get()
                                            if server.get(u'turn') == "p1":
                                                clear()
                                                typePrint("Ask your question\n", ts)
                                                i = input("")
                                                server_ref.update({u'p1quest' : i})
                                                server = server_ref.get()
                                                while server.get(u'p2ans') == None:
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
                                                    server = server_ref.get()
                                                clear()
                                                server = server_ref.get()
                                                typePrint(ruser.get(u'namecolor') + ruser.get(u'username') + reset +
                                                      " said:" + "\n" +
                                                      server.get(u'p2ans'), ts)
                                                typePrint(
                                                    "\n\n[1] Correct\n[2] Incorrect\n", ts
                                                )
                                                i = input("")
                                                if i == "1":
                                                    server = server_ref.get()
                                                    server_ref.update({u'sd' : False})
                                                    ruser = ruser_ref.get()
                                                    user = user_ref.get()
                                                    clear()
                                                    typePrint(
                                                        "Opponent is correct", ts)
                                                    user_ref.update({u'playedmatches' : user.get(u'playedmatches') + 1})
                                                    ruser_ref.update({u'wins' : ruser.get(u'wins') + 1})
                                                    server_ref.update({u'roundwon' : 'p2'})
                                                    ruser_ref.update({u'coins' : ruser.get(u'coins') + 1})
                                                    server_ref.update({u'sd' : False})
                                                    server_ref.update({u'roundwon' : u'p2'})
                                                    sleep(2)
                                                else:
                                                    server = server_ref.get()
                                                    user = user_ref.get()
                                                    ruser = ruser_ref.get()
                                                    if server.get(u'sd') == True:
                                                        server_ref.update({u'winner' : u'p1'})
                                                        server_ref.update({u'roundwon' : u'p1'})
                                                        clear()
                                                        typePrint(user.get(u'winscreen'), ts)
                                                        ruser_ref.update({u'playedmatches' : ruser.get(u'playedmatches') + 1})
                                                        user_ref.update({u'wins' : user.get(u'wins') + 1})
                                                        user_ref.update({u'coins' : user.get(u'coins') + 5})
                                                        sleep(2)
                                                        break
                                                    else:
                                                        server = server_ref.get()
                                                        user = user_ref.get()
                                                        ruser = ruser_ref.get()
                                                        server_ref.update({u'sd' : True})
                                                        clear()
                                                        typePrint(
                                                            green +
                                                            "You won this round, " +
                                                            "opponent is now at risk"
                                                            + reset, ts)
                                                        ruser_ref.update({u'playedmatches' : ruser.get(u'playedmatches') + 1})
                                                        user_ref.update({u'wins' : user.get(u'wins') + 1})
                                                        server_ref.update({u'roundwon' : u'p1'})
                                                        sleep(2)
                                                        user_ref.update({u'coins' : user.get(u'coins') + 2})
                                            else:
                                                server = server_ref.get()
                                                while server.get(u'p2quest') == None:
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
                                                    server = server_ref.get()
                                                clear()
                                                server = server_ref.get()
                                                typePrint(ruser.get(u'namecolor') + ruser.get(u'username')  + reset +
                                                      " asked:\n" +
                                                      server.get(u'p2quest') + "\n", ts)
                                                typePrint("Type your answer\n", ts)
                                                i = input("")
                                                server_ref.update({u'p1ans' : i})
                                                server = server_ref.get()
                                                while server.get(u'roundwon') == None:
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
                                                    server = server_ref.get()
                                                if server.get(u'roundwon') == "p1":
                                                    clear()
                                                    user = user_ref.get()
                                                    server = server_ref.get()
                                                    ruser = ruser_ref.get()
                                                    typePrint(
                                                          "Your answer was " + green + "correct." +
                                                          reset, ts)
                                                    ruser_ref.update({u'playedmatches' : ruser.get(u'playedmatches') + 1})
                                                    user_ref.update({u'wins' : user.get(u'wins') + 1})
                                                    user_ref.update({u'coins' : user.get(u'coins') + 2})
                                                    sleep(2)
                                                    server = server_ref.get()
                                                    user = user_ref.get()
                                                    ruser = ruser_ref.get()
                                                    if server.get(u'sd') == True:
                                                        clear()
                                                        typePrint(green +
                                                              user.get(u'winscreen') +
                                                              reset, ts)
                                                        user_ref.update({u'coins' : user.get(u'coins') + 5})
                                                        sleep(2)
                                                        break
                                                else:
                                                    user = user_ref.get()
                                                    ruser = ruser_ref.get()
                                                    server = server_ref.get()
                                                    if server.get(u'sd') == False:
                                                        clear()
                                                        typePrint(red +
                                                              ruser.get(u'losescreen') +
                                                              reset, ts)
                                                        sleep(2)
                                                        user_ref.update({u'playedmatches' : user.get(u'playedmatches') + 1})
                                                        ruser_ref.update({u'wins' : ruser.get(u'wins') + 1})
                                                        ruser_ref.update({u'coins' : ruser.get(u'coins') + 1})
                                                        break
                                                    else:
                                                        clear()
                                                        user = user_ref.get()
                                                        ruser = ruser_ref.get()
                                                        typePrint(
                                                            "Your answer was " + red + "incorrect, " + reset +
                                                            "opponent is no longer at risk."
                                                            + reset, ts)
                                                        user_ref.update({u'playedmatches' : user.get(u'playedmatches') + 1})
                                                        ruser_ref.update({u'wins' : ruser.get(u'wins') + 1})
                                                        ruser_ref.update({u'coins' : ruser.get(u'coins') + 1})
                                                        sleep(5)
                                                        server_ref.update({'sd' : False})
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
            