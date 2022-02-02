#include <SPI.h>

const int stepPin = 4;
const int dirPin = 3;

void setup()
{
  Serial.begin(9600);
  pinMode(12, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(5, INPUT_PULLUP);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  digitalWrite(7, HIGH);
}

int s;
void loop()
{
  if (digitalRead(12) == LOW || Serial.read()=='s')
    {
      Serial.println("pp");
      digitalWrite(7, LOW);
      digitalWrite(dirPin, HIGH);
      for(int x = 0; x < 70; x++){
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1500);
      }
      delay(1000);
      digitalWrite(7, HIGH);
      digitalWrite(dirPin, LOW);
      for(int x = 0; x < 70; x++){
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1500);
      }
      serialFlush();
    }
    else
    {
      buttonCheck();
    }
}
void buttonCheck(){
  if (digitalRead(5) == LOW)
  {
    Serial.print("d");
    //digitalWrite(7,LOW);
    for (int t = 0; t < 10; t++)
    {
      digitalWrite(7, LOW);
      delay(200);
      digitalWrite(7, HIGH);
      delay(200);
    }
  }
  else
  {
    //digitalWrite(7,HIGH);
  }
}
void serialFlush() {
  while (Serial.available() > 0) {
    char t = Serial.read();
  }
}
