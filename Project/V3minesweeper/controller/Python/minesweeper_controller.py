from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from time import sleep
from time import time
import socket, pygame
import numpy as np

# Setup the Socket connection to the Space Invaders game
# CLIENT
host = "127.0.0.1"
port = 65432
tester = ("127.0.0.1", 65432)
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)


class PygameController:
    comms = None

    def __init__(self, serial_name, baud_rate):
        self.comms = Communication(serial_name, baud_rate)

    def run(self):
        # 1. make sure data sending is stopped by ending streaming
        shoot = False

        self.comms.send_message("stop")
        self.comms.clear()

        # 2. start streaming orientation data
        input("Ready to start? Hit enter to begin.\n")
        self.comms.send_message("start")

        # 3. Forever collect orientation and send to PyGame until user exits
        print("Use <CTRL+C> to exit the program.\n")
        previous_time = 0

        prev_x = 0
        prev_y = 0
        previous_time = time()
        while True:
            isclicked = 0
            # must send choose to enter state needs to be fixed to be sent to this state via a command
            # if enough time has elapsed, clear the axis, and plot az
            current_time = time()
            if (current_time - previous_time > 4):
              previous_time = current_time
              controller.comms.send_message("choose")

            message = self.comms.receive_message()

            if (message != None):
                f_command = None
                try:
                    m0 = message
                    print("m0: " + str(m0))
                    (x, y) = message.split(',')
                    isclicked = 2
                    a = abs(prev_x -int(x))+abs(prev_y - int(y))
                    prev_x = int(x)
                    prev_y = int(y)
                    controller.comms.send_message("Payment Required,"+str(a)+" Jumping Jacks")

                except ValueError:  # if corrupted data, skip the sample
                    print("failed")
                    continue

                # if enough time has elapsed, clear the axis, and plot az
                # current_time = time()
                # if (current_time - previous_time > 0.01):
                #  previous_time = current_time

                if isclicked == 2:
                    f_command = "click," + str(x) + "," + str(y)
                # elif isclicked == 7:
                #  f_command = "noclick"

                if f_command is not None:
                    print(f_command)
                    mySocket.send(f_command.encode("UTF-8"))

                # try:
                #    data = mySocket.recv(1024)
                #    data = data.decode("utf-8")
                #    controller.comms.send_message(data)
                #    #print("Response: " + data)
                # except BlockingIOError:
                #    pass  # do nothing if there's no data


if __name__ == "__main__":

    # the_num_samples = 100               # 2 seconds of data @ 50Hz
    # the_refresh_time = 0.01             # update the processing every 0.01s
    # sensitivity = 2

    serial_name = "/dev/cu.esp32Spark-ESP32SPP"
    # serial_name = "/dev/ttyUSB0"
    baud_rate = 115200
    # controller = PygameController(serial_name, baud_rate, the_num_samples, the_refresh_time, sensitivity)
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
