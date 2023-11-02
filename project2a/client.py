#!/opt/local/bin/python3.7

import sys
from socket import socket, SOCK_STREAM, AF_INET
from select import select
import json

def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))


def send_data(tcp_sock, data):
  try:
    ret = tcp_sock.send(bytes(data, 'utf-8'))
  except KeyboardInterrupt as k:
    raise KeyboardInterrupt()
  except Exception as e:
    print_error(e, "send")


def recv_data(tcp_sock):
  try:
    data = tcp_sock.recv(4096)
    if len(data) == 0:
      return False
    print("Server said: " + data.decode('utf-8'))
    return True
  except Exception as e:
    print_error(e, "recv")

def main():
  if len(sys.argv) >= 3:
    ip = sys.argv[1]
    try:
      port = int(sys.argv[2])
    except:
      print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
      sys.exit(1)
  else:
    ip = "localhost"
    port = 2001
  data = None

  # Create socket to connect to the server
  try:
    tcp_sock = socket(AF_INET, SOCK_STREAM)
  except Exception as e:
    data = 'quit\n'
    print_error(e, "socket")

  # Attempt to connect to server
  try:
    tcp_sock.connect((ip, port))
    print("Connected to {}:{}".format(ip,port))
  except Exception as e:
    data = 'quit\n'
    print_error(e, "connect")

  # We're using select, so set socket to non-blocking just in case
  tcp_sock.setblocking(0)
  # Add client (tcp_sock) and stdin to list of read FDs
  read_sockets = [tcp_sock, sys.stdin]
  json_dic = {"action":"connect","user_name":"@","targets":[]}
  msg_dic = {"action":"message", "user_name":"@", "target":"", "message":""}
  if data != 'quit\n':
    print("JSON Dictionary:"+str(json.dumps(json_dic)))
    print("Enter user name: ")
    data = sys.stdin.readline()
    json_dic["user_name"] += data[:len(data)-1]
    #bytes(data, 'utf-8')
    # print(sys.getsizeof(json_dic["user_name"]))
    # print(sys.getsizeof(bytes(json_dic["user_name"], 'utf-8')))
    while sys.getsizeof(bytes(json_dic["user_name"], 'utf-8'))-33 > 60:
      print("Enter a shorter user name: ")
      data = sys.stdin.readline()
      json_dic["user_name"] = "@"+str(data[:len(data)-1])
    while data != "q\n":
      print("Enter target or q to exit: ")
      data = sys.stdin.readline()
      # print(sys.getsizeof("#"+data[:len(data)-1]))
      # print(sys.getsizeof(bytes("#"+data[:len(data)-1], 'utf-8')))
      if data == "q\n":
        break
      while sys.getsizeof(bytes("#"+data[:len(data)-1], 'utf-8'))-33 > 60:
        print("Enter a shorter target: ")
        data = sys.stdin.readline()
        # print(sys.getsizeof(bytes("#"+data[:len(data)-1], 'utf-8')))
      json_dic["targets"].append("#"+data[:len(data)-1])
    print("Client connet message: "+str(json_dic))
  try:
    send_data(tcp_sock, json.dumps(json_dic))
    while data != 'quit\n':
      readlist, writelist, _ = select(read_sockets, [], [], 1)
      # print("Selected")
      try:
        if tcp_sock in readlist:
          if recv_data(tcp_sock) == False:
            print("Server went away, shutting down.")
            data = 'quit\n'

        if sys.stdin in readlist:
          data = sys.stdin.readline()
          if data == "msg\n":
            print("Before: " + str(json.dumps(msg_dic)))
            msg_dic["user_name"] = json_dic["user_name"]
            print("Enter target to message (include the user @ or room #): ")
            data = sys.stdin.readline()
            # print(sys.getsizeof(data[:len(data)-1]))
            # print(sys.getsizeof(bytes(data[:len(data)-1], 'utf-8')))
            while sys.getsizeof(bytes(data[:len(data)-1], 'utf-8'))-33 > 60:
              print("Enter a shorter target: ")
              data = sys.stdin.readline()
              # print(sys.getsizeof(data[:len(data)-1]))
              print(sys.getsizeof(bytes(data[:len(data)-1], 'utf-8')))
            msg_dic["target"] = data[:len(data)-1]

            print("Enter message to send: ")
            data = sys.stdin.readline()
            # print(sys.getsizeof(data[:len(data)-1]))
            print(sys.getsizeof(bytes(data[:len(data)-1], 'utf-8')))
            while sys.getsizeof(bytes(data[:len(data)-1], 'utf-8'))-33 > 3800:
              print("Enter shorter message to send: ")
              data = sys.stdin.readline()
              # print(sys.getsizeof(data[:len(data)-1]))
              print(sys.getsizeof(bytes(data[:len(data)-1], 'utf-8')))

            msg_dic["message"] = data[:len(data)-1]

            print("After: " + str(json.dumps(msg_dic)))
            if data != 'quit\n':
              send_data(tcp_sock, json.dumps(msg_dic))
          elif data == 'exit\n' or data == 'quit\n':
            print("Got client quit.")
            break
          elif data != 'quit\n':
            send_data(tcp_sock, json.dumps(json_dic))
          else:
            # print("Got client quit.")
            print("Unrecognized command: Please enter msg or exit/quit command")
      except KeyboardInterrupt as e:
        print("Got keyboard kill")
        data = 'quit\n'
        

  except Exception as e:
    print_error(e, "send_data")

  finally:
    print("Closing")
    json_dic = {"action":"disconnect"}
    send_data(tcp_sock, json.dumps(json_dic))
    tcp_sock.close()

if __name__ == "__main__":
  main()
