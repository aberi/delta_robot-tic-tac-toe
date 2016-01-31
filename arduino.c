#include <Servo.h> 
#include <stdlib.h>
Servo myservofront;  // create servo object to control a servo 
Servo myservoright;
Servo myservoleft;

float cx = 0, cy = 0, cz = 271; // current x, y, and z coordinates
int ticker = 0;
int s = 50;
int boardheight = 269;//269
int lastRead = 0;
int reading;
int oteam=1;

void setup(){ 
  myservofront.attach(3);  // attaches the servo on pin 9 to the servo object 
  myservoleft.attach(5);
  myservoright.attach(6);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  Serial.begin(9600);
  establishContact();
  moveTo(cx, cy, cz);
  digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  drawBoard();
} 

void setLevers(float f, float l, float r){ //f is front, l is left, r is right
  if (f > 150 || l > 150 || r > 150 || f < 15 || l < 15 || r < 15){
    Serial.println("inputs are out of range for lever arms");
    return; // this checks for invalid inputs
  }
  // TODO: create another indicator that the inputs are invalid
  int fcor = 275; int rcor = 350; int lcor = 375; //fcor = front correction
  long upperLimit = 800; // upper limit ~= 800 = 125 degrees to straight down (((1900)))
  long lowerLimit = 2300;// lower limit ~= 2300 = 35 degrees to straight down (((925 )))
  myservofront.writeMicroseconds((f - 35)*(upperLimit - lowerLimit)/(125-35) + fcor + lowerLimit); // tell servo to go to position in variable 'pos' 
  myservoright.writeMicroseconds((r - 35)*(upperLimit - lowerLimit)/(125-35) + rcor + lowerLimit);
  myservoleft.writeMicroseconds((l - 35)*(upperLimit - lowerLimit)/(125-35) + lcor + lowerLimit);
}

float leverCalc(float x, float y, float z){
  float p0 = 75, p1 = 150, p2 = 315, p3 = 50, mp2, h, theta; // refer to picture < picture of linkages > for explanations of names. all units in mm
  mp2 = sqrt( pow(p2,2) - pow(x,2) ); // adjusts the linkage length to compensate for the tilt of the linkages
  y = y + p3 - p0;  // p0 is the distance from the base of the lever arm to the center of the lever arms
                    // p3 is the distance from the center of the tooltip to the bottom ends of the linkages
                    // This whole adjustment makes y (the change in y) the y distance from the base of the levers to the ends of the linkages
  h = sqrt( pow(y,2) + pow(z,2) ); // calculates h. Refer to < picture of linkages > 
  theta = atan( y / z ) + acos( ( pow(h,2) + pow(p1,2) - pow(mp2,2) ) / (2*h*p1) );
  theta = theta / PI * 180; // adjust theta to match setLever() parameters
  //analogWrite(8, 128 + sin(millis()/1000)*128);
  //analogWrite(9, 128 - sin(millis()/1000)*128);
  return theta;
}

void moveTo(float x, float y, float z){
  float front, right, left, p2 = 315; // these are the variables for the lever angles
  front = leverCalc(x, y, z); //calculates lever angle for the front lever
  float ry = -y*sin(PI/6) + x*cos(PI/6); // adjust x, y, and z values for the left lever
  float rx = -y*cos(PI/6) - x*sin(PI/6);
  right = leverCalc(rx, ry, z); //calculates lever angle for the left lever
  float ly = -y*sin(PI/6) - x*cos(PI/6); // adjust x, y, and z values for the right lever
  float lx = y*cos(PI/6) - x*sin(PI/6);
  left  = leverCalc(lx, ly, z); //calculates lever angle for the right lever
  // Throws error and prevents movement if the input is out of bounds of the mechanism
  if ( atan(x/p2) > PI/6 || atan(rx/p2) > PI/6 || atan(lx/p2) > PI/6 ){ 
    Serial.println("out of bounds of the ball bearings");
    return;
  }
  setLevers(front, left, right); // sets levers to desired angles
  cx = x; cy = y; cz = z;
}

void lineTo(float x, float y, float z, int i, int timeOfInterval){ // i = intervals (determines the precision of the movement)
  float px = cx, py = cy, pz = cz; // px, py, and pz are the initial values of x, y, and z. **note: moveTo() updates cx, cy, and cz
  long pastTimestamp = millis(); //
  for (float j = 1; j <= i; j++){
    moveTo( px + ( j * (x - px) / i), py + ( j * (y - py) / i), pz + ( j * (z - pz) / i) );
    while(millis() - timeOfInterval < pastTimestamp){ // changed from <= to try to make interval timing more accurate
      delay(1);
    }
    pastTimestamp = millis();
  }
  cx = x; cy = y; cz = z;
}

void drawBoard(){
  int z = boardheight;
  //int s = 50; // size of board in mm
  int interval = 100; int lilint = 50; int floatinterval = 50;//movement interval, little movement interval
  
  lineTo(0   ,0   ,z-80,interval,7);
  lineTo(-s/3,s   ,z-20,interval,7);
  lineTo(-s/3,s   ,z   ,lilint,7);
  lineTo(-s/3,-s  ,z   ,interval,7);
  lineTo(-s/3,-s  ,z-20,lilint,7);
  lineTo(s/3 ,-s  ,z-20,floatinterval,7);
  lineTo(s/3 ,-s  ,z   ,lilint,7);
  lineTo(s/3 ,s   ,z   ,interval,7);
  lineTo(s/3 ,s   ,z-20,lilint,7);
  lineTo( s  ,s/3 ,z-20,floatinterval,7);
  lineTo( s  ,s/3 ,z   ,lilint,7);
  lineTo(-s  ,s/3 ,z   ,interval,7);
  lineTo(-s  ,s/3 ,z-20,lilint,7);
  lineTo(-s  ,-s/3,z-20,floatinterval,7);
  lineTo(-s  ,-s/3,z   ,lilint,7);
  lineTo( s  ,-s/3,z   ,interval,7);
  lineTo( s  ,-s/3,z-20,lilint,7);/*
  lineTo( s  ,-s  ,z-20,floatinterval,7);
  lineTo( s  ,-s  ,z   ,lilint,7);
  lineTo( s  , s  ,z   ,interval,7);
  delay(100);
  lineTo(-s  , s  ,z   ,interval,7);
  delay(100);
  lineTo(-s  ,-s  ,z   ,interval,7);
  delay(100);
  lineTo( s  ,-s  ,z   ,interval,7);
  delay(100);
  lineTo(-s  ,-s  ,z-20,lilint,7);*/
  lineTo(0   ,50  ,z-80,interval,7);
}

void drawMove(int x, int y, int width, int XorO){
  if (XorO==1){ // draws the X
    lineTo(x+width/2, y+width/2, boardheight - 20, 70, 7);
    lineTo(x+width/2, y+width/2, boardheight, 50, 7);
    lineTo(x-width/2, y-width/2, boardheight, 70, 7);
    delay(100);
    lineTo(x-width/2, y-width/2, boardheight - 20, 50, 7);
    lineTo(x-width/2, y+width/2, boardheight - 20, 50, 7);
    lineTo(x-width/2, y+width/2, boardheight, 50, 7);
    lineTo(x+width/2, y-width/2, boardheight, 70, 7);
    lineTo(x+width/2, y-width/2, boardheight - 20, 50, 7);
    lineTo(0   ,50  ,boardheight-70,100,7);
  } else { // draws the O
    lineTo(x, y+width/2, boardheight - 20, 70, 7);
    lineTo(x, y+width/2, boardheight, 50, 7);
    //millis() = 0;
    long timestamp = millis();
    while ((millis() < timestamp + 1000)||(millis()<100)){
      moveTo(sin((millis()-timestamp)/(1000/PI/2))*(width/2)+x,cos((millis()-timestamp)/(1000/PI/2))*(width/2)+y,boardheight);
    }
    delay(100);
    lineTo(x, y+width/2, boardheight - 20, 50, 7);
    lineTo(0   ,50  ,boardheight-70,100,7);
  }
}

void gameMove(int place, int team){
  int width = 25;
  place = place % 12;
  switch (place) {
  case 1:
    drawMove(-s*2/3, s*2/3, width, team);
    break;
  case 2:
    drawMove( 0    , s*2/3, width, team);
    break;
  case 3:
    drawMove( s*2/3, s*2/3, width, team);
    break;
  case 4:
    drawMove(-s*2/3, 0, width, team);
    break;
  case 5:
    drawMove( 0    , 0, width, team);
    break;
  case 6:
    drawMove( s*2/3, 0, width, team);
    break;
  case 7:
    drawMove(-s*2/3,-s*2/3, width, team);
    break;
  case 8:
    drawMove( 0    ,-s*2/3, width, team);
    break;
  case 9:
    drawMove( s*2/3,-s*2/3, width, team);
    break;
  case 10:
    if (oteam == 1){
      oteam = 0;} else {
      oteam = 1;}
    break;
  case 11:
    drawBoard();
    break;
  default: 
      
    break;
  }//
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');
    delay(100);
  }
}

void loop() {
  if (Serial.available() > 0 && (reading = Serial.read())!=lastRead) {
    gameMove(reading/*-47*/,oteam);
    delay(15);
    lastRead = reading;
    Serial.println(lastRead);
  }
}


