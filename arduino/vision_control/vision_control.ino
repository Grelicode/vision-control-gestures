#include <LiquidCrystal.h>

LiquidCrystal lcd(A0, A1, A2, A3, A4, A5);
const int BUZZER = 3;

char tryb = '0';
unsigned long liczbaStartow = 0;

void pokazStan() {
  // Zielone D10–D11, zolte D12–D13, czerwone D8–D9.
  digitalWrite(10, tryb == '1');
  digitalWrite(11, tryb == '1');
  digitalWrite(12, tryb == 'R');
  digitalWrite(13, tryb == 'R');
  digitalWrite(8, tryb == '0');
  digitalWrite(9, tryb == '0');

  lcd.setCursor(0, 0);
  if (tryb == '1') {
    lcd.print("TRYB: RUN       ");
  } else if (tryb == 'R') {
    lcd.print("TRYB: RESET     ");
  } else {
    lcd.print("TRYB: STOP      ");
  }

  lcd.setCursor(0, 1);
  lcd.print("STARTY:         ");
  lcd.setCursor(8, 1);
  lcd.print(liczbaStartow);
}

void setup() {
  Serial.begin(9600);
  for (int pin = 8; pin <= 13; pin++) {
    pinMode(pin, OUTPUT);
  }
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  lcd.begin(16, 2);
  pokazStan();
}

void loop() {
  if (Serial.available() == 0) {
    return;
  }

  char polecenie = Serial.read();

  if (polecenie == '1') {
    if (tryb != '1') {
      liczbaStartow++;
      noTone(BUZZER);
      tone(BUZZER, 1000, 150);
    }
  } else if (polecenie == '0') {
    noTone(BUZZER);
    tone(BUZZER, 1000);  // Gra do nastepnego START lub RESET.
  } else if (polecenie == 'R') {
    liczbaStartow = 0;
    noTone(BUZZER);
    tone(BUZZER, 1000, 400);
  } else {
    return;
  }

  tryb = polecenie;
  pokazStan();
}