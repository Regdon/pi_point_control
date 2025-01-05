#include <Wire.h>

const int SLAVE_ADDRESS = 0x08;

void setup() {
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
    Serial.begin(9600);
}

void loop() {
    delay(100);
}

void receiveEvent(int howMany) {
    while (Wire.available()) {
        char c = Wire.read();
        Serial.print(c);
    }
    Serial.println();
}

void requestEvent() {
    Wire.write("Hello Pi");
}
