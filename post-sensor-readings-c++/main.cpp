#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "<SSID>";                                                             // WIFI SSID
const char* password = "<PASSWORD>";                                                     // WIFI Password

const String X_API_KEY = "<X_API_KEY>";                                                  // API key obtained from Fruitful
const String SYSTEM_ID = "<SYSTEM_ID>";                                                  // System ID (unique identifier of your growth environment)
const String DEVICE_ID = "<DEVICE_ID>";                                                  // Device ID (unique ID of the device streaming data)

String SERVER_NAME = "https://api.fruitful.ag";                                                  // Server name of Fruitful
String SERVER_PATH = "/v1/systems/" + SYSTEM_ID + "/devices/" + DEVICE_ID + "/data";     // Endpoint for sensor readings

const int MIN_INTERVAL_IN_MINUTES = 5;                                                   // Minutes between each HTTP POST request
const int _MIN_INTERVAL = MIN_INTERVAL_IN_MINUTES * 60000;                        

unsigned long _previous_millis = 0; 

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.print("Posting reading every: ");
  Serial.print(MIN_INTERVAL_IN_MINUTES);
  Serial.print(" ");
  Serial.println("minutes...");
  delay(2000);
}

void post_reading()
{
  ///////////////////////////////////////////
  //#########################################
  //######## INSERT READINGS HERE ###########
  
  DynamicJsonDocument doc(2048);
  doc["air_temp"] = 42.0;         // make sure values are numeric
  doc["air_co2"] = 42.0;          // make sure values are numeric
  doc["air_humidity"] = 42.0;     // make sure values are numeric
  doc["water_ec"] = 42.0;         // make sure values are numeric
  doc["water_temp"] = 42.0;       // make sure values are numeric
  // Add additional metrics if needed
  
  //#########################################
  //#########################################
  ///////////////////////////////////////////

  String json;
  serializeJson(doc, json);
  
  WiFiClientSecure client;
  
  // NB! Remove this and configure certificates 
  client.setInsecure();

  HTTPClient http;

  // Initialise connection
  http.begin(client, SERVER_NAME + SERVER_PATH);

  // Set content and auth header
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-KEY", X_API_KEY);

  // Make request
  http.POST(json);

  // Read response
  Serial.print(http.getString());
  
  // Disconnect
  http.end();
}

void loop()
{
  unsigned long current_millis = millis();
  if (current_millis - _previous_millis >= _MIN_INTERVAL)
  {
    post_reading();
    _previous_millis = current_millis;
  }
}
