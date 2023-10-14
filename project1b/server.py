from concurrent.futures import ThreadPoolExecutor
import sys
from socket import socket, SOCK_DGRAM, AF_INET
import numpy as np
def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))


def send_data(udp_sock, endpoint, data):
  try:
    ret = udp_sock.sendto(bytes(data, 'utf-8'), endpoint)
    print("Sent %d bytes" % (ret))
    return ret
  except Exception as e:
    print_error(e, "sendto")
    return 1


def recv_data(udp_sock):
  try:
    data, (ip, port) = udp_sock.recvfrom(512)
    print("Received %d bytes" % (len(data)))
    print(data.decode('utf-8'))
    return data.decode('utf-8'), ip, port
  except Exception as e:
    print_error(e, "recvfrom")
    return None, None, None
  

def gamePlay(udp_sock):
  side = np.random.randint(0,2)

  while True:
    try:
      incoming_data, sender_ip, sender_port = recv_data(udp_sock)
      print("Incoming data: "+incoming_data)
    except Exception as e:
      print_error(e, "recv_data")
      udp_sock.close()

    if len(incoming_data) > 0:
      try:
        
        Xmove = False
        Omove = False
        if side == 0:
          print("Server is O")
          Omove = True
        else:
          print("Server is X")
          Xmove = True
        print("Game ID: "+ str(incoming_data[:24]))
        print("Serial ID: "+ str(incoming_data[24:32]))
        print("Flags: "+ str(incoming_data[32:46]))
        print("Game State: "+ str(incoming_data[46:64]))
        print("Name: "+ str(incoming_data[64:]))

        gameID = incoming_data[:24]
        serialID = incoming_data[24:32]
        serialID = int(serialID, 2) + 1
        serialID = format(serialID, '08b')
        
        flags = incoming_data[32:46]
        gameState = incoming_data[46:64]
        if flags[2] == '0' and flags[3] == '0' and flags[4] == '0': # Game is not over yet
          if Xmove and flags[0] == '1': # Server makes its move
            print("Server choosing a spot for X")
            spot = np.random.randint(0,8) * 2 + 1
            print(spot)
            while gameState[spot-1] == '1' or gameState[spot] == '1':
              spot = np.random.randint(0,8) * 2 + 1
              # print(spot)
            flags = "01" + flags[2:]
            gameState = gameState[:spot] + "1" + gameState[spot+1:]
          elif Omove and flags[1] == '1':
            print("Server choosing a spot for O")
            spot = np.random.randint(0,8) * 2
            print(spot)
            while gameState[spot+1] == '1' or gameState[spot] == '1':
              spot = np.random.randint(0,8) * 2
              # print(spot)
            flags = "10" + flags[2:]
            gameState = gameState[:spot] + "1" + gameState[spot+1:]
        

        name = incoming_data[64:]
        return_data = str(gameID) + str(serialID) + str(flags) + str(gameState) + str(name)
        send_data(udp_sock, (sender_ip, sender_port), return_data)
      except Exception as e:
        print_error(e, "send_data")
        udp_sock.close()

def main():
  if len(sys.argv) == 3:
    ip = sys.argv[1]
    try:
      port = int(sys.argv[2])
    except:
      print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
      sys.exit(1)
  else:
    # print("Run with %s HOST PORT" % (sys.argv[0]))
    # sys.exit(1)
    
    # ip = input("Enter IP: ")
    ip = "192.168.1.11"
    print(ip)
    try:
        # port = int(input("Enter Port: "))
        port = 2000
        print(port)
    except:
        print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
        sys.exit(1)

  try:
    udp_sock = socket(AF_INET, SOCK_DGRAM)
  except Exception as e:
    print_error(e, "socket")
  
  try:
    udp_sock.bind((ip, port))
  except Exception as e:
    print_error(e, "bind")
  thread = ThreadPoolExecutor(max_workers=2)
  thread.submit(gamePlay, udp_sock)
  thread.submit(gamePlay, udp_sock)

if __name__ == "__main__":
  main()
