from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from .models import Provider
from .models import Polygon

from django.views.decorators.csrf import csrf_exempt

import json

from django.core import serializers

from django.http import JsonResponse

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

@csrf_exempt
def providerCreate(request):
	
	if request.method == 'POST':

		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		print (body)

		name= body["name"]
		email=body["email"]
		phone=body["phone"]
		language=body["language"]
		currency=body["currency"]
		provider = Provider(name=name, email=email, phone=phone, language= language, currency= currency)
		provider.save()


		

		return HttpResponse("Provider added: " + provider.id)
	else :
		return HttpResponseNotFound('<h1>Entry not found</h1>')

@csrf_exempt
def providerRUD(request,id):
	if request.method == 'GET':

		try:
			provider = Provider.objects.get(pk=id)
		except Exception as e:
			provider = None
		else:
			pass
		finally:
			pass
		


		if(provider!=None):

			return HttpResponse("Provider : " + str(provider))
		else: 
			return HttpResponseNotFound('<h1>Page not found</h1>')

	
	
	elif request.method == "PATCH" :

		provider = Provider.objects.get(pk=id)

		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		keys= body.keys()

		print(body)

		Provider.objects.filter(pk=id).update(**body)

		for fieldName in keys:
			print(body[fieldName])
			setattr(provider, fieldName, body[fieldName])
			# provider.setattr(user, field_name, False)
			provider.save()

		print(provider.name)

		

		return HttpResponse("Provider update: " + str(provider))

	elif request.method == "DELETE" :

		provider = Provider.objects.get(pk=id)


	
		provider.delete()

			

		return HttpResponse("Provider deleted: " + str(provider))


	else :
		return HttpResponseNotFound('<h1>Page not found</h1>')

			
@csrf_exempt
def polygonCreate(request):
	
	if request.method == 'POST':

		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		print (body)

		name= body["name"]
		price=body["price"]
		geojson=body["geojson"]
		providerID=body["provider_id"]

		try:
			provider = Provider.objects.get(pk=providerID)
		except Exception as e:
			provider = None
			return HttpResponseNotFound('<h1>Provider not found</h1>')




		
		polygon =Polygon(name=name,price=price,geojson=geojson,provider=provider)
		polygon.save()
 
		

		return HttpResponse("Polygon added: " + str(polygon.id))
	else :
		return HttpResponseNotFound('<h1>Entry not found</h1>')



@csrf_exempt
def polygonRUD(request,id):
	if request.method == 'GET':
		print("Id: " + str(id))

				
		polygon = Polygon.objects.filter(pk=id)


		if(polygon==None):
			return JsonResponse({'status_code': 404,'error': 'The resource was not found'},status=404)
		else: 
			data = serializers.serialize("json", polygon)
			return JsonResponse(data,safe=False)	

	
	
	elif request.method == "PATCH" :

		polygon = Polygon.objects.filter(pk=id)

		if(polygon==None):
			return JsonResponse({'status_code': 404,'error': 'The resource was not found'},status=404)
		else: 
			body_unicode = request.body.decode('utf-8')
			body = json.loads(body_unicode)

			keys= body.keys()

			print(body)

			Polygon.objects.filter(pk=id).update(**body)

			for fieldName in keys:
				print(body[fieldName])
				setattr(polygon, fieldName, body[fieldName])

			print(polygon.name)
			return JsonResponse({'status_code': 200,'Message': 'Resource updated'},status=200)

	elif request.method == "DELETE" :

		polygon = Polygon.objects.filter(pk=id)


	
		polygon.delete()

			

		return JsonResponse({'status_code': 200,'Message': 'Resource deleted'},status=200)


	else :
		return HttpResponseNotFound('<h1>Not permited</h1>')






# Create your views here.
