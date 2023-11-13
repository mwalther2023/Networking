#!/opt/local/bin/python3.7

import sys
from socket import socket, SOCK_STREAM, AF_INET
from select import select
import traceback
import json

def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))
    traceback.print_exc()
history = {"status":"chat","history":[]}
errorMsg = {"status":"error","message":"This is an error message."}
clientList = {"id":[], "rooms":[], "socket":[]}
def recv_data(tcp_sock):
  try:
    data = tcp_sock.recv(4096)
    # Indicates client has disconnected
    if len(data) == 0:
      return False
    print("Received %d bytes" % (len(data)))
    msg = json.loads(data.decode('utf-8'))
    print("Msg: "+str(msg))
    if sys.getsizeof(bytes(msg["user_name"], 'utf-8'))-33 > 60:
      tcp_sock.send(bytes(json.dumps(errorMsg), 'utf-8'))
    elif sys.getsizeof(bytes(msg["target"], 'utf-8'))-33 > 60:
      tcp_sock.send(bytes(json.dumps(errorMsg), 'utf-8'))
    elif sys.getsizeof(bytes(msg["message"], 'utf-8'))-33 > 3800:
      tcp_sock.send(bytes(json.dumps(errorMsg), 'utf-8'))
    elif "targets" in msg:
      for s in msg["targets"]:
        if sys.getsizeof(bytes(s, 'utf-8'))-33 > 60:
          tcp_sock.send(bytes(json.dumps(errorMsg), 'utf-8'))
          break
    # print(type(msg))
    print(msg["action"])
    if msg["action"] == "message":
      chat = {"target":msg["target"], "from":msg["user_name"], "message":msg["message"]}
      history["history"].append(chat)
      print("History: "+str(history))

      if msg["target"][0] == "@":
        print("DM: "+str(msg["target"]))
        for u in range(len(clientList["id"])):
          if clientList["id"][u] == msg["target"]:
            outMsg = "{} says to {}: {}".format(msg["user_name"],msg["target"],msg["message"])
            clientList["socket"][u].send(bytes(outMsg, 'utf-8'))
      elif msg["target"][0] == "#":
        print("Chat Room: "+str(msg["target"]))
        for u in range(len(clientList["rooms"])):
          for i in range(len(clientList["rooms"][u])):
            if clientList["rooms"][u][i] == msg["target"] and clientList["id"][u] != msg["user_name"]:
              outMsg = "{} says to {}: {}".format(msg["user_name"],msg["target"],msg["message"])
              clientList["socket"][u].send(bytes(outMsg, 'utf-8'))
      else:
        tcp_sock.send(bytes(json.dumps(errorMsg), 'utf-8'))

    elif msg["action"] == "connect":
      clientList["id"].append(msg["user_name"])
      clientList["rooms"].append(msg["targets"])
      clientList["socket"].append(tcp_sock)
      print(clientList)
    else:
      tcp_sock.send(bytes(json.dumps(errorMsg), 'utf-8'))
    # Echo the data back to the client
    # tcp_sock.send(data)
    tcp_sock.send(bytes(json.dumps(history), 'utf-8'))
    return True
  except BlockingIOError as b:
    print("Recv failed due to non-blocking IO, this means the client has disconnected?")
    return False
  except Exception as e:
    print_error(e, "recv")
    return False

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
    ip = "localhost"
    port = 2001

  try:
    server_sock = socket(AF_INET, SOCK_STREAM)
  except Exception as e:
    print_error(e, "socket")
    sys.exit(1)
  
  try:
    server_sock.bind((ip, port))
    print("Binded on {}:{}".format(ip,port))

  except Exception as e:
    print_error(e, "bind")
    sys.exit(1)

  try:
    server_sock.listen(10)
  except Exception as e:
    print_error(e, "listen")
    sys.exit(1)

  read_sockets = []
  write_sockets = []
  except_sockets = []
  
  read_sockets.append(server_sock)
  except_sockets.append(server_sock)
  quit = False

  readlist, writelist, exceptlist = [], [], []
  
  while (quit == False):
    try:
      # print(read_sockets)
      readlist, writelist, exceptlist = select(read_sockets, write_sockets, except_sockets, 2)
      # print("ReadList: "+str(readlist))
      # print("WriteList: "+str(writelist))
    except KeyboardInterrupt as k:
      quit = True
    except Exception as e:
      print_error(e, "select")

    if server_sock in readlist:
      try:
        client_sock, (client_ip, client_port) = server_sock.accept()
        client_sock.setblocking(0)
        read_sockets.append(client_sock)
        write_sockets.append(client_sock)
        except_sockets.append(client_sock)
        continue
      except KeyboardInterrupt as k:
        quit = True
      except Exception as e:
        print_error(e, "accept")

    for client in read_sockets:
      # Means client has sent us data
      if client in readlist:
        try:
          ret = recv_data(client)
          print("Data: "+str(ret))
          if ret == False:
            print("Closing client socket.")
            client.close()
            read_sockets.remove(client)
            except_sockets.remove(client)
        except KeyboardInterrupt as k:
          quit = True
        except Exception as e:
          print_error(e, "recv_data")

      if client in exceptlist:
        print("Closing client socket (client in except?).")
        client.close()
        read_sockets.remove(client)
        except_sockets.remove(client)
  try:
    print("Closing sockets.")
    json_dic = {"status":"disconnect"}
    server_sock.close()
    for client_sock in read_sockets:
      client_sock.send(json.dumps(json_dic))
      client_sock.close()
  except:
    pass
if __name__ == "__main__":
  main()
