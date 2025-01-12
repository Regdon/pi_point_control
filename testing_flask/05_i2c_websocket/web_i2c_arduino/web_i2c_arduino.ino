#include <Wire.h>

const int SLAVE_ADDRESS = 0x08;

int led_state = 0;
String result = "";

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);

    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
    Serial.begin(9600);
    Serial.println("Setup and ready");
}

void loop() {
    if (led_state == 0) {
      digitalWrite(LED_BUILTIN, LOW);
    } else {
      digitalWrite(LED_BUILTIN, HIGH);
    }
    delay(100);
}

void receiveEvent(int howMany) {
    result = "";
    
    while (Wire.available()) {
        char c = Wire.read();
        if (int(c) != 0) {
          result += c;
        }
        Serial.println(int(c));
    }    
    result.trim();
    Serial.println(result);
    Serial.println(result.length());
    
    if (result == "on") {
      led_state = 1;
    } else if (result == "off") {
      led_state = 0;
    } else {
      led_state = 0;
      Serial.println("Unexpected request");
    }
}

void requestEvent() {
    Wire.write("Boo!");
}
