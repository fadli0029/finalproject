"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from time import sleep
import socket, pygame

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
  comms = None

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    lastState = False
    lastMessage =  None
    shoot = False
    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    while True:
      message = self.comms.receive_message()

      # if the last message is similar to current message,
      # don't send any message to avoid lagging due
      # to continuously sending messages 
      if ((message != lastMessage) and (message != None)):
        command = None
        message = int(message)

        if message == 23:
          command = "RFIRE"
        elif message == 24:
          command = "LFIRE"
        elif message == 20:
          command = "FIRE"
        elif message == 74:
          command = "LEFT"
        elif message == 73:
          command = "RIGHT"

        if command is not None:
          mySocket.send(command.encode("UTF-8"))

      lastMessage = message

if __name__== "__main__":
  #serial_name = "/dev/cu.BTDemo-ESP32SPP"
  serial_name = "/dev/ttyUSB0"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")
