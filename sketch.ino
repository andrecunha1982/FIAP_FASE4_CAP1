#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); // Endereço I2C pode ser 0x27 ou 0x3F

//DTH Config
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// Relay, LDR e Botoes
#define RELAY_PIN 5
#define LDR_PIN 34
#define BUTTON_P 13
#define BUTTON_K 12

// nutrientes e irrigacao
bool fosforoPresente = false;
bool potassioPresente = false;
bool irrigationOn = false;

void setup() {
  Serial.begin(115200);

  dht.begin();
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUTTON_P, INPUT_PULLUP);
  pinMode(BUTTON_K, INPUT_PULLUP);
  
  
  lcd.begin(20, 4);
  lcd.init();
  lcd.backlight();
  
  lcd.setCursor(4, 0);
  lcd.print("Bem-vindo ao");
  lcd.setCursor(0, 1);
  lcd.print("Sistema de Irrigacao");
  lcd.setCursor(1, 2);
  lcd.print("do melhor grupo da");
  lcd.setCursor(8, 3);
  lcd.print("FIAP");
  delay(5000);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  int ldrValue = analogRead(LDR_PIN);
  float ph = map(ldrValue, 0, 4095, 5.5, 8.5);
  
  fosforoPresente = !digitalRead(BUTTON_P);
  potassioPresente = !digitalRead(BUTTON_K);
  
  if (h < 30.0) {
    irrigationOn = true;
    digitalWrite(RELAY_PIN, HIGH);
  } else if (h > 40.0) {
    irrigationOn = false;
    digitalWrite(RELAY_PIN, LOW);
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T: ");
  lcd.print(t);
  lcd.print("C ");
  lcd.print("U: ");
  lcd.print(h);
  lcd.print("%");
   
  lcd.setCursor(0, 1);
  lcd.print("pH: ");
  lcd.print(ph, 2);
  
  lcd.setCursor(0, 2);
  lcd.print("P: ");
  lcd.print(fosforoPresente ? "Sim" : "Nao");
  lcd.print(" K: ");
  lcd.print(potassioPresente ? "Sim" : "Nao");


  lcd.setCursor(0,3);
  lcd.print("Irrigacao: " );
  lcd.print(irrigationOn ? "ON" : "OFF");
  
  
  Serial.print("T: ");
  Serial.print(t);
  Serial.print("C | U: ");
  Serial.print(h);
  Serial.print("%, pH: ");
  Serial.println(ph, 1);
  Serial.print("Fósforo: ");
  Serial.println(fosforoPresente ? "Sim" : "Nao");
  Serial.print("Potássio: ");
  Serial.println(potassioPresente ? "Sim" : "Nao");
  Serial.print("Irrigacao: ");
  Serial.print(irrigationOn ? "ON" : "OFF");
  
  delay(3000);
}
