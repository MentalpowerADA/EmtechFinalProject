#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,  16, 2);

int x;
int piezo = 4;
int red = 3;
int green = 2;

void setup() {
  lcd.init();
  lcd.backlight();
  pinMode(piezo, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  digitalWrite(red, LOW);
  digitalWrite(green, LOW);
  Serial.begin(9600);
  Serial.setTimeout(1);
  lcd.setCursor(0,0);
  lcd.print("Facial Biometric");
  lcd.setCursor(0,1);
  lcd.print("Security System");
}
bool isOn = false;
void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  if(x == 1){
    lcd.clear();
    Serial.print("    Scanning    ");
    lcd.setCursor(0,0);
    lcd.print("    Scanning    ");
    if (isOn == true){
      digitalWrite(red, LOW);
      digitalWrite(green, LOW);
      isOn = false;
    }
    else{
      digitalWrite(red, LOW);
      digitalWrite(green, HIGH);
      isOn = true;
    }
  }
  if(x == 2){
    lcd.clear();
    Serial.print("passed");
    lcd.setCursor(0,0);
    lcd.print("    Access");
    lcd.setCursor(0,1);
    lcd.print("    Granted");
    digitalWrite(green, HIGH);
    digitalWrite(red, LOW);
  }
  if(x == 3){
    lcd.clear();
    Serial.print("failed");
    lcd.setCursor(0,0);
    lcd.print("  Scan Failed!");
    lcd.setCursor(0,1);
    lcd.print("  Unrecognized");

    digitalWrite(red, HIGH);
    digitalWrite(green, LOW);
  }
  if(x == 4){
    lcd.clear();
    Serial.print("too many failed attempts");
    lcd.setCursor(0,0);
    lcd.print("    Too Many");
    lcd.setCursor(0,1);
    lcd.print("Failed Attempts!");
    
    digitalWrite(red, HIGH);
    digitalWrite(green, LOW);
    digitalWrite(piezo, HIGH);
  }
}