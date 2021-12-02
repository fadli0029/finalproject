// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;              // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0;       // Time of last sample (in Sampling tab)
const int buttonPin1 = /*0;*/ 12;
const int buttonPin2 = 0; /*12;*/
int x = 0;
int y = 0;
bool sending, oldStatus1, oldStatus2, both;

int currentState1 = 0;
int lastButtonState1;
int currentState2 = 0;
int lastButtonState2;
bool bothlast = false;
bool resetState = false;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupMotor();
  sending = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);

  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
}

void loop() {

  String command = receiveMessage();
  if(command == "stop") {
    writeDisplay("Controller: Off", 0, true);
  }

  else if(command == "start") {
    writeDisplay("Controller: On", 0, true);
  }


  else if(command == "choose") {
    sending = false;  // added [Fade]
      
    while(1) {
      writeDisplay("Select Tile!", 0, true);
      String h = "x: "+String(x)+" y: "+String(y);
      writeDisplay(h.c_str(), 1, false);
      currentState1 = !digitalRead(buttonPin1);
      currentState2 = !digitalRead(buttonPin2);

      // sending to computer
      both  = currentState1 && currentState2;
      // if button 1 and 2 send and break
      if(both != bothlast) {
        if(both) {
          writeDisplay("Selecting",0,true);
          sendMessage(String(x)+","+ String(y));
          break;
        }
      }
      bothlast = both;
      
      // if button 1 ++
      if (currentState1 != lastButtonState1) { 
        if (currentState1) {
          x++;
        }
        if(x == 7) {
          x = 0;
        }
      }
      lastButtonState1 = currentState1;

      // if button 2 ++
      if (currentState2 != lastButtonState2) { 
        if (currentState2) {
          y++;
        }
        if(y == 7) {
          y = 0;
        }
      }
      lastButtonState2 = currentState2;
    }
  }else if(command =="jj") {
    sending = true;
    writeDisplay("",0,true);

  }else if(command == "Won"){
    writeDisplay("You Won!!!      ",0,true);
   // writeDisplay("Press R to reset",1,false);
    resetState = true;
  }else if(command == "Loss"){
    writeDisplay("Game Over!      ",0,true);
    //writeDisplay("Press R to reset",1,false);
    resetState = true;

  }else if(command != ""){
    writeDisplayCSV(command,1);
  }

//   if(resetState){
//     resetState = false;
//     sending = false;
//     x=0;
//     y=0;
//     while(1){
//       currentState1 = !digitalRead(buttonPin1);
//       if (currentState1 != lastButtonState1) {
//         if (currentState1) {
//           sendMessage("Reset");
//           break;
//         }
//       }
//       lastButtonState1 = currentState1;
//     }
//   }




  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);
  }
}
