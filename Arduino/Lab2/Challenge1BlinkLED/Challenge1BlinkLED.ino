//pins location (for my own convenience coz the teensy is burried, 
//into the breadboard, and im too lazy to open the schematic everytime)
//2v3, 2nd from bottom (longer side)
//gnd, 4th from bottom (longer side)
//gpio pin 12 (better use thi), 5th from bottom (shorter side)

const int led_pin = 12;
const float freq1 = 1.00;
const float freq2 = 10.00;
const float freq3 = 50.00;

unsigned long freq_input(float freq) {
  unsigned long the_delay;
  unsigned long period;
  period = (1 / freq) * 1000;
  the_delay = period/2;
  return (the_delay);
}
// basically a function that lets me
// input a freq, it then changes it
// to period, i.e: time between on off and on again.
// so i divde it by 2,
// and return the_delay, which will be passed
// to delay() function

void customBlink(int onTime, int offTime, int pin) {
  digitalWrite(pin, HIGH);
  delay(onTime);
  digitalWrite(pin, LOW);
  delay(offTime);
}

void setup() {
  pinMode(led_pin, OUTPUT);
}

/* For 1st part of Challenge1BlinkLED - uncomment to test */
/*
void loop() {
  digitalWrite(led_pin, HIGH);
  delay(freq_input(freq3));
  digitalWrite(led_pin, LOW);
  delay(freq_input(freq3));
}
*/

/* For 2nd part of Challenge1BlinkLED - uncomment to test */

void loop() {
  customBlink(20, 10, led_pin);
}

