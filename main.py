from neopixel import *
import time
import numpy as np
import threading
from clock import wordclock
import paho.mqtt.client as mqtt
import socket
import argparse
import os


def display(pixelmap):
    for i in range(len(pixelmap)):
        strip.setPixelColorRGB(i, pixelmap[i][1], pixelmap[i][0], pixelmap[i][2]) # G, R, B
    strip.show()

def is_connected():
  try:
    host = socket.gethostbyname("www.google.com")
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False


def update_time():
    hours = time.strftime("%H")
    minutes = time.strftime("%M")
    seconds = time.strftime("%S")

    print(hours + ":" + minutes + ":" + seconds)

    clock_object.set_time(int(hours),int(minutes))
    clock_object.update()
    pixelmap = clock_object.get_pixelmap()
    display(pixelmap)

def thread1():

    minutes_last = "0"

    while True:
        if (is_connected()):
            hours = time.strftime("%H")
            minutes = time.strftime("%M")
            seconds = time.strftime("%S")

            print(hours + ":" + minutes + ":" + seconds)

            if minutes_last != minutes:
                print("update time")

                clock_object.set_time(int(hours),int(minutes))
                clock_object.update()
                pixelmap = clock_object.get_pixelmap()
                display(pixelmap)

            minutes_last = minutes
        else:
            clock_object.no_time_availabe()
            pixelmap = clock_object.get_pixelmap()
            display(pixelmap)


        #print(is_connected())

        client.publish(args.mqtt_topic_get_time, hours + ":" + minutes + ":" + seconds, qos=0, retain=False)

        time.sleep(1.0)




def thread2():
    global client

    while True:

        client.on_connect = on_connect
        client.on_message = on_message

        try_to_connect = True

        while try_to_connect:
            try:
                client.connect(args.mqtt_server_ip, int(args.mqtt_server_port), 60)
                try_to_connect = False
                break
            except Exception as e:
                print(e)



        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()







# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(args.mqtt_topic_set_brightness)
    client.subscribe(args.mqtt_topic_set_mode)
    client.subscribe(args.mqtt_topic_set_color)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " "+ msg.payload.decode("utf-8"))

    if msg.topic == args.mqtt_topic_set_brightness:
        clock_object.set_brightness(float(msg.payload.decode("utf-8")))
        pixelmap = clock_object.get_pixelmap()
        display(pixelmap)

    if msg.topic == args.mqtt_topic_set_mode:
        if msg.payload.decode("utf-8") == "SAME_COLOR" or msg.payload.decode("utf-8") == "WORD_RANDOM_COLOR" or msg.payload.decode("utf-8") == "CHARACTER_RANDOM_COLOR":
            clock_object.set_mode(msg.payload.decode("utf-8"))
            update_time()

        if msg.payload.decode("utf-8") == "TEST":
            clock_object.set_mode("TEST")
            clock_object.set_color((255,0,0))
            clock_object.update()
            pixelmap = clock_object.get_pixelmap()
            display(pixelmap)


    if msg.topic == args.mqtt_topic_set_color:
        color = msg.payload.decode("utf-8")
        if color[0] == "#":
            r = color[1:3]
            g = color[3:5]
            b = color[5:7]
        else:
            r = color[0:2]
            g = color[2:4]
            b = color[4:6]

        r = int(r, 16)
        g = int(g, 16)
        b = int(b, 16)

        clock_object.set_color((r, g, b))
        update_time()


# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mqtt_server_ip", help="")
parser.add_argument("--mqtt_server_port", help="")
parser.add_argument("--mqtt_topic_set_brightness", help="")
parser.add_argument("--mqtt_topic_set_mode", help="")
parser.add_argument("--mqtt_topic_set_color", help="")
parser.add_argument("--mqtt_topic_get_time", help="")
args = parser.parse_args()

# LED strip configuration:
LED_COUNT   = 114      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
strip.begin()


client = mqtt.Client()

clock_object = wordclock()

t1= threading.Thread(target=thread1)
t2= threading.Thread(target=thread2)

t1.start()
t2.start()
