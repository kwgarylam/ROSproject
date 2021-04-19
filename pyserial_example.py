#define LED 13
String str;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    // 讀取傳入的字串直到"\n"結尾
    str = Serial.readStringUntil('\n');

    if (str == "LED_ON") {           // 若字串值是 "LED_ON" 開燈
        digitalWrite(LED, HIGH);     // 開燈
        Serial.println("LED is ON"); // 回應訊息給電腦
    } else if (str == "LED_OFF") {
        digitalWrite(LED, LOW);
        Serial.println("LED is OFF");
    }
  }
}
