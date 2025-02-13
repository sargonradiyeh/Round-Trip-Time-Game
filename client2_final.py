from socket import *


host = '127.0.0.1'  #str(gethostbyname(gethostname())) works on private networks as Firewall Prevents Port Access by default on public networks
# we can use the localhost IP since both server and client run on same machine
port = 8696  # port number of the proxy server
client_socket = socket(AF_INET, SOCK_STREAM)  # instantiate socket to connect to proxy server

try:
    client_socket.connect((host, port))  # connect to the proxy server
    welcome = client_socket.recv(4096).decode()  # receives 4096 bytes of data from server(limits data received to 2048 bytes)
    print(welcome)#print welcome message sent by server
    print("=========================================================================\n")
    print("How to Win: Input the number you see as fast you can in a 3 round battle!\n")
    print("=========================================================================\n")
    while True:
        timer = client_socket.recv(4096).decode()#continously print time sent by server until "STARTED" is sent after 5 seconds.
        if timer == "STARTED":
            print("The Game Has Started! Input the number you see IMMEDIATELY\n")
            print("=========================================================================")
            break
        else:
            print(timer, end="\r")

    for i in range(0, 3):
        print("\n")
        response = client_socket.recv(4096).decode()
        if "Game Over" in response:#if game ends for any reason, it will contain "Game Over" along with corresponding reason (variable reasons)
            print("=========================================================================\n")
            print(response)
            break
        print("=========================================================================\n")
        print("Please enter the number displayed: ", response,"\n")#print random number
        print("=========================================================================\n")
        number=input()#take as input number typed by client

        if not number:#if nothing is typed, inform server client is disqualified for round
            client_socket.send("Disqualified".encode())
        else:#send the number and let the server decide
            client_socket.send(str(number).encode())
    print("\n")
    response = client_socket.recv(4096).decode() # receives 4096 bytes of data from server(limits data received to 2048 bytes)
    print("=========================================================================\n")
    print(response)#print final response (the ending of the game for some reason)
except ConnectionRefusedError:#if specific error occurs
    print("Couldn't connect to server. Make sure it is on and running")
except:#if any other error occurs
    print("Lost Connection with Server. Game has Ended")


