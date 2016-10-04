import nexmo
import re

NEXMO_API_KEY = '<add_your_api_key_here>'
NEXMO_API_SECRET = '<add_your_api_secret_here>'
SMS_FROM = 'No Reply'

def validate_phone_number(phone_number):
	checked_phone_number = phone_number.strip()
	checked_phone_number = zero_to_indonesia_country_code(checked_phone_number)
	checked_phone_number = add_indonesia_country_code(checked_phone_number)
	checked_phone_number = validate_indonesia_country_code(checked_phone_number)
	return checked_phone_number

def zero_to_indonesia_country_code(phone_number):
	return re.sub('^0', '+62', phone_number)

def add_indonesia_country_code(phone_number):
	return re.sub('^8', '+628', phone_number)

def validate_indonesia_country_code(phone_number):
	return re.sub('^62', '+62', phone_number)

def check_status(response_message):
	if response_message['status'] == '0':
	  print 'Sent message', response_message['message-id']
	  print 'Remaining balance is', response_message['remaining-balance']
	else:
	  print 'Error:', response_message['error-text']

def send_sms_handler(event, context):
	json_message = eval(event['Records'][0]['Sns']['Message'])
	print(json_message)

	sms_to = validate_phone_number(json_message['SmsTo'])
	text = json_message['Text']

	client = nexmo.Client(key = NEXMO_API_KEY, secret = NEXMO_API_SECRET)
	response = client.send_message(
		{
			'from': SMS_FROM, 
			'to': sms_to, 
			'text': text
		}
	)

	check_status(response['messages'][0])