import sys
import Adafruit_DHT
from gpiozero import LED, Button
from time import sleep


import pubnub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

 
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-9c8dd184-c4dc-11eb-9292-4e51a9db8267"
pnconfig.publish_key = "pub-c-a243be10-d60f-4b3c-bc5a-0f49b27783ab"
pnconfig.ssl = False
 
pubnub = PubNub(pnconfig)

pump = LED(4)
sensor = 22
pin = 17
soil = Button(14)

flag = 1

pump.on()

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
               
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
            else:
                pass
            elif status.operation == PNOperationType.PNSubscribeOperation:
            if status.is_error():
                pass
            else:
                pass
        else:
            pass

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def message(self, pubnub, message):
        if message.message == 'ON':
        	global flag
        	flag = 1
        elif message.message == 'OFF':
			global flag
			flag = 0
        elif message.message == 'WATER':
        	pump.off()
        	sleep(5)
        	pump.on()
 
 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('ch1').execute()

def publish_callback(result, status):
	pass

def get_status():
	if soil.is_held:
		print("dry")
		return True
	else:
		print("wet")
		return False


while True:
	if flag ==1:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		DHT_Read = ('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		print(DHT_Read)

		dictionary = {"eon": {"Temperature": temperature, "Humidity": humidity}}
		pubnub.publish().channel('ch2').message([DHT_Read]).async(publish_callback)
		pubnub.publish().channel("eon-chart").message(dictionary).async(publish_callback)

		wet = get_status()
		
		if wet == True:
		    print("turning on")
		    pump.off()
		    sleep(5)
		    print("pump turning off")
		    pump.on()
		    sleep(5)
		else:
		    pump.on()

		sleep(5)
	elif flag == 0:
		pump.on()
		sleep(5)
