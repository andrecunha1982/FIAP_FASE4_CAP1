#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <RTClib.h>

// Definindo os pinos I2C no ESP32
#define SDA_PIN 26
#define SCL_PIN 27

RTC_DS1307 ds1307_rtc;
LiquidCrystal_I2C lcd(0x27, 20, 4); // Endereço I2C pode ser 0x27 ou 0x3F

// DHT Config
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// Relay, LDR e Botões
#define RELAY_PIN 5
#define LDR_PIN 34
#define BUTTON_P 13
#define BUTTON_K 12

// Nutrientes e irrigação
bool fosforoPresente = false;
bool potassioPresente = false;
bool irrigationOn = false;

// Buffer para manipulação de strings
char info[128]; // (otimizado para char para manipular strings, evitando fragmentação de heap)

void setup() {
  // Inicializando comunicação Serial
  Serial.begin(115200);

  // Configurando o barramento I2C com os pinos SDA e SCL para o RTC
  Wire.begin(SDA_PIN, SCL_PIN);

  // Inicializando o RTC
  if (!ds1307_rtc.begin()) {
    Serial.println("RTC nao encontrado!");
    while (1);
  }
  ds1307_rtc.adjust(DateTime(__DATE__, __TIME__)); // Configura a hora atual com base no compilador

  // Inicializando o DHT
  dht.begin();

  // Configurando os pinos como entrada ou saída
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(BUTTON_P, INPUT_PULLUP);
  pinMode(BUTTON_K, INPUT_PULLUP);

  // Inicializando o LCD
  lcd.begin(20, 4);
  lcd.backlight();

  // Mensagem de boas-vindas
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
  // Leitura de sensores
  float h = dht.readHumidity(); // Leitura de umidade
  float t = dht.readTemperature(); // Leitura de temperatura
  uint16_t ldrValue = analogRead(LDR_PIN); // Leitura do sensor LDR (otimizado para uint16_t)
  uint8_t ph = map(ldrValue, 0, 4095, 0, 14); // Conversão do valor para pH (otimizado para uint8_t)

  // Leitura dos botões
  fosforoPresente = !digitalRead(BUTTON_P);
  potassioPresente = !digitalRead(BUTTON_K);

  // Obtendo a data e hora atual
  DateTime now = ds1307_rtc.now();

  // Lógica de irrigação
  if (h < 30.0f) {
    irrigationOn = true;
    digitalWrite(RELAY_PIN, HIGH);
  } else if (h > 40.0f) {
    irrigationOn = false;
    digitalWrite(RELAY_PIN, LOW);
  }

  // Atualizando o LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.printf("T: %.1fC U: %.1f%%", t, h); // Usando printf para strings formatadas
  lcd.setCursor(0, 1);
  lcd.printf("pH: %d", ph);
  lcd.setCursor(0, 2);
  lcd.printf("P: %s K: %s", fosforoPresente ? "Sim" : "Nao", potassioPresente ? "Sim" : "Nao");
  lcd.setCursor(0, 3);
  lcd.printf("Irrigacao: %s", irrigationOn ? "ON" : "OFF");

  // Montando a string para Serial (substitui String por snprintf para manipular strings, evitando fragmentação de heap.)
  snprintf(info, sizeof(info), "%04d/%02d/%02d %02d:%02d:%02d;%.1f;%.1f;%d;%d;%d;%d", 
           now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second(), 
           t, h, ph, fosforoPresente, potassioPresente, irrigationOn);

  // Enviando para Serial
  Serial.println(info);

  delay(500); // Delay de 500 ms
}
