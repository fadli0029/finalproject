from ECE16Lib.Communication import Communication
import time

if __name__ == "__main__":
    try:
        comms = Communication("/dev/rfcomm0", 115200)
        comms.clear()
        count = 0
        lastTime = 0
        for x in range(31):
            curr = time.time()
            if (curr - lastTime >= 1):
                count += 1
                comms.send_message(str(count))
                lastTime = curr
                time.sleep(1)
        print("Yeay! it worked!")
        comms.close()
    except KeyboardInterrupt:
        print("Bruh, the user did Ctrl-C")
    finally:
        print("Cleaning up and exiting the program")
