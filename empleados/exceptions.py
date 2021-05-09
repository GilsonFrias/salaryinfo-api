from rest_framework.views import exception_handler

def my_exception_handler(exc, context):
	print('On exception block...')
	response = exception_handler(exc, context)
	if response is not None:
		response.data['message'] = str(exc)
		response.data['result'] = None
		del response.data['detail']
	return response
