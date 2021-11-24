import socket, pygame
import time
# Setup the Socket connection to the Space Invaders game
# CLIENT
host = "127.0.0.1"
port = 65432
tester = ("127.0.0.1", 65432)
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)


while True:
  time.sleep(2)
  mySocket.send("-1,-1,-1,0".encode("utf-8"))
  time.sleep(2)
  mySocket.send("0,0,-1,-1".encode("utf-8"))
  time.sleep(2)
  mySocket.send("1,1,-1,-1".encode("utf-8"))
  time.sleep(2)
  mySocket.send("-1,-1,1,-1".encode("utf-8")) # X,Y rows and col ,reset 1 for reset 0 for nothing, mode selection at begining 0 to 3
  time.sleep(2)



  try:
    data = mySocket.recv(1024)
    data = data.decode("utf-8")
    print("Response: " + data)
  except BlockingIOError:
    pass # do nothing if there's no data

mySocket.close()
pygame.quit()
