from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json,imagehash,urllib2,io,traceback,sys,numpy
from PIL import Image
# Create your views here.

@csrf_exempt
def index(request):
	message = {}
	print request.method
	if request.method == 'GET':
		message = construct_message(request.GET,'image')
	elif request.method == 'POST':
		print '%r' %request
		message = construct_message(json.loads(request.body),'image')
	else:
		print 'invalid request'
	return HttpResponse(json.dumps(message))


def construct_message(parameter,key):
	message = {}
	if not parameter.has_key(key):
		message['Code'] = 400
		message['Message'] = 'invalid request'
	else:
		url = parameter[key].strip()
		if url == '':
			message['Code'] = 406
			message['Message'] = 'empty ' 
		else:
			try:
				hist = get_hist(url)
				message['Code'] = 200
				message['Message'] = sign
			except:
				traceback.print_exc()
				message['Code'] = 400
				message['Message'] = sys.exc_info()[0]
	return message

def get_hist(url):
	fd = urllib2.urlopen(url)
	image_file = io.BytesIO(fd.read())
	image = Image.open(image_file)
	size = image.size
	wid = size[0]
	height = size[1]
	# convert to greyscale or not.
	image = image.convert("L").resize((100,100), Image.ANTIALIAS)
	vector = image.histogram()
	return vector




