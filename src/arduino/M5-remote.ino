#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <M5Stack.h>

extern const char* ssid;
extern const char* pass;
extern const char* host;

const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument doc(capacity);

int encoder_increment;
int encoder_value=0;
uint8_t direction;
uint8_t last_button,cur_button;

void GetValue(void)
{
  int temp_encoder_increment;
  Wire.requestFrom(0x5E, 3);
  if(Wire.available()){
     temp_encoder_increment = Wire.read();
     cur_button = !Wire.read();
  }
  if(temp_encoder_increment > 127){//anti-clockwise
      direction = 1;
      encoder_increment = 256 - temp_encoder_increment;
  }
  else{
      direction = 0;
      encoder_increment = temp_encoder_increment;
  }
  M5.update();
}

void setLed(char i, char r,char g,char b)
{
  Wire.beginTransmission(0x5E);
  Wire.write(i);
  Wire.write(r);
  Wire.write(g);
  Wire.write(b);
  Wire.endTransmission();
}

void setAllLed(uint16_t d,uint8_t r,uint8_t g,uint8_t b)
{
  for(int i=0;i<12;i++){
    setLed(i,r,g,b);
    delay(d);
  }
}

void ledLOOP()
{
  static uint8_t r = 0;
  static uint8_t g = 127;
  static uint8_t b = 255;

  for(int i=0;i<12;i++){
    setLed(i,r,g,b);
    delay(35);
    setLed(i,0,0,0);
    delay(5);
    r += 16;
    g += 16;
    b += 16;
  }
}

void POSTjson()
{
  char buffer[255];
  HTTPClient client;
  setAllLed(30,0,0xFF,0xFF);
  doc["mode"] = 1;
  doc["type"] = "local";
  doc["dest"] = "utsunomiya-o";
  doc["dest2"] = "ssl-ju";

  serializeJson(doc,buffer,sizeof(buffer));

  client.begin(host);
  client.addHeader("Content-Type","text/plain");
  int status_code = client.POST((uint8_t*)buffer, strlen(buffer));
  
  
  if (status_code == HTTP_CODE_OK){
    setAllLed(30,0,0xFF,0);
  }
  else{
    M5.Lcd.printf("ERROR:%s\n", client.errorToString(status_code).c_str());
    setAllLed(30,0xFF,0,0); 
    delay(700);
  }
  client.end();
  setAllLed(30,0,0,0);
}

void setup()
{
  dacWrite(25,0); //ノイズ対策
  Serial.begin(921600);
  M5.begin();
  Wire.begin();
  M5.Lcd.setTextSize(2);
  M5.Lcd.setTextColor(TFT_GREENYELLOW);
  M5.Lcd.printf("Connecting to AP...\n");
  
  WiFi.begin(ssid,pass);    
  
  do {
    ledLOOP();
  } while(WiFi.status() != WL_CONNECTED);
  M5.Lcd.printf("Connected\n");
}

void loop()
{  
  GetValue();
  if(!last_button && cur_button) POSTjson();
  last_button = cur_button;
  if(M5.BtnA.wasPressed()) {M5.Lcd.fillScreen(TFT_BLACK); M5.Lcd.setCursor(0,0);}
}
