float temperatura, humedad, valorhum, valortemp, luminosidad, valorlum;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
Serial.println("Comunicacion establecida");
}

void loop() {
  if(Serial.available()){
    switch(Serial.read()){
      case 49:  //1
        for(int i =0; i<25; i++){
        temperatura = analogRead(1);
        valortemp += (5.0*temperatura*100.0/1024.0);
        }
        valortemp = valortemp/25;
        Serial.println(valortemp);//Temperatura
        break;
      case 50:  //2
        humedad = analogRead(0);
        //valorhum = (100-((humedad/10.23)));
        valorhum = ((1024-humedad)/674)*100;
        if (valorhum >= 100)
        valorhum = 100;
        //Serial.println(humedad);
        Serial.println(valorhum);//Humedad
        break;
      case 51:
        luminosidad = analogRead(2);
        valorlum = ((1024-luminosidad)/342)*100;
        if (valorlum >= 100)
        valorlum = 100;
        Serial.println(valorlum);//Luminosidad
        break;
    }
    delay(100);
    Serial.read();
  }
}
