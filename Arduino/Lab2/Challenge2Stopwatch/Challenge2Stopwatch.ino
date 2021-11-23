const int  buttonPin = 12;

unsigned long previousMillis_event1 = 0;
unsigned long previousMillis_event2 = 0;

const long initEvent1 = 1000;
const long initEvent2 = 100;

int counter = 0;
int currentState = 0;
int lastButtonState;

bool stopWatchOn = false;
bool printing = false;
bool oldStatus;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}


void loop() {
  unsigned long currentMillis = millis(); // update frequently
  currentState = !digitalRead(buttonPin);
  // i inverted the readvalue, coz originally
  // a 0 means pressed for my button.
  // so, after inverting, a 1 should mean pressed.

  if (currentState != lastButtonState) { // button is pressed
    if (currentState == HIGH) {
      if (counter == 0) { 
        // means there's no way the button is pressed unless with
        // the intent of starting the timer
        stopWatchOn = true;
        printing = true;
      }
      else if (counter != 0) {
        // it could be the case that the person wants to pause the timer
        // or it could also be the case that the person paused before 
        // and now pressed the button again to resume. How do you
        // differentiate between the two?
        
        // I assign the last status of the stopwatch,
        // i.e: whether it was paused or not, to a variable
        // called oldStatus. If last time it was running,
        // then set oldStatus will hold the value true, and
        // then button is clicked, stopWatchOn will store false,
        // which stops counter incrementation.
        // if last time it was false, i.e: it was paused before,
        // then it will make stopWatchOn hold true, and hence
        // initiate counter incrementation again.
        if (oldStatus == false) {
          stopWatchOn = true; // resume
          printing = true; // resumed, so continue printing counter
        }
        if (oldStatus == true) {
          stopWatchOn = false; // paused
          printing = false; // paused, so stop printing counter
        }
      }
    }
    delay(50); // to remove debouncing, prolly not the best method
  }
  lastButtonState = currentState;

  if (printing == true) {
    if (currentMillis - previousMillis_event2 >= initEvent2)
    {
      // just print the counter every 100 ms
      Serial.println(counter);
      previousMillis_event2 = currentMillis;
    }
  }

  if (stopWatchOn == true) {
    // increment counter
    if(currentMillis - previousMillis_event1 >= initEvent1) 
    { // check if the difference between the current elapsed time (currentMillis)
      // and previousMillis, which was initially 0 but it is shifted
      // forward everytime they are separated by 1 second, by assigning it to currenMillis,
      // so everytime this happens, we know 1 second has passed, and hence
      // increment counter
      counter++;
      previousMillis_event1 = currentMillis; // update previous time for next iteration
    }
  }
  oldStatus = stopWatchOn; // remember last status of stopwatch
}
