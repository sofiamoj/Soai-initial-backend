from kavenegar import *


def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI('54516632546366674E463841317272745178673779685753517A54304A6732573755387162517531336F453D')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f'{code} کد تایید شما '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)

