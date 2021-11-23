int row = 0;

void setup() {
  setupCommunication();
  setupDisplay();
}

void loop() {
  String message1 = receiveMessage();
  if(message1 != "") {
    writeDisplay(message1.c_str(), row, true);
    sendMessage(message1);
    row++;
    if (row == 4) {
      row = 0;
    }
  }
  // I increment row for every message 
  // to allow me to print them in different lines
  // because I am sending 4 messages
}
