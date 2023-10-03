import sys
from socket import socket, SOCK_DGRAM, AF_INET
import numpy as np

def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))


def send_data(udp_sock, endpoint, data):
  try:
    if type(data) is list:
       for i in range(len(data)):
          # print(data[i])
          ret = udp_sock.sendto(bytes(data[i], 'utf-8'), endpoint)
          print("Sent %d bytes" % (ret))
    else:
      ret = udp_sock.sendto(bytes(data, 'utf-8'), endpoint)
      print("Sent %d bytes" % (ret))
  except Exception as e:
    print_error(e, "sendto")

def recv_data(udp_sock):
  try:
    data, (ip, port) = udp_sock.recvfrom(512)
    print("Received %d bytes" % (len(data)))
    print(data.decode('utf-8'))
    return data.decode('utf-8'), ip, port
  except Exception as e:
    print_error(e, "recvfrom")
    return None, None, None
def checkState(gameState, flags):
    print("Checking Game state for win or tie")
    X = False
    O = False
    count = 0
    for i in gameState:
       if i == '1':
          count += 1
    if count == 9:
       print("Tie")
       flags = format(0, '014b')
       flags = flags[:4] + "1" + flags[5:]
    if flags[0] == '1':
        if gameState[0] == gameState[2] and gameState[0] == gameState [4] and gameState[0] == '1':
            print("X Wins") # Top Across
            X = True
        elif gameState[6] == gameState[8] and gameState[6] == gameState [10] and gameState[6] == '1':
            print("X Wins") # Middle Across
            X = True
        elif gameState[12] == gameState[14] and gameState[12] == gameState [16] and gameState[12] == '1':
            print("X Wins") # Bottom Across
            X = True
        elif gameState[0] == gameState[6] and gameState[0] == gameState [12] and gameState[0] == '1':
            print("X Wins") # Left Down
            X = True
        elif gameState[2] == gameState[8] and gameState[2] == gameState [14] and gameState[2] == '1':
            print("X Wins") # Middle Down
            X = True
        elif gameState[4] == gameState[10] and gameState[4] == gameState [16] and gameState[4] == '1':
            print("X Wins") # Right Down
            X = True
        elif gameState[0] == gameState[8] and gameState[0] == gameState [16] and gameState[0] == '1':
            print("X Wins") # Left Diagonal
            X = True
        elif gameState[4] == gameState[8] and gameState[4] == gameState [12] and gameState[4] == '1':
            print("X Wins") # Right Diagonal
            X = True
    else:
        if gameState[1] == gameState[3] and gameState[1] == gameState [5] and gameState[1] == '1':
            print("O Wins") # Top Across
            O = True
        elif gameState[7] == gameState[9] and gameState[7] == gameState [11] and gameState[7] == '1':
            print("O Wins") # Middle Across
            O = True
        elif gameState[13] == gameState[15] and gameState[13] == gameState [17] and gameState[13] == '1':
            print("O Wins") # Bottom Across
            O = True
        elif gameState[1] == gameState[7] and gameState[1] == gameState [13] and gameState[1] == '1':
            print("O Wins") # Left Down
            O = True
        elif gameState[3] == gameState[9] and gameState[3] == gameState [15] and gameState[3] == '1':
            print("O Wins") # Middle Down
            O = True
        elif gameState[5] == gameState[11] and gameState[5] == gameState [17] and gameState[5] == '1':
            print("O Wins") # Right Down
            O = True
        elif gameState[1] == gameState[9] and gameState[1] == gameState [17] and gameState[1] == '1':
            print("O Wins") # Left Diagonal
            O = True
        elif gameState[5] == gameState[9] and gameState[5] == gameState [13] and gameState[5] == '1':
            print("O Wins") # Right Diagonal
            O = True
    if X:
       flags = format(0, '014b')
       flags = flags[:2] + "1" + flags[3:]
    elif O:
       flags = format(0, '014b')
       flags = flags[:3] + "1" + flags[4:]
    return (X or O, flags)

def main():
  print(len(sys.argv))
  if len(sys.argv) >= 3:
    ip = sys.argv[1]
    try:
      port = int(sys.argv[2])
    except:
      print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
      sys.exit(1)
  else:
        # ip = input("Enter IP: ")
        ip = "192.168.1.12"
        print("IP: "+ip)
        try:
            # port = int(input("Enter Port: "))
            port = 2000
            print("Port: "+str(port))
        except:
            print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
            sys.exit(1)
  data = None
  if len(sys.argv) == 4:
    data = sys.argv[3]
    print("Will send %s to %s:%d via udp" % (data, ip, port))
  else:
    # print("Must enter data to send as argument to program")
    data = input("Enter Player Name: ")
    while len(data) > 35000:
       print("Msg is to long to send, please re-enter")
    #    data = input("Enter data to send: ")
       data = input("Enter Player Name: ")
    # gameID = str(np.random.randint(1,100))

  try:
    udp_sock = socket(AF_INET, SOCK_DGRAM)
    # name = input("Enter Player Name: ")
    # send_data(udp_sock, (ip, port), name)
    # incoming_data, sender_ip, sender_port = recv_data(udp_sock)


    gameID = ""
    for i in range(24):
       gameID += str(np.random.randint(0,2))
    serialID = format(0, '08b')
    # flags = format(0, '014b')
    flags = format(0, '013b')
    flags = "1"+flags #Flag for X to move first
    gameState = format(0, '018b')
    bitData = ''.join(format(ord(c),'b') for c in data)
    msg = str(gameID) + str(serialID) + str(flags) + str(gameState) + str(bitData)
    print("Msg to Send: "+str(len(msg)))
    print("Msg to Send: "+str(msg))
    send_data(udp_sock, (ip, port), msg)
    # print(flags)
    while flags[2] == '0' and flags[3] == '0' and flags[4] == '0':
        # print("In While")
        # Server Response
        incoming_data, sender_ip, sender_port = recv_data(udp_sock)
        print("Server Address: "+ str(sender_ip) +":"+str(sender_port))
        print("Reply: "+str(incoming_data))
        print("Game ID: "+ str(incoming_data[:24]))
        gameID = incoming_data[:24]
        print("Serial ID: "+ str(incoming_data[24:32]))
        serialID = incoming_data[24:32]
        serialID = int(serialID, 2) + 1
        serialID = format(serialID, '08b')
        print("Flags: "+ str(incoming_data[32:46]))
        flags = incoming_data[32:46]
        print("Game State: "+ str(incoming_data[46:64]))
        gameState = incoming_data[46:64]
        (decision, flags) = checkState(gameState, flags)
        if (decision):
            print("Game has been decided")
            if flags[2]:
                print("X has Won")
            elif flags[3]:
                print("O has Won")
            elif flags[4]:
                print("The Game is a Tie")
            break
        print("Name: "+ str(incoming_data[64:]))
        name = incoming_data[64:]
        if flags[0] == '1':
            print("You are X")
            move = int(input("Select an even bit spot between 0-16 to make your move: "))
            while move%2 != 0 or gameState[move+1] == '1' or gameState[move] == '1':
                if move%2 != 0: 
                    print("Position was not an even number")
                else:
                    print("Spot is already taken")
                move = int(input("Select an even bit spot between 0-16 to make your move: "))
            flags = "01" + flags[2:]
        elif flags[1] == '1':
            print("You are O")
            move = int(input("Select an odd bit spot between 1-17 to make your move: "))
            while move%2 != 1 or gameState[move-1] == '1' or gameState[move] == '1':
                if move%2 != 1:
                    print("Position was not an odd number")
                else:
                    print("Spot is already taken")
                move = int(input("Select an odd bit spot between 1-17 to make your move: "))
            flags = "10" + flags[2:]
        gameState = gameState[:move] + "1" + gameState[move+1:]


        msg = str(gameID) + str(serialID) + str(flags) + str(gameState) + str(name)
        print("Msg to Send: "+str(msg))
        send_data(udp_sock, (ip, port), msg)

  except Exception as e:
    print_error(e, "socket")

if __name__ == "__main__":
#   gameState = int(format(0, '018b'))
#   # gameState[0] = 1
#   print(gameState)
#   gameState += 1
#   print(format(gameState,'018b'))
#   gameID = ""
#   for i in range(24):
#     gameID += str(np.random.randint(0,2))
#   # gameID[0] = 0
#   gameID = int(gameID,2)
#   print(gameID)

#   data = "Test"
#   print(''.join(format(ord(c),'b') for c in data))

#   flags = format(0, '014b')
#   print(flags)
#   flags = int(flags, 2) + 1
#   print(flags)
#   flags = format(flags, '014b')
#   print(flags)
    # print("\tX")
    # spot = np.random.randint(0,8)
    # print(spot)
    # print(spot * 2)
    # print("\tO")
    # spot = np.random.randint(0,8)
    # print(spot)
    # print(spot * 2 + 1)

    # flags = format(0, '013b')
    # flags = "1"+flags #Flag for X to move first

    # print(flags[2] == '0')
    main()
