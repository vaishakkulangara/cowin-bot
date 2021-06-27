import requests
import json
import time
import itertools,sys
spinner = itertools.cycle(['#','/','|','\\'])


from twilio.rest import Client
def sendSMS(msg):
	''' Change the value of 'from' with the number 
	received from Twilio and the value of 'to'
	with the number in which you want to send message.'''
	acc_sid = ''	# Your Account Sid and Auth Token from twilio.com / console
	token = ''
	client = Client(acc_sid,token)
	message = client.messages.create(
					from_ ='',
					to = '',
					body = msg )
	print(message.sid)

NO_CENTER_MSG = 'Hi , looks like there are no slots availbale for vaccination\nYou are instantly notified with slot details if available ,\nThank you'
CENTER_AVAILABLE = 'Vaccination Slots Available'
pincode = input('Enter your pincode:')
date = input('Enter required date(DD-MM-YYYY):')
FLAG = False
URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode='+str(pincode)+'&date='+date

start = True
while(1):
	page = requests.get(URL)
	data = json.loads(page.text)
	for d in data['sessions']:
		if(d['available_capacity']>0):
			msg = CENTER_AVAILABLE + ' at ' + d['name'] + '\nFee type : ' + d['fee_type'] + '\nAvailable ' + str(d['available_capacity']) + ' slots' + '\nMinimum Age : ' + str(d['min_age_limit']) + '\nVaccine : ' + d['vaccine']
			sendSMS(msg) 
			print(msg) 
			FLAG = True 
	if(start):	
		print(NO_CENTER_MSG)
		start = False
	if(FLAG):
		break	
	time.sleep(10)
	sys.stdout.write(next(spinner))  
	sys.stdout.flush()   
	sys.stdout.write('\b')             
