# Chris12902#0182
# 12 May 2020
# Kudos to https://www.youtube.com/watch?v=T8DLwACpe3o


import time
import socket
import RobloxInterface

interface = RobloxInterface.RobloxInterface()
time.sleep(5)
interface.press("space")
time.sleep(5)
interface.release("space")
# Functions
def open_socket(HOST, PORT, PASS, IDENT, CHANNEL):
    print("signing into account " + IDENT)
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", encoding='utf8'))
    s.send(bytes("NICK " + IDENT + "\r\n", 'UTF-8'))
    s.send(bytes("JOIN #" + CHANNEL + "\r\n", 'UTF-8'))
    print("sign in complete")
    return s


def loading_complete(line):
    if "End of /NAMES list" in line:
        return False
    else:
        return True


def join_room(s):
    print("joining chat...")
    readbuffer = ""
    loading = True
    while loading:
        readbuffer = readbuffer + str(s.recv(1024))
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()
        if "Improperly formatted auth" in readbuffer:
            print("error: improperly formatted auth")
            quit()
        loading = loading_complete(readbuffer)
    print("successfully joined chat!")
    send_message(s, "successfully joined the chat!")


def send_message(s, message):
    global CHANNEL
    message_temp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send(bytes(message_temp + "\r\n", 'UTF-8'))
    print("sent " + message_temp)


def get_user(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


def get_message(line):
    message = line.split('PRIVMSG #' + get_user(line) + ' :')
    message = message[len(message) - 1].split("\\r\\n")[0]
    return message


def getX(line):
    separate = line.split(",")
    return separate[0]


def getY(line):
    separate = line.split(",")
    return separate[1]


# Variables
readbuffer = ""
settingsFile = None
# These lines read the text file and set up the variables of the program. You absolutely do not want to edit these lines
print("initializing settings...")
try:
    settingsFile = open("settings.txt", "r")
except IOError:
    print("error: settings file is invalid")
    quit()
sfLines = settingsFile.readlines()
PORT = sfLines[0][5:len(sfLines[0]) - 1]
PORT = int(PORT)
PASS = sfLines[1][5:len(sfLines[1]) - 1]
USERNAME = sfLines[2][9:len(sfLines[2]) - 1]
CHANNEL = sfLines[3][8:len(sfLines[3]) - 1]
settingsFile.close()
print("initialization complete")
print("now connecting to twitch's APIs")
s = open_socket("irc.twitch.tv", PORT, PASS, USERNAME, CHANNEL)  # Connects to your Twitch profile
join_room(s)

while True:
    readbuffer = readbuffer + str(s.recv(1024))
    temp = str.split(readbuffer, "\n")
    readbuffer = temp[0]
    for line in temp:
        if "PING :tmi.twitch.tv" == line:
            s.send(bytes("PONG :tmi.twitch.tv", 'UTF-8'))
        user = get_user(line)
        message = get_message(line)
        if "w" == message.lower() or "a" == message.lower() or "d" == message.lower() or "s" == message.lower() or "jump" in message.lower() or "click" in message.lower():
            print("took input from " + user + ": " + message)
        if "w" == message.lower():
            interface.press('w')
            time.sleep(0.3)
            interface.release('w')
        if "a" == message.lower():
            interface.press('a')
            time.sleep(0.1)
            interface.release('a')
        if "d" == message.lower():
            interface.press('d')
            time.sleep(0.1)
            interface.release('d')
        if "s" == message.lower():
            interface.press('s')
            time.sleep(0.1)
            interface.release('s')
        if "jump" in message.lower():
            interface.press("space")
            if "jump+w" == message.lower():
                interface.press('w')
            if "jump+a" == message.lower():
                interface.press('a')
            if "jump+d" == message.lower():
                interface.press('d')
            if "jump+s" == message.lower():
                interface.press('s')
            time.sleep(0.1)
            interface.release("space")
            if "jump+w" == message.lower():
                interface.release('w')
            if "jump+a" == message.lower():
                interface.release('a')
            if "jump+d" == message.lower():
                interface.release('d')
            if "jump+s" == message.lower():
                interface.release('s')
        if "click" in message.lower():
            X = getX(message)
            Y = getY(message)
            interface.click(x=X, y=Y)
