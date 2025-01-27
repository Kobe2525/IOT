# Start eerst de daemon: "sudo pigpiod" in terminal
# Om programma te starten: sudo python3 GIP_Kobe.py
import RPi.GPIO as GPIO
import spidev

from time import sleep, time, strftime, gmtime
import json
import sys
from os import system
import multiprocessing as mp
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

from mfrc522 import SimpleMFRC522


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)




Joysticks = {
	"X1": 5000,
	"X1MIN": 1710,
	"X1MAX": 1760,
	"X1speed": 0,

	"Y1": 5000,
	"Y1MIN": 1790,
	"Y1MAX": 1820,
	"Y1speed": 0,

	"X2": 5000,
	"X2MIN": 1780,
	"X2MAX": 1810,
	"X2speed": 0,

	"Y2": 5000,
	"Y2MIN": 1820,
	"Y2MAX": 1850,
	"Y2speed": 0,

	"servo_pinnen": [27, 22, 5, 6, 13, 26],
	"servo_channels": [None, None, None, None, None, None],					# Lijst van servo stuurkanalen (moeten nog aangemaakt worden)
	"min_hoek": [140, 0, 117, 47, 47, 75],
	"max_hoek": [210, 23, 187, 140, 140, 115],
	"hoeken": [180, 23, 187, 93, 93, 75],
	"prev_hoek": [180, 23, 187, 93, 93, 75]									# Worden veranderd bij het initialiseren van de servo's
}

PUL = 23			# PUL voor te laten draaien
DIR = 24			# DIR voor de richting
KALIBR = 20			# KALIBR voor de kalibratie

LASERREC = 25		# IR-sensor

GPIO.setup(PUL,GPIO.OUT)										# GPIO 23 = OUTPUT PUL
GPIO.setup(DIR,GPIO.OUT)										# DIR
GPIO.setup(KALIBR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)			# Kalibratie

GPIO.setup(LASERREC, GPIO.IN)

factory = PiGPIOFactory()

MIN_RANGE = 0.6			# 0.6ms => 0° = min hoek
MAX_RANGE = 2.4			# 2.4ms => 210° = max hoek

for x in range(6):
	Joysticks["servo_channels"][x] = AngularServo(Joysticks["servo_pinnen"][x], min_angle=Joysticks["min_hoek"][x], max_angle=Joysticks["max_hoek"][x], initial_angle=None, min_pulse_width=((Joysticks["min_hoek"][x]/116)+MIN_RANGE)/1000, max_pulse_width=((Joysticks["max_hoek"][x]/116)+MIN_RANGE)/1000, frame_width=20/1000, pin_factory=factory)
	
	if x+1 == 2 or x+1 == 6:						# start met de juiste starthoek
		Joysticks['prev_hoek'][x] = Joysticks['hoeken'][x]

		Joysticks["servo_channels"][x].angle = Joysticks['prev_hoek'][x]
		print("Hoek servo " + str(x+1) + ": " + str(round(Joysticks['prev_hoek'][x],2)) + "°")
	else:						# start met de juiste starthoek
		Joysticks['prev_hoek'][x] = Joysticks['min_hoek'][x] + Joysticks['max_hoek'][x] - Joysticks['hoeken'][x]

		Joysticks["servo_channels"][x].angle = Joysticks['prev_hoek'][x]
		print("Hoek servo " + str(x+1) + ": " + str(round(Joysticks['prev_hoek'][x],2)) + "°")

MAXSPEED = 0.02							# Maximale snelheid van servo's toegestaan

data = '{ }'

queue_js1 = mp.Queue()
queue_js2 = mp.Queue()
queue_Re = mp.Queue()
queue_DK = mp.Queue()

pixel_pin = board.D12                   # LEDstrip pin = 12
num_pixels = 47                         # Aantal LED's
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
	pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

conn = pymysql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', user='<Gebruikersnaam hier>', passwd='<Wachtwoord hier>', db='GIP')
cur = conn.cursor()

# Tabel van de database leegmaken
cur.execute("TRUNCATE TABLE RFID")

reader = SimpleMFRC522()

def Ontvangen():
	global data_js1
	global data_js2
	global data_Re
	global data_DK
	global data

	

	# Convert received message to string
	string = "".join(chr(i) for i in receivedMessage)

	# Remove characters after end-bracket '}'
	string = string.split('}', 1)[0] + '}'

	# Try parsing the received string as JSON
	try:
		if 'js1X' in string:
			data_js1 = json.loads(string)
			#print("Received: " + str(data_js1))
			queue_js1.put(data_js1)
		elif 'js2X' in string:
			data_js2 = json.loads(string)
			#print("Received: " + str(data_js2))
			queue_js2.put(data_js2)
		elif 'Re' in string:
			data_Re = json.loads(string)
			#print("Received: " + str(data_Re))
			queue_Re.put(data_Re)
		elif 'p1' in string:
			data_DK = json.loads(string)
			#print("Received: " + str(data_DK))
			queue_DK.put(data_DK)
		else:
			data = json.loads(string)
			print("No key recognised: Received: " + str(data))
	except ValueError as e:
		print("Invalid JSON received: ")
		print(string)
		print(e)

def stappenmotor():
	try:
		direction = 1
		positieNU = 0
		positielaatst = 0
		verandering = 0

		data_Re = '{ }'

		while True:
			if not queue_Re.empty():
				data_Re = queue_Re.get_nowait()
			if 'Re' in data_Re:
				positie = data_Re['Re'] * 5		# 17 standen van RE = 85 posities
				if positielaatst != positie:
					verandering = positieNU - positie
					if verandering < 0:
						direction = 1
					elif verandering > 0:
						direction = 0
					else:
						print("Het platform zal niet verplaatsen")
					positielaatst = positie
					sleep(0.01)
				GPIO.output(DIR,direction)

				while abs(verandering) > 0:			# aantal omwentelingen
					for i in range (1,400):					# microstep 125: 25000 pulsen van 0.0144° ==> standaard: 1.8° * 200 = 360°
						GPIO.output(PUL,1)
						sleep(0.0004)						# 0.2us = T ==> 0.2us * 25000 = 0.005s (*2 = 0.01s)
						GPIO.output(PUL,0)
						sleep(0.0004)

					if direction == 1:
						positieNU = positieNU + 1
					else:
						positieNU = positieNU - 1

					verandering = positieNU - positie
					print ("positie nu: " + str(positieNU))
					print ("verandering: " + str(abs(verandering)))

					if not queue_Re.empty():
						data_Re = queue_Re.get_nowait()
						positie = data_Re['Re'] * 5		# 17 standen van RE = 85 posities
					if positielaatst != positie:
						verandering = positieNU - positie
						if verandering < 0:
							direction = 1
						elif verandering > 0:
							direction = 0
						else:
							print("Het platform zal niet verplaatsen")
						positielaatst = positie
						sleep(0.01)
					GPIO.output(DIR,direction)

	except KeyboardInterrupt:
		print("\n'ctrl + C' except: stappenmotor\n")
		GPIO.remove_event_detect(KALIBR)
		GPIO.remove_event_detect(LASERREC)
		GPIO.cleanup()
	except:
		print("\n'Error' except: stappenmotor\n")
		GPIO.remove_event_detect(KALIBR)
		GPIO.remove_event_detect(LASERREC)
		GPIO.cleanup()

def robotarm(RFID_access):
	data_js1 = '{ }'
	data_js2 = '{ }'
	data_DK = '{ }'
	DKstate = 1					# 0 wanneer ingedrukt
	GPstate = 0					# 0 = grijper open, 1 = grijper gesloten
	time_last_change = 0
	hit = 0
	prev_hit = 0
	prev_ineff_hit = 0
	cooldown = False
	GROEN = (0, 255, 0)
	ROOD = (255, 0, 0)
	BLAUW = (0, 0, 255)
	ZWART = (0, 0, 0)
	kleur_nu = GROEN
	kleur_set = False
	stap = 0
	scan = False
	access = False

	try:
		while True:
			if time()-prev_hit >= 10 and hit != 0:					# Einde geïnverteerde sturing
				hit = 0
				cooldown = True
				kleur_nu = BLAUW
				kleur_set = False
			elif time()-prev_hit >= 15 and cooldown:			# Einde afkoelperiode
				cooldown = False
				kleur_nu = GROEN
				kleur_set = False

			if GPIO.input(LASERREC) and 1 < time()-prev_hit <= 15 and time()-prev_ineff_hit > 1:
				prev_ineff_hit = time()
				print("niet effectief geraarkt")
			elif GPIO.input(LASERREC) and time()-prev_hit > 15:
				hit = 1
				prev_hit = time()
				print("effectief geraarkt")
				kleur_nu = ROOD
				kleur_set = False

			if RFID_access.value != 0:
				prev_scan = time()
				scan = True
				pixels.fill(ZWART)
				pixels.show()

				if RFID_access.value == 1:
					access = True
				elif RFID_access.value == 2:
					access = False
				
				RFID_access.value = 0

			if not scan and not kleur_set:
				print("kleur nu")
				pixels.fill(kleur_nu)
				pixels.show()
				kleur_set = True

			if scan and 0.5 < time()-prev_scan <= 1 and stap != 1:
				if access:
					pixels.fill(GROEN)
				else:
					pixels.fill(ROOD)
				pixels.show()
				stap = 1
			elif scan and 1 < time()-prev_scan <= 1.5 and stap != 2:
				pixels.fill(ZWART)
				pixels.show()
				stap = 2
			elif scan and time()-prev_scan > 1.5:
				pixels.fill(kleur_nu)
				pixels.show()
				scan = False

			if not queue_js1.empty():
				data_js1 = queue_js1.get_nowait()
				if 'js1X' in data_js1 and 'js1Y' in data_js1:
					if (Joysticks['X1'] != data_js1['js1X']) or (Joysticks['Y1'] != data_js1['js1Y']):
						Joysticks['X1'] = data_js1['js1X']
						Joysticks['Y1'] = data_js1['js1Y']

						Joysticks['X1speed'] = Joystickwaardes('X',Joysticks['X1'],Joysticks['X1MIN'],Joysticks['X1MAX'],hit)
						Joysticks['Y1speed'] = Joystickwaardes('Y',Joysticks['Y1'],Joysticks['Y1MIN'],Joysticks['Y1MAX'],hit)

						print("X1 = " + str(Joysticks['X1']) + " Y1 = " + str(Joysticks['Y1']))

			if not queue_js2.empty():
				data_js2 = queue_js2.get_nowait()
				if 'js2X' in data_js2 and 'js2Y' in data_js2:
					if (Joysticks['X2'] != data_js2['js2X']) or (Joysticks['Y2'] != data_js2['js2Y']):
						Joysticks['X2'] = data_js2['js2X']
						Joysticks['Y2'] = data_js2['js2Y']

						Joysticks['X2speed'] = Joystickwaardes('X',Joysticks['X2'],Joysticks['X2MIN'],Joysticks['X2MAX'],hit)
						Joysticks['Y2speed'] = Joystickwaardes('Y',Joysticks['Y2'],Joysticks['Y2MIN'],Joysticks['Y2MAX'],hit)

						print("X2 = " + str(Joysticks['X2']) + " Y2 = " + str(Joysticks['Y2']))

			if not queue_DK.empty():
				data_DK = queue_DK.get_nowait()
				if 'p1' in data_DK:
					DKstate = data_DK['p1']
					time_now = time()

					if DKstate == 0 and GPstate == 1 and time_now > time_last_change + 1:
						print("state DK: " + str(DKstate))
						GPstate = 0
						time_last_change = time()

						Joysticks["servo_channels"][5].angle = Joysticks['min_hoek'][5]
						print("Grijper = open")

					elif DKstate == 0 and GPstate == 0 and time_now > time_last_change + 1:
						print("state DK: " + str(DKstate))
						time_last_change = time()
						GPstate = 1

						Joysticks["servo_channels"][5].angle = Joysticks['max_hoek'][5]
						print("Grijper = gesloten")

			if Joysticks['X1speed'] != 0:
				Servosnelheid(Joysticks['X1speed'],1)
			if Joysticks['Y1speed'] != 0:
				Servosnelheid(Joysticks['Y1speed'],2)
				Servosnelheid(Joysticks['Y1speed'],3)
			if Joysticks['X2speed'] != 0:
				Servosnelheid(Joysticks['X2speed'],4)
			if Joysticks['Y2speed'] != 0:
				Servosnelheid(Joysticks['Y2speed'],5)

	except KeyboardInterrupt:
		print("\n'ctrl + C' except: robotarm\n")
		GPIO.remove_event_detect(KALIBR)
		GPIO.remove_event_detect(LASERREC)
		for a in range(6):
			Joysticks["servo_channels"][a].angle = None
		GPIO.cleanup()
	except:
		print("\n'Error' except: robotarm\n")
		GPIO.remove_event_detect(KALIBR)
		GPIO.remove_event_detect(LASERREC)
		for b in range(6):
			Joysticks["servo_channels"][b].angle = None
		GPIO.cleanup()

def Servosnelheid(speed,servo):
	global Joysticks
	global MAXSPEED

	speed = (speed*MAXSPEED)/100
	Joysticks['hoeken'][servo-1] = Joysticks['hoeken'][servo-1] + speed

	if (round(Joysticks['hoeken'][servo-1],2) != round(Joysticks['max_hoek'][servo-1],2)) and (round(Joysticks['hoeken'][servo-1],2) != round(Joysticks['min_hoek'][servo-1],2)):

		if Joysticks['hoeken'][servo-1] > Joysticks['max_hoek'][servo-1]:
			Joysticks['hoeken'][servo-1] = Joysticks['max_hoek'][servo-1]

		elif Joysticks['hoeken'][servo-1] < Joysticks['min_hoek'][servo-1]:
			Joysticks['hoeken'][servo-1] = Joysticks['min_hoek'][servo-1]

		channel = Joysticks['servo_channels'][servo-1]

		if servo != 2:
			if (Joysticks['min_hoek'][servo-1] + Joysticks['max_hoek'][servo-1] - Joysticks['hoeken'][servo-1]) != Joysticks['prev_hoek'][servo-1]:
				Joysticks['prev_hoek'][servo-1] = Joysticks['min_hoek'][servo-1] + Joysticks['max_hoek'][servo-1] - Joysticks['hoeken'][servo-1]

				channel.angle = Joysticks['prev_hoek'][servo-1]
				print("Hoek servo " + str(servo) + ": " + str(round(Joysticks['prev_hoek'][servo-1],2)) + "°")
		else:
			if (Joysticks['hoeken'][servo-1]) != Joysticks['prev_hoek'][servo-1]:
				Joysticks['prev_hoek'][servo-1] = Joysticks['hoeken'][servo-1]

				channel.angle = Joysticks['prev_hoek'][servo-1]
				print("Hoek servo " + str(servo) + ": " + str(round(Joysticks['prev_hoek'][servo-1],2)) + "°")

	#sleep(0.1)

def Joystickwaardes(axis,waarde,MIN,MAX,geraakt):
	global Joysticks
	print("Joystickwaardes")

	MID = (MIN + MAX)/2			 						# Gemiddelde van min en max = middelpunt

	if (axis == 'X' and geraakt == 0) or (axis == 'Y' and geraakt == 1):
		if waarde < MIN:
			snelheid = ((MID - waarde)*100)/MID
		elif waarde > MAX:
			snelheid = ((MID - waarde)*100)/(4095 - MID)
		else:
			snelheid = 0

	elif (axis == 'Y' and geraakt == 0) or (axis == 'X' and geraakt == 1):
		if waarde < MIN:
			snelheid = ((waarde - MID)*100)/MID
		elif waarde > MAX:
			snelheid = ((waarde - MID)*100)/(4095 - MID)
		else:
			snelheid = 0

	print(str(round(snelheid,2)) + "%")
	return snelheid										# Geeft snelheid door in %

def RFID(RFID_access):
	prev_id = 0
	prev_scan = 0

	try:
		while True:
			id, text = reader.read()

			if id != prev_id or time()-prev_scan > 20:
				prev_scan = time()
				prev_id = id

				text = text.strip()                       # Verwijdert spaties vanvoor en vanachter bij een string

				naam = readDB(id)
				if naam:
					print("Naam:",naam)
					insertDB(naam)
					print("Access Granted")
					RFID_access.value = 1
				else:
					print("Geen naam in database")
					print("Access Denied")
					RFID_access.value = 2

				print("Tag ID:", id)
				print("Tag Text:", [text])

				sleep(1.5)

	except KeyboardInterrupt:
		print("\n'ctrl + C' except: RFID\n")
		cur.close()
		conn.close()
		GPIO.cleanup()
	except:
		print("\n'Error' except: RFID\n")
		cur.close()
		conn.close()
		GPIO.cleanup()

def insertDB(naam):
		# INSERT INTO [tabelnaam] (kolom1,kolom2) VALUES (%s,%s) Tijd moet in phpmyadmin datatype "TIMESTAMP" hebben
		cur.execute("INSERT INTO RFID(naam,time) VALUES (%s,%s)",(naam,strftime("%Y-%m-%d %H:%M:%S", gmtime())))
		# %s betekend dat er naar de sql regel gezocht gaat worden voor variabelen die meegestuurd moeten worden
		# voorbeeld met 2 kolommen : cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (42, 'bar'))
		conn.commit()

def readDB(id):
	# Read a single record
	sql = "SELECT `naam` FROM `UID` WHERE `id`=%s"
	cur.execute(sql, (id,))
	result = cur.fetchone()
	if result:
		return result[0]
	else:
		return False

def interruptStartpositie(a):
	global Startpositie							# status startpositie platform
	Startpositie = 1

def Kalibratie():
	global Startpositie

	GPIO.output(PUL,0)							# Stuur LAAG naar GPIO 23
	Startpositie = 0
	direction = 0								# platform beweegt naar motor toe

	GPIO.output(DIR,direction)					# 1 is weg van de motor, 0 is naar de motor
	while Startpositie == 0:					# limit switch is normally closed --> startpositie bereikt wanneer startpositie = 1
		GPIO.output(PUL,1)
		sleep(0.0004)
		GPIO.output(PUL,0)
		sleep(0.0004)

	direction = 1
	GPIO.output(DIR,direction)

	for i in range (1,800):						# platform beweegt naar startpositie, zodat kalibratiepunt niet gelijk is aan het 0-punt
		GPIO.output(PUL,1)
		sleep(0.0004)
		GPIO.output(PUL,0)
		sleep(0.0004)

	print ("gekalibreerd")

stappenmotor_process = mp.Process(target=stappenmotor, args=())
RFID_access = mp.Value('i',0)
robotarm_process = mp.Process(target=robotarm, args=(RFID_access,))
RFID_process = mp.Process(target=RFID, args=(RFID_access,))


try:
	GPIO.add_event_detect(KALIBR, GPIO.FALLING, callback=interruptStartpositie, bouncetime=600)

	print("start kalibratie")
	Kalibratie()
	print("start stappenmotor")
	print("start robotarm")
	print("start RFID")
	stappenmotor_process.start()
	robotarm_process.start()
	RFID_process.start()

	while True:
		if not radio.available(0):
			sleep(0.01)
		else:
			print("radio available")
			Ontvangen()

except KeyboardInterrupt:
	#system('clear')
	print("\n'ctrl + C' except: main\n")
	GPIO.remove_event_detect(KALIBR)
	for y in range(6):
		Joysticks["servo_channels"][y].angle = None
	pixels.fill((0, 0, 0))
	pixels.show()
	sleep(1)
	GPIO.cleanup()
	sys.exit()
except:
	#system('clear')
	print("\n'Error' except: main\n")
	GPIO.remove_event_detect(KALIBR)
	for z in range(6):
		Joysticks["servo_channels"][z].angle = None
	pixels.fill((0, 0, 0))
	pixels.show()
	sleep(1)
	GPIO.cleanup()	
	sys.exit()