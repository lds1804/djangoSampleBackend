from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
import numpy as np

from .models import Provider
from .models import Polygon


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as PolygonSha

from django.views.decorators.csrf import csrf_exempt

import json

from django.core import serializers

from django.http import JsonResponse


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


		

		return HttpResponse("Provider added: " + str(provider.id))
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
		coordinates=body["coordinates"]
		providerID=body["provider_id"]

		try:
			provider = Provider.objects.get(pk=providerID)
		except Exception as e:
			provider = None
			return HttpResponseNotFound('<h1>Provider not found</h1>')




		
		polygon =Polygon(name=name,price=price,geojson=coordinates,provider=provider)
		polygon.save()
 
		

		return HttpResponse("Polygon added: " + str(polygon.id))
	else :
		return HttpResponseNotFound('<h1>Entry not found</h1>')



@csrf_exempt
def polygonRUD(request,id):
	if request.method == 'GET':
		print("Id: " + str(id))

				
		polygon = Polygon.objects.filter(pk=id)


		if(len(polygon)==0):
			return JsonResponse({'status_code': 404,'error': 'The resource was not found'},status=404)
		else: 
			print(str(polygon))
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


@csrf_exempt
def polygonsInRegion(request): 

	polygons=Polygon.objects.all()

	body_unicode = request.body.decode('utf-8')
	body = json.loads(body_unicode)

	latitude=body["latitude"]
	longitude=body["longitude"]

	print (type(body))
	
	polygonList=[]

	for polygon in polygons:
		
		lats_vect=[]
		long_vect=[]
		listPoints=polygon.geojson
		for point in listPoints:
			lats_vect.append(point[0])
			long_vect.append(point[1])
		
		if(insidepolygon(lats_vect, long_vect, latitude, longitude)):
			polygonList.append(polygon)	


	return	HttpResponse("Polygon List" + str(polygonList))		




def insidepolygon(lats_vect,long_vect,x,y):

	print(str(lats_vect))
	print(str(long_vect))
	print(str(x))
	print (str(y))

	lons_lats_vect = np.column_stack((long_vect, lats_vect)) # Reshape coordinates
	polygon = PolygonSha(lons_lats_vect) # create polygon
	point = Point(y,x) # create point
	return (point.within(polygon))
	# return (polygon.contains(point)) # check if polygon contains point

