from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
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
    ped = None
    ref_t = 0 # refresh time

    def __init__(self, serial_name, baud_rate, num_samples=250, fs=50, rt=0.1):
        self.comms = Communication(serial_name, baud_rate)
        self.ped = Pedometer(num_samples, fs, [])
        self.ref_t = rt

    def run(self):
        # 1. make sure data sending is stopped by ending streaming
        self.comms.send_message("stop")
        self.comms.clear()

        # 2. start streaming orientation data
        input("Ready to start? Hit enter to begin.\n")

        self.comms.send_message("start")
        self.comms.clear()
        self.ped.threshSetter(100, 850)   # to set the threshold for DSP

        # 3. Forever collect orientation and send to PyGame until user exits
        print("Use <CTRL+C> to exit the program.\n")

        isClicked = False   # check if button is click
        sendChoose = True   # send choose command
        GameOver = False    # checking game state

        prev_x = 0          # track previous coord specified
        prev_y = 0          # track previous coord specified
        jj_n = 0            # number of jumping jacks required hehe

        while True:
            try:
                # send W/L message to MCU
                data = mySocket.recv(1024)
                data = data.decode("utf-8")
                if not GameOver:
                    controller.comms.send_message(data)
                if data != None:
                    GameOver = True

            except BlockingIOError:
                pass  # do nothing if there's no data

            # ask player to input(choose) coordinate
            if sendChoose and not GameOver:
                controller.comms.send_message("choose")
                sendChoose = False

                
            # receives coordinates inputted by player
            message = self.comms.receive_message()
            if message != None:
                print(message)

            if (message != None) and not GameOver:
                print("Waiting for User to enter coordinates...")
                try:
                    (x, y) = message.split(',')
                    jj_n = abs(prev_x - int(x)) + abs(prev_y - int(y))
                    # [where 'jj_n' is the number of jumping jacks needed]
                    print("Jumping Jacks required: " + str(jj_n))
                    prev_x = int(x)
                    prev_y = int(y)
                    sendChoose = True # update sendChoose
                    isClicked = True  # update isClicked for jumping jacks later
               
                except ValueError:  # if corrupted data, skip the sample
                    continue

            if (message != None) and (message == "Reset\r\n"):   # reset game
                mySocket.send(("R").encode("UTF-8"))
                prev_x = 0
                prev_y = 0
                GameOver = False
                sleep(0.5)
                try:
                    a = mySocket.recv(1024)
                except BlockingIOError:
                    pass  # do nothing if there's no data

            f_command = None
            if (isClicked):
                validate = True     # ask for jumping jacks
                self.ped.resetVal() # reset jumping jacks value
                prev_time = 0
                print("Counting your jumping jacks...")
                self.comms.clear()
                # send message to MCU, begin taking sensor data
                controller.comms.send_message("jj")
                while (validate):
                    msg = self.comms.receive_message()
                    if(msg != None):
                        try:
                            (m1, m2, m3, m4) = msg.split(',')
                        except ValueError:
                            continue

                        # add the new values to the circular lists
                        self.ped.add(int(m2),int(m3),int(m4))

                        current_time = time()
                        if (current_time - prev_time > self.ref_t):
                            prev_time = current_time
                            # begin  processing data
                            track_jumps, peaks, filtered = self.ped.process()
                            print("You did " + str(track_jumps) + " Jumping Jacks!")
                            controller.comms.send_message("Jumping Jacks   ,Required: "+str(jj_n-track_jumps))
                            if (track_jumps >= jj_n):
                                validate = False # update validate

                # display number of jumping jacks completed
                controller.comms.send_message("Jumping Jacks!  ,Completed!!!    ")
                print("Jumping Jacks VALIDATED!")
                print("sending coordinates to server...")
                            
                f_command = "click" + "," + str(x) + "," + str(y)

            # send command(coordinate) to server
            if f_command is not None:
                mySocket.send(f_command.encode("UTF-8"))
                sleep(0.5)
                try:
                    a = mySocket.recv(1024)
                except BlockingIOError:
                    pass  # do nothing if there's no data

            isClicked = False # reset isClicked status to False


if __name__ == "__main__":

    serial_name = "/dev/cu.esp32Spark-ESP32SPP"    # [JUSTIN]
    #serial_name = "/dev/cu.BTDemoMine-ESP32SPP"   # [JUSTIN]
    #serial_name = "/dev/ttyUSB0"                  # [FADE]
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
