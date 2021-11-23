const int  buttonPin = 12;

const long initEvent1 = 3000;
const long initEvent2 = 1000;
const long initEvent3 = 100;

long previousMillis_event1 = 0;
long previousMillis_event2 = 0;
long previousMillis_event3 = 0;


int timer = 0;
int currentState = 0;
int lastButtonState = LOW;

bool triggered = false;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}


void loop() {
  unsigned long currentMillis = millis(); // update frequently
  currentState = !digitalRead(buttonPin);

  if (currentState != lastButtonState) { // button is pressed
    if (currentState == HIGH) {
      timer++;
      triggered = false;
    }
    delay(50); // to remove debouncing, prolly not the best method
    lastButtonState = currentState; // update buttton state
  }

  if (currentMillis - previousMillis_event3 >= initEvent3) { // print every 100ms
    Serial.println(timer);
    previousMillis_event3 = currentMillis;
  }

  if (triggered == true) {
    if (timer > 0) {
      if (currentMillis - previousMillis_event2 >= initEvent2) {
        timer--;
        previousMillis_event2 = currentMillis;
      }
    }
  }

  if (currentMillis - previousMillis_event1 >= initEvent1) { // 3 seconds has passed
    triggered = true; // start activating countdown
    previousMillis_event1 = currentMillis; // update time
  }
}
