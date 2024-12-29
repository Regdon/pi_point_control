var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO
var LED25 = new Gpio(596, 'out'), //use declare variables for all the GPIO output pins
  LED12 = new Gpio(583, 'out'),
  LED16 = new Gpio(587, 'out'),
  LED20 = new Gpio(591, 'out'),
  LED21 = new Gpio(592, 'out'),
  LED05 = new Gpio(576, 'out'),
  LED06 = new Gpio(577, 'out'),
  LED13 = new Gpio(584, 'out'),
  LED19 = new Gpio(590, 'out'),
  LED26 = new Gpio(597, 'out');

//Put all the LED variables in an array
var leds = [LED26, LED19, LED13, LED06, LED05, LED21, LED20, LED16, LED12, LED25];
var indexCount = 0; //a counter
dir = "up"; //variable for flowing direction

var flowInterval = setInterval(flowingLeds, 100); //run the flowingLeds function every 100ms

function flowingLeds() { //function for flowing Leds
  leds.forEach(function(currentValue) { //for each item in array
    currentValue.writeSync(0); //turn off LED
  });
  if (indexCount == 0) dir = "up"; //set flow direction to "up" if the count reaches zero
  if (indexCount >= leds.length) dir = "down"; //set flow direction to "down" if the count reaches 7
  if (dir == "down") indexCount--; //count downwards if direction is down
  leds[indexCount].writeSync(1); //turn on LED that where array index matches count
  if (dir == "up") indexCount++ //count upwards if direction is up
};

function unexportOnClose() { //function to run when exiting program
  clearInterval(flowInterval); //stop flow interwal
  leds.forEach(function(currentValue) { //for each LED
    currentValue.writeSync(0); //turn off LED
    currentValue.unexport(); //unexport GPIO
  });
};

process.on('SIGINT', unexportOnClose); //function to run when user closes using ctrl+cc