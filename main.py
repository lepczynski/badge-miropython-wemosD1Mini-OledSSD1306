# https://github.com/lepczynski/badge-miropython-wemosD1Mini-OledSSD1306
# Made in 2019 on Earth by Lepi

import machine, ssd1306

PIN_CLOCK = 4
PIN_DATA  = 5


WIDTH  = 128
HEIGHT =  32
W = WIDTH -1
H = HEIGHT -1
# the font is 8x8 plus one pixel space gives us 9x9
half_char_width = WIDTH / 18

i2c  = machine.I2C( scl=machine.Pin(PIN_CLOCK), sda=machine.Pin(PIN_DATA) )
oled = ssd1306.SSD1306_I2C( WIDTH, HEIGHT, i2c, 0x3c )


corners_interval_on  =  128
corners_interval_off = 2048 - corners_interval_on

ants_loop_length_ms = 1000

performance_interval_on  =  600
performance_interval_off = 1365.3333 - performance_interval_on




class BusinessCard( object ):

    def __init__( self, delay=5 ):
        self.delay   = delay
        self.bc_text = []
        self.bc_off  = []

        self.loadBusinessCard()
        self.drawBusinessCard()


    def loadBusinessCard( self, filename='properties.business.card.txt' ):
        print('loading business card from a config file...')
        
        try:
            self.bc_text = [ x.rstrip() for x in open(filename, 'r').readlines() ]
        except:
            print('failed to read business card config, loading defaults...')
            self.bc_text = ['Name', 'Surname', '-------', 'Hello ;)']
        finally:
            print('business card text: ', self.bc_text)

        self.calculateBusinessCardIndents()


    def calculateBusinessCardIndents( self ):
        import math as m

        print('Calculating business card indents from bc_text: ', self.bc_text)

        self.bc_off = [ len(x) for x in self.bc_text ]
        print('business card item lengths: ', self.bc_off)
        
        self.bc_off = [ m.floor( 8 -(x/2) ) for x in self.bc_off]
        print('business card item offsets in number of chars: ', self.bc_off)
        
        #transforms the list of indent numbers for center allignment into space string of such lengths
        self.bc_off = [ ( "".join(map(str, [ " " for i in range(x) ] )) ) for x in self.bc_off ]
        print('business card item offsets in space strings: ', self.bc_off)


    def drawBusinessCard( self ):
        # toDo: devise a better idea than wiping it all out
        # and maybe draw text in a 1x1 pixel cross pattern in black first
        # oled.fill(0)

        oled.text( self.bc_off[2] + self.bc_text[2], 0, 17 )
        oled.text( self.bc_off[0] + self.bc_text[0], 0,  0 )
        oled.text( self.bc_off[1] + self.bc_text[1], 0,  9 )
        oled.text( self.bc_off[3] + self.bc_text[3], 4, 24 )


    def drawCorners( self, color=1, length=3 ): #length and color
        oled.hline( 0        , 0        ,length,color)  #  F  yest
        oled.vline( 0        , 0        ,length,color)

        oled.hline( W-length , 0        ,length,color)  #  7
        oled.vline( W        , 0        ,length,color)

        oled.hline( W-length , H        ,length,color)  #  _|
        oled.vline( W        , H-length ,length,color)

        oled.hline( 0        , H        ,length,color)  #  length  yest
        oled.vline( 0        , H-length ,length,color)

    def drawAnts( self, color=1, length=2, space=3 ):
        olded.pixel


    def loop( self ):
        import utime
        import math as m
        performance_last = corners_last = ants_loop = utime.ticks_ms()
        performance_time4on = corners_time4on = False

        then = now = now = utime.ticks_ms()

        while True:
            then = now
            now = utime.ticks_ms()
            try:
                fps = m.floor( 1000/ utime.ticks_diff(now, then) )
            except:
                fps = 0

            ants = m.floor( utime.ticks_diff(now, ants_loop) / ants_loop_length_ms * 100 ) / 100

            
            oled.fill(0)


            if utime.ticks_diff( now, corners_last ) > corners_interval_off and not corners_time4on:
                self.drawCorners(1)
                corners_time4on = True

            if utime.ticks_diff( now, corners_last ) > corners_interval_off + corners_interval_on:
                corners_last = now
                corners_time4on = False


            if utime.ticks_diff(now, ants_loop) > ants_loop_length_ms:
                ants_loop = now

            self.drawBusinessCard()


            if utime.ticks_diff( now, performance_last) > performance_interval_off and not performance_time4on:

                print('FPS = ', str(fps), ' ants = ', str(ants))
                
                oled.fill_rect(0, 0, 9*4, 9, 0)
                oled.text('F.' + str(fps), 0, 0, 1)
                
                oled.fill_rect(0, 24, 9*6, 9, 0)
                oled.text('a.' + str(ants), 0, 24, 1)
                performance_last = now

                performance_time4on = True

            if utime.ticks_diff( now, performance_last) > performance_interval_off + corners_interval_off:
                performance_last = now
                performance_time4on = False


            oled.show()


if __name__ == '__main__':
    BusinessCard().loop()
