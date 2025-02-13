import datetime
import random
from socket import *
import time

host = '127.0.0.1'  # str(gethostbyname(gethostname())) works on private networks as Firewall Prevents Port Access by default on public networks
# we can use the localhost IP since both server and client run on same machine
port = 8696  # port the server binds to
server_socket = socket(AF_INET, SOCK_STREAM)  # instantiate tcp socket
server_socket.bind((host, port))  # bind host address and port together
server_socket.listen()  # listens for incoming connections
print("Server is listening for incoming connections")
i = 0
connection = []#to differentiate number of connections
address = []#to differentiate IP Adresses of connections and display them later
disqualified = []  # for wrong answers
disconnected = []  # for disconnecting
RTT = []
# score1 = 0
# score2 = 0
score = [0, 0]
breakFlag = False  # know if to break out of nested loops
disconnection_occurred = False  #tells program that a client disconnected
for i in range(0, 2):
    conn, add = server_socket.accept()  # accepting incoming connections of the clients
    connection.append(conn)
    address.append(add)  # produces a tuple: in server_socket.accept()[0] we have connection type info, in [1] we have the IP and Port info
    disqualified.append(False)
    disconnected.append(False)#initiate both disqualified and disconnected to false for each client
    RTT.append(0)#initiate RTT for each client
    print("TCP Connection established from " + "Player " + str(i+1) + str(address[i]) + " at " + str(datetime.datetime.now()))#display player number along with IP address as well as time of connection
    connection[i].send(("Welcome Player " + str(i + 1) + ", you have connected to the game server!").encode())#Welcome message sent to each player

# Countdown function
print("\n")
t = 5
while t >= 0:#standard countdown timer starting from 5 seconds
    mins, secs = divmod(t, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    for i in range(0, len(connection)):#len(connection) is just the number of connections established
        connection[i].send(("Game starting in: " + str(timer)).encode())#constantly send clients timer countdown to prepare them
    print("Game starting in: " + timer, end="\r")
    time.sleep(1)
    t -= 1
for i in range(0, len(connection)):
    connection[i].send("STARTED".encode())#send to indicate to client the game has started
print("\r" + "\r" + "The game has started!  ")#telling server user the game has started
print("\n")
print("Scores will be displayed in the format: " + "\x1B[3m" + "Player1Score-Player2Score" + "\x1B[0m")
print("RTTs will be listed from slowest to fastest(descending order)")#clarifying to server user how leaderboard system will work
print("\n")

# Implementing the game logic:
try:
    for i in range(0, 3):
        if breakFlag: #breakFlag created in order to implement multiple breaks (exit all loops)
            break
        for j in range(0, len(connection)):
            disqualified[j] = False #reintialise to False in case it was True last round (disqualification should not persist)
            number_sent = str(random.randint(0, 9))#create random number, different for each client to make it more fair in case players are sitting close to eachother
            connection[j].send(number_sent.encode())#send random number
            time_sent = datetime.datetime.now()#start timing for RTT

            try:
                echo = connection[j].recv(4096).decode()#recieve response and save in echo
                time_received = datetime.datetime.now()#end timing for RTT
                RTT[j] = (time_received - time_sent).total_seconds()#place accordingly in RTT array
                if echo != number_sent:#if player enters anything (word, empty string, wrong number) other than the number sent, disqualify for current round
                    disqualified[j] = True
                    RTT[j] = 999999  #sets RTT of disqualified to 999999 for calculations

            except: 
                disconnected[j] = True #if except reached, assume client is disconnected
                disconnection_occurred = True #exists to ensure other cases work, if this didnt exist its harder to enforce the cases to be ignored
                print("Player " + str(j + 1) + " Disconnected. Game Has Ended")#print to server side who disconnected then accordingly send to other player as well
                if j == 1:  # second player disconnected
                    connection[0].send("Game Over: Player 2 disconnected".encode())
                elif j == 0:  # first player disconnected
                    connection[1].send("Game Over: Player 1 disconnected".encode())
                breakFlag = True#set break flag to true in order to leave all loops now since no need to continue
                break
        if breakFlag:
            break
        print("Round", i + 1)#print round accordingly
        for k in range(0, len(connection)):
            if disqualified[k] and not disconnection_occurred: #disconnection_occured used to enforce ignoring cases if disconnected
                print("Player " + str(k + 1) + " is disqualified")
            if not disqualified[k] and not disconnection_occurred:
                if RTT[k] == min(RTT):#whoever has the smallest RTT in the array will gain +1 on their score
                    score[k] = score[k]+1
        while True:
            breakWhile = True #to check if we exit while loop
            for k in range(0, len(connection)):
                if RTT[k] != 999999 and RTT[k] != -1:
                    breakWhile = False  #if element not already checked by min and max(-1) or disqualified(999999) don't break
            if breakWhile:
                break
            else:
                for k in range(0, len(connection)):
                    if disqualified[k]:
                        RTT[k] = -1  #sets disqualified as -1 (-1 means element was checked)
                    if not disqualified[k] and not disconnection_occurred:
                        if RTT[k] == max(RTT) and RTT[k] != -1:
                            print("Player " + str(k + 1) + ": Time=" + str(RTT[k]))
                            RTT[k] = -1

        print("Scores: " + str(score[0]) + "-" + str(score[1]))#print scores each round regardless
        print("\n")
    if disconnection_occurred:#close connection of other client if a client disconnects
        if disconnected[0]:
            connection[1].close()
        elif disconnected[1]:
            connection[0].close()
    else:
        print("Final Score:")
        print("Player 1 - Player 2")
        print("    "+str(score[0]) + "    " + "-" + "    " + str(score[1]))
        print("\n")
        if score[0] > score[1]:#basic cases for which player won or if they both drawed, regardless send to each player what occured to them
            print("Player 1 is the Winner !")
            connection[0].send("You are the winner! ".encode())
            connection[1].send("Player 1 Won. Hard Luck! ".encode())
        elif score[1] > score[0]:
            print("Player 2 is the Winner !")
            connection[0].send("Player 2 Won. Hard Luck! ".encode())
            connection[1].send("You are the winner! ".encode())
        else:
            print("Draw! No Winner.")
            connection[0].send("Draw!  No Winner.".encode())
            connection[1].send("Draw!  No Winner.".encode())

        print("Good Game !!")#Print this server side to indicate game over, proceed to close connections of clients.
        connection[0].close()
        connection[1].close()
except:#if all else fails, indicate a error has occured server side
    print("The Error Listed Above caused the game to end")
