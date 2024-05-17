#define cav1 2
#define cav2 3
#define cav3 4
#define cav4 5
#define cav5 6
#define cav6 7
#define cav7 8
#define cav8 9
#define cav9 10
#define cav10 11
#define cav11 12
#define cav12 13

int cavPins[12] = {cav1, cav2, cav3, cav4, cav5, cav6, cav7, cav8, cav9, cav10, cav11, cav12};

void setup() {
  Serial.begin(9600);  // Set baud rate to match the Python code
  pinMode(cav1, OUTPUT);
  pinMode(cav2, OUTPUT);
  pinMode(cav3, OUTPUT);
  pinMode(cav4, OUTPUT);
  pinMode(cav5, OUTPUT);
  pinMode(cav6, OUTPUT);
  pinMode(cav7, OUTPUT);
  pinMode(cav8, OUTPUT);
  pinMode(cav9, OUTPUT);
  pinMode(cav10, OUTPUT);
  pinMode(cav11, OUTPUT);
  pinMode(cav12, OUTPUT);

  
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();  // Remove any trailing newline characters

    // Make a copy of the string data to use with strtok
    char dataArray[50];  // Adjust size as needed
    data.toCharArray(dataArray, 50);

    // Split the string into an array
    float values[6];
    int index = 0;
    char* token = strtok(dataArray, ",");
    while (token != NULL && index < 6) {
      values[index] = atof(token);
      token = strtok(NULL, ",");
      index++;
    }
    

    for (int i = 0; i < 6; i++) {
      if (values[i] == 0) {
        digitalWrite(cavPins[i * 2], HIGH);
        digitalWrite(cavPins[i * 2 + 1], HIGH);
      } else if (values[i] == 1) {
        digitalWrite(cavPins[i * 2], HIGH);
        digitalWrite(cavPins[i * 2 + 1], LOW);
      } else if (values[i] == 2) {
        digitalWrite(cavPins[i * 2], LOW);
        digitalWrite(cavPins[i * 2 + 1], HIGH);
      }
    }

    
    
  }
}
