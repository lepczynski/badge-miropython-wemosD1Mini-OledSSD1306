# https://github.com/lepczynski/badge-miropython-wemosD1Mini-OledSSD1306
# Made in 2019 on Earth by Lepi

import machine, ssd1306

PIN_CLOCK = 4
PIN_DATA = 5

WIDTH = 128
HEIGHT = 32
# the font is 8x8 plus one pixel space gives us 9x9
half_char_width = WIDTH / 18

corners_interval_on = 2048
corners_interval_off = 128

ants_loop_length_ms = 400

i2c = machine.I2C(scl=machine.Pin(PIN_CLOCK), sda=machine.Pin(PIN_DATA))
oled = ssd1306.SSD1306_I2C(128, 32, i2c, 0x3c)

W = WIDTH -1
H = HEIGHT -1




def loop(delay=5):

    bc_text = [None] # [ 0 for x in range(4) ]
    bc_off = [None]  # [ 0 for x in range(4) ]


    def loadBusinessCard(filename='properties.business.card.txt'):
        print('loading business card from a config file...')
        
        try:
            bc_text = [ x.rstrip() for x in open(filename, 'r').readlines() ]
        except:
            print('failed to read business card config, loading defaults...')
            bc_text = ['Name', 'Surname', '-------', 'Hello ;)']
        finally:
            print('business card text: ', bc_text)

        return bc_text


    def calculateBusinessCardIndents():
        import math as m

        print('Calculating business card indents from bc_text: ', bc_text)

        bc_off = [ len(x) for x in bc_text ]
        print('business card item lengths: ', bc_off)
        
        bc_off = [ m.ceil( 8 -(x/2) ) for x in bc_off]
        print('business card item offsets in number of chars: ', bc_off)
        
        #transforms the list of indent numbers for center allignment into space string of such lengths
        bc_off = [ ( "".join(map(str, [ " " for i in range(x) ] )) ) for x in bc_off ]
        print('business card item offsets in space strings: ', bc_off)


    def drawBusinessCard():
        # toDo: devise a better idea than wiping it all out
        # and maybe draw text in a 1x1 pixel cross pattern in black first
        # oled.fill(0)

        print("bc_off: ", bc_off)
        print("bc_text: ", bc_text)

        oled.text(bc_off[2] + bc_text[2], 0, 17)
        oled.text(bc_off[0] + bc_text[0], 0, 0)
        oled.text(bc_off[1] + bc_text[1], 0, 9)
        oled.text(bc_off[3] + bc_text[3], 4, 24)


    def drawCorners(color=1, length=3): #length and color
        oled.hline( 0        , 0        ,length,color)  #  F  yest
        oled.vline( 0        , 0        ,length,color)

        oled.hline( W-length , 0        ,length,color)  #  7
        oled.vline( W        , 0        ,length,color)

        oled.hline( W-length , H        ,length,color)  #  _|
        oled.vline( W        , H-length ,length,color)

        oled.hline( 0        , H        ,length,color)  #  length  yest
        oled.vline( 0        , H-length ,length,color)

    bc_text = loadBusinessCard()
    
    drawBusinessCard()

    import utime
    i = 0
    corners_last = ants_loop = utime.ticks_ms()
    time4on = False


    while True:
        now = utime.ticks_ms()

        if utime.ticks_diff(now, corners_last) > corners_interval_off and not time4on:
            drawCorners(1)
            time4on = True
        if utime.ticks_diff(now, corners_last) > corners_interval_off + corners_interval_on:
            drawCorners(0)
            drawBusinessCard()
            corners_last = now
            time4on = False

        if utime.ticks_diff(now, ants_loop) > ants_loop_length_ms:
            ants_loop = now

        print(utime.ticks_diff(now, ants_loop))

        drawBusinessCard()
        oled.show()


if __name__ == '__main__':
    loop()
