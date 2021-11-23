// setting PWM properties
const int pwmFrequency = 5000;    // Set the PWM frequency to 5kHZ
const int pwmChannel = 0;         // Use PWM channel 0
const int pwmBitResolution = 8;   // Set a PWM resolution of 8 bits 

const int MOTOR_PIN = 18;

void setupMotor() {

  ledcSetup(pwmChannel, pwmFrequency, pwmBitResolution);
  // attach the PWM channel to the output GPIO to be controlled
  ledcAttachPin(MOTOR_PIN, pwmChannel);

}

void activateMotor(int motorPower) {
  
  ledcWrite(pwmChannel, motorPower);

}

void deactivateMotor() {

  ledcWrite(pwmChannel, 0);

}
