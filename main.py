import pycom, machine, micropython, time   # Some libraries that we will use
from machine import I2C
import busio, adafruit_mlx90640
import utime
import network
from network import WLAN
from network import Bluetooth
import ujson
import os
from machine import ADC
from machine import RTC
from machine import Timer
import re

wlan = WLAN()
wlan.deinit()

pycom.heartbeat(False)
BLEConnected = False

def is_float(n):
    try:
        float(n)
        return True
    except:
        return False

def extractData(f):
    data = []
    for line in f:
        line = line.strip()
        print(line)
        if len(line) == 0 or line[0].isalpha(): continue
        print(line)
        items = line.split()
        print(items)
        data.append([float(item) for item in items[1:]])
    return data

def deep_sleep(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, msecs)
    machine.deepsleep()

def connectionCallback(e):
    events = e.events()
    global BLEConnected
    if events & Bluetooth.CLIENT_CONNECTED:
        BLEConnected = True
        print("Client připojen")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        BLEConnected = False
        print("Client nepřipojen")


def char1_cb_handler(chr, data):
    events, value = data
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print("Požadavek na zápis")
        pycom.rgbled(int.from_bytes(bytearray(value), 'big'))
    elif events & Bluetooth.CHAR_READ_EVENT:
        print("Požadavek na čtení")
class Clock:

    def __init__(self):
        self.seconds = 0
        self.__alarm = Timer.Alarm(self._seconds_handler, 1, periodic=True)

    def _seconds_handler(self, alarm):
        self.seconds += 1
        if self.seconds == 4:
            print("False")
            pripojeni = False
        if self.seconds == 5:
            alarm.cancel() # stop counting after 5 seconds


apin = ADC().channel(pin='P16')

pycom.heartbeat(False)

time.sleep(2.0)
ixc = busio.I2C(pins=('P9','P10'), frequency=400000) # read on some forum that 400KHz is the highest baudrate that                                              
senzor = adafruit_mlx90640.MLX90640(ixc)
i = 0
j = 0
bl = 0
pocet = 0
prvek1 = 0
pocet2 = 0
pocet3 = 0
tik = 0
posli_data = 0
frame = [0]*768


bt = Bluetooth()
bt.deinit()
spi = True
while True:
    try:
        senzor.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ # 2Hz or higher refresh rates produce 0s for alternate pixels,
        senzor.getFrame(frame)
        #pole = array(frame)
        #print(frame)
        for prvek in frame:
            if (prvek > 27):
                spi = False
        podminka = True
        #rtc.wakeup(20000)
        if (spi == False):
            if (bl == 0):
                with open("/flash/matice.txt", 'w') as file:
                    k=repr(frame)
                    file.write(k)
                    file.close()
                    print("ZAPSANO!!!")
                    bl = bl + 1
                    posli_data = 0
            elif (bl > 0):
                with open("/flash/matice.txt", 'a') as file:
                    #file.write("matice")
                    k=repr(frame)
                    file.write(k)
                    file.close()
                    print("ZAPSANO2!!!")
                    bl = bl + 1
                    posli_data = 0
        if ((posli_data == 3 and bl > 5) or bl == 15):
            bl = 0
            posli_data = 0
            pycom.rgbled(0x00000f)
            pripojeni = True
            bt = Bluetooth()
            bt.init()
            Bluetooth().set_advertisement(
                name='Wipy', service_uuid=12345)

            Bluetooth().callback(trigger=Bluetooth.CLIENT_CONNECTED |
                                Bluetooth.CLIENT_DISCONNECTED, handler=connectionCallback)

            Bluetooth().advertise(True)

            srv = Bluetooth().service(uuid=12345, isprimary=True, nbr_chars=2, start=True)

            char1 = srv.characteristic(uuid=54321, properties=Bluetooth.PROP_INDICATE |
                                    Bluetooth.PROP_BROADCAST | Bluetooth.PROP_NOTIFY, value=ujson.dumps({}))

            char2 = srv.characteristic(uuid=64321, value=0xff00)

            char1_cb = char2.callback(
                trigger=Bluetooth.CHAR_WRITE_EVENT, handler=char1_cb_handler)

            start = time.ticks_ms()
            print(start)
            while (pripojeni):
                if (time.ticks_diff(time.ticks_ms(), start) == 10000):
                    pripojeni = False
                if BLEConnected:
                    print("PRIPOJENO")
                    pripojeni = False
            with open("/flash/matice.txt", 'r') as testf:
                pycom.rgbled(0x000f00)
                dataR = testf.read()
                x1 = dataR.replace("][",", ")
                x1 = x1.replace("[","")
                x1 = x1.replace("]","")
                #print(x1)
                dataList = x1.split(", ")
                for i in range(0, len(dataList), 1):
                    dataList[i] = float(dataList[i])
                    pycom.rgbled(0x000f0f)

            for row in dataList:
                print(row)
                json = ujson.dumps(row)
                utime.sleep(0.02)
                if BLEConnected:
                    char1.value(json)

        bt.deinit()
        matice = []
        matice_W = []
        if (spi):
            posli_data = posli_data + 1
            print("sleep")
            ######### DEEPSLEEP #############
            # rtc = machine.RTC()
            # rtc.init((2017, 6, 12, 14, 35, 20))
            # rtc.now()
            # rtc.synced()
            # machine.deepsleep(10000)


            #deep_sleep(10000)
            # pycom.rgbled(0xff0000)
            # rtc = machine.RTC()
            # rtc.irq(trigger=rtc.ALARM0, wake=machine.deepsleep)
            # rtc.alarm(rtc.ALARM0, 20000)
            # pycom.rgbled(0x00ff00)
            # machine.deepsleep()
            #print("KONEC")

            #machine.lightsleep(4000)
            machine.sleep(4000)
        spi = True

    except Exception as e:
        print(e)
        pycom.rgbled(0xff0000) # Indikace chyby    
