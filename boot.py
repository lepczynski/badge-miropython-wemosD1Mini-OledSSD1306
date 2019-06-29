# https://github.com/lepczynski/badge-miropython-wemosD1Mini-OledSSD1306
# Made in 2019 on Earth by Lepi

# boot.py file is executed on every boot (including wake-boot from deepsleep)

# for production:
#import uos
#uos.dupterm(None, 1) # disable REPL on UART(0)

import gc

import time, machine

def do_connect():

    import network
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():

        print('connecting to WiFi network...')

        sta_if.active(True)

        print('loading config_wifi.txt ...')
        config_wifi_carrets = open('config_wifi.txt', 'r').readlines()
        config_wifi = [ x.rstrip() for x in config_wifi_carrets ]

        sta_if.connect(config_wifi[0], config_wifi[1])

        while not sta_if.isconnected():
            pass

    print('WiFi network config:', sta_if.ifconfig())


try:
    do_connect()


except:
    time.sleep(60)
    machine.reset()


import webrepl

print('starting WebREPL...')
webrepl.start()
gc.collect()
