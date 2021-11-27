// ----------------------------------------------------------------------------------------------------
// =========== Accelerometer Sensor ============ 
// ----------------------------------------------------------------------------------------------------

/*
 * Configure the analog input pins to the accelerometer's 3 axes
 */
const int X_PIN = A2;
const int Y_PIN = A3;
const int Z_PIN = A4;

/*
 * Set the "zero" states when each axis is neutral
 * NOTE: Customize this for your accelerometer sensor!
 */

// DEFAULT - Ramsin's: 
//const int X_ZERO = 1850;
//const int Y_ZERO = 1850;
//const int Z_ZERO = 1950;

// CUSTOMIZED - Fade's:
// NOTE: Better sensitivity imo, 
// experiment for yourself :) .
const int X_ZERO = 1970;
const int Y_ZERO = 1900;
const int Z_ZERO = 2350;


/*
 * Configure the analog pins to be treated as inputs by the MCU
 */
void setupAccelSensor() {
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

/*
 * Read a sample from the accelerometer's 3 axes
 */
void readAccelSensor() {
  ax = analogRead(X_PIN); 
  ay = analogRead(Y_PIN);
  az = analogRead(Z_PIN);
}

/*
 * Get the orientation of the accelerometer
 * Returns orientation as an integer:
 * 0 == flat
 * 1 == up
 * 2 == down
 * 3 == left
 * 4 == right
 */
int getOrientation() {
  int orientation = 0;

  // Subtract out the zeros
  // i.e: measuring how much the value changed
  int x = ax - X_ZERO;
  int y = ay - Y_ZERO;
  int z = az - Z_ZERO;

  // If ax has biggest magnitude, it's either left or right
  if(abs(x) >= abs(y) && abs(x) >= abs(z)) {
    if( x < 0 ) // left
      // ax < X_ZERO
      orientation = 3;
    else        // right
      // ax > X_ZERO
      orientation = 4;
  }
  // If az biggest magnitude, it's flat (or upside-down)
  else if(abs(z) > abs(x) && abs(z) >= abs(y)) {
    orientation = 7; // flat, not shooting, not moving
  }
  return orientation;
}
