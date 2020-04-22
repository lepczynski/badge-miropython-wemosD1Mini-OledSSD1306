# badge-miropython-wemosD1Mini-OledSSD1306
A fun project in Micro Python for a conference badge (hopefully an interactive badge soon) using Wemos D1 Mini developement board (esp8266) and for now 128x23 OLED I2C display (on SSD1306). Hope to add 2 PIRs : )

Connect Wemos D1 mini's +5V and GND to SSD1306's GND and VCC pins;
connect Wemos's D1 and D2 pins to SSD1306's i2C Data and Clock pins.

To run install esptool, flash micropython onto your board, install AdaFruit ampy and using it put boot.py, main.py, ssd1306.py.

Adjust property files to your needs:
  properties.wifi.txt
  properties.business.card.txt
and ampy them onto the board as well.

Use a serial terminal (screen, picocom, CuteCom or such) and send Ctr+D to soft reboot the board and run.


ToDo:
  add alternative Wifi credentials with priorities so the board can connect to one of a few defined SSID's
  add marching ants animation
  rethink architecture to accomodate growing complexity of animation with readability
    make use of Peter Hinch'es Micropython Async lib ( https://github.com/peterhinch/micropython-async )
    or maybe create a builder or other pattern..
  post some photos somewhere (?)
 
If I can help in anyway, please, drop me a line at:
  lepi a t hackerspace d o t pl

Cheers!
Mike
