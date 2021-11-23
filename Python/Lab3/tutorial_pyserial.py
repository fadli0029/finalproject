import serial   # the PySerial Library
import datetime
import time     # for timing purposes

def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baudrate=baud_rate)
    return ser

def send_message(ser, message):
    if (message[-1] != '\n'):
        message = message + '\n'
    ser.write(message.encode('utf-8'))

def receive_message(ser, num_bytes=50):
    if (ser.in_waiting > 0):
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None

def close(ser):
    ser.close()

def main_2():
    ser = setup("/dev/ttyUSB0", 115200)
    time.sleep(3)
    send_message(ser, "fadli alim\n")
    time.sleep(3)
    close(ser)


def main():
    ser = setup("/dev/rfcomm0", 115200)
    the_message = datetime.datetime.now().strftime("%H:%M:%S")
    send_message(ser, the_message)
    # send_message(ser, "apa alim\n")
    time.sleep(1)
    message = receive_message(ser)
    print(message)
    close(ser)


"""
Main entrypoint for the application
"""

if __name__== "__main__":
    while True:
        main()
