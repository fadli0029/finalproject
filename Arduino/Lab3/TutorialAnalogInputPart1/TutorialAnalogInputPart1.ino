const int acce1X = A4;

void setup() {

  Serial.begin(9600);
  pinMode(acce1X, INPUT);

}

void loop() {

  int accel_val = analogRead(acce1X);
  Serial.println(accel_val);

}

/*
If we put the accelerometer flat on the desk, according to my
orientation of it, x is forward (+ve), y is to left (+ve), and z is out of paper (+ve)
*/
