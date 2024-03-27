from machine import Pin, SPI
import time
import epaper7in5_V2
import framebuf

import network
import utime


import utelegram

import my_secrets

debug = False
global wlan
global mytext
mytext = 'Hello World11111111111111111'

sck = Pin(13)
dc = Pin(27)
cs = Pin(15)
busy = Pin(25)
rst = Pin(26)
mosi = Pin(14)


def start_network():
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface

    # ----------------------------------------------------------------------------
    print('vor sleeep ')
    time.sleep(0)
    print('vor connect ')
    wlan.connect(my_secrets.WIFI_SSID, my_secrets.WIFI_PASSWD)  # connect to an AP
    print('nach connect ')
    time.sleep(5)
    print('nach sleeep ')

    global mytext
    mytext = 'Hello World11111111111111111'
    # ----------------------------------------------------------------------------
    if debug:
        print('WAITING FOR NETWORK - sleep 20')
    utime.sleep(20)


# ----------------------------------------------------------------------------


def eink_screen_ini():
    global mytext

    spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, mosi=mosi)
    e = epaper7in5_V2.EPD(spi, cs, dc, rst, busy)

    print("We're in main")

    w = 800
    h = 480
    x = 0
    y = 0

    e.init()
    print("Screen ready")

    # ----------------------------------------------------------------------------
    # https://docs.micropython.org/en/latest/library/framebuf.html

    buf = bytearray(w * h // 8)
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
    black = 0
    white = 1

    fb.fill(white)
    fb.text(mytext, 30, 0, black)
    e.display_frame(buf)


# ----------------------------------------------------------------------------


def start_telegrambot():
    def get_message(message):
        bot.send(message['message']['chat']['id'],
                 message['message']['text'].upper())

    def reply_ping(message):
        global mytext
        print(message)
        bot.send(message['message']['chat']['id'], mytext)
        mytext = "new Text"
        eink_screen_ini()

    # ----------------------------------------------------------------------
    # if wlan.isconnected():
    bot = utelegram.ubot(my_secrets.TELEGRAM_API)
    bot.register('/ping', reply_ping)
    bot.set_default_handler(get_message)

    print('BOT LISTENING')
    bot.listen()
    # else:
    # print('NOT CONNECTED - aborting')


start_network()
print('CONNECTED')
eink_screen_ini()
print('Screen ready')
start_telegrambot()
