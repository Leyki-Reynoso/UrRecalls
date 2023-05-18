import urllib.request
from django.core.mail import send_mail
#import urllib
#from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework import status, response
from .models import *
from .serializers import *
from pprint import pprint
import requests
import json
from google_images_search import GoogleImagesSearch
from pathlib import Path
import glob
import os
from django.core.files import File
import re, math
import sys
from collections import Counter
from rest_framework import generics

# Create your views here.

class createUser(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			user = Users.objects.create(**data)
			return Response({'Status':'CREATED'})
		except Exception as e:
			return Response({'Error': repr(e)})

class getUser(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			user = Users.objects.filter(username__contains=data.pop('username'), password__contains=data.pop('password'))
			serialized = userSerializer(user, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class refreshSaved(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			user = Users.objects.filter(id__contains=data.pop('id'))
			serialized = userSerializer(user, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertFood(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			if 'Product_Name' in data:
				pass
			else:
				raise Exception('Must include Product_Name')
			food = RecallsFood.objects.create(**data)
			# print(food.__dict__)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})
	
class InsertDrug(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			if 'DrugName' in data:
				pass
			else:
				raise Exception('Must include DrugName')
			drugs = RecallsDrugs.objects.create(**data)
			# print(goods.__dict__)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertCars(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			for x in ['make','model','year']:
				if x in data:
					continue
				else:
					raise Exception('Must include make, model, year')
			cars_data = {}
			for x in ['make','model','year']:
				if x in data:
					cars_data[x] = data[x]
				else:
					raise Exception('Improper Key:Value')
			# print(cars_data)
			cars = RecallsCars.objects.create(**cars_data)
			info = CarRecallInfo.objects.create(**data)
			cars.recallInfo.add(info)
			# print(cars.__dict__)
			return Response({'Status':'CREATED'})
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertGoods(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			if 'name' in data:
				pass
			else:
				raise Exception('Must include name')
			goods = RecallsGoods.objects.create(**data)
			# print(goods.__dict__)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertUserGoods(APIView):
	def put(self, request, format=None):
		data = { k:request.data[k] for k in request.data }
		# put raise Exception('Improper Key:Value') check here ***********
		user = Users.objects.get(id=data.pop('userID'))
		goods = RecallsGoods.objects.get(id=data.pop('ID'))
		user.recalls_goods.add(goods)
		serialized = userSerializer(user).data 
		return Response(serialized)

class InsertUserDrugs(APIView):
	def put(self, request, format=None):
		data = { k:request.data[k] for k in request.data }
		# put raise Exception('Improper Key:Value') check here ***********
		user = Users.objects.get(id=data.pop('userID'))
		drugs = RecallsGoods.objects.get(id=data.pop('ID'))
		user.recalls_drugs.add(drugs)
		serialized = userSerializer(user).data 
		return Response(serialized)

class InsertUserFood(APIView):
	def put(self, request, format=None):
		data = { k:request.data[k] for k in request.data }
		# put raise Exception('Improper Key:Value') check here ***********
		user = Users.objects.get(id=data.pop('userID'))
		food = RecallsGoods.objects.get(id=data.pop('ID'))
		user.recalls_food.add(food)
		serialized = userSerializer(user).data 
		return Response(serialized)

class InsertUserCars(APIView):
	def put(self, request, format=None):
		data = { k:request.data[k] for k in request.data }
		# put raise Exception('Improper Key:Value') check here ***********
		user = Users.objects.get(id=data.pop('userID'))
		cars = RecallsGoods.objects.get(id=data.pop('ID'))
		user.recalls_cars.add(cars)
		serialized = userSerializer(user).data 
		return Response(serialized)

class GetGoods(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			goods = RecallsGoods.objects.filter(name__contains=data.pop('name'))
			# pprint(goods[0].__dict__)
			serialized = goodsSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetGoodsByUPC(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			upc = data.pop('UPC')
			r = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc='+upc)
			r = r.json()
			if(len(r['items']) > 0):
				name = r['items'][0]['title']
				brand = r['items'][0]['brand']
			goods = RecallsGoods.objects.filter(name__contains=brand)
			serialized = goodsSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class SearchGoods(APIView):
	def Update(r):
		if(len(r) < 0):
			return
		for i in range(len(r)-1):
			d = {}
			if  len(r[i]['Products']) > 0 :
				d["name"] = r[i]['Products'][0]['Name']
			d["title"] = r[i]['Title']
			d["recallDate"] = r[i]['RecallDate']
			d["recallNumber"] = r[i]['RecallNumber']
			d["description"] = r[i]['Description']
			d["url"] = r[i]['URL']
			d["consumerContact"] = r[i]['ConsumerContact']
			if  len(r[i]['Images']) > 0 :
				d["image"] = r[i]['Images'][0]['URL']
			if  len(r[i]['Injuries']) > 0 :
				d["inguries"] = r[i]['Injuries'][0]['Name'] 
			if  len(r[i]['Manufacturers']) > 0 :
				d["manufacturers"] = r[i]['Manufacturers'][0]['Name'] 
			if  len(r[i]['Retailers']) > 0 :
				d["retailers"] = r[i]['Retailers'][0]['Name']
			if  len(r[i]['ManufacturerCountries']) > 0 :
				d["manufacturerCountries"] = r[i]['ManufacturerCountries'][0]['Country']
			if  len(r[i]['Hazards']) > 0 :
				d["hazards"] = r[i]['Hazards'][0]['Name']
			if  len(r[i]['Remedies']) > 0 :
				d["remedies"] = r[i]['Remedies'][0]['Name']
			if  len(r[i]['Distributors']) > 0 :
				d["distributors"] = r[i]['Distributors'][0]['Name']
			q = requests.post('http://ec2-34-227-36-231.compute-1.amazonaws.com/general/InsertGoods', d)
			print(q.text)

	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			r = requests.get('https://www.saferproducts.gov/RestWebServices/Recall?format=json&ProductName='+ data.pop('name'))
			r = r.json()
			SearchGoods.Update(r)
			return Response(r)
		except Exception as e:
			return Response({'Error': repr(e)})

class SearchCars(APIView):
	def Update(r):
		#insert into our DB
		if(len(r) < 0):
			return
		for x in range(len(r['Results'])):
			d = {}
			d['make'] = r['Results'][x]["Make"]
			d['model'] = r['Results'][x]["Model"]
			d['year'] = r['Results'][x]["ModelYear"]
			d['manufacturer'] = r['Results'][x]["Manufacturer"]
			d['NHTSAcampaignnumber'] = r['Results'][x]["NHTSACampaignNumber"]
			d['reportReceivedDate'] = r['Results'][x]["ReportReceivedDate"]
			d['Summary'] = r['Results'][x]["Summary"]
			d['Conequence'] = r['Results'][x]["Conequence"]
			d['Remedy'] = r['Results'][x]["Remedy"]
			d['Component'] = r['Results'][x]["Component"]
			d['Notes'] = r['Results'][x]["Notes"]
			q = requests.post('http://ec2-34-227-36-231.compute-1.amazonaws.com/general/InsertCars', d)
			print(q.text)
			
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			r = requests.get('https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+ data.pop('year')+ '/make/' + data.pop('make')+ '/model/' + data.pop('model')+ '?format=json')
			r = r.json()
			SearchCars.Update(r)
			return Response(r)
		except Exception as e:
			return Response({'Error': repr(e)})



class GetCars(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			car = RecallsCars.objects.filter(make__contains=data.pop('make'), model__contains=data.pop('model'), year__contains=data.pop('year'))
			# pprint(goods[0].__dict__)
			serialized = carSerializer(car, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})


class GetFood(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			food = RecallsFood.objects.filter(Product_Name__contains=data.pop('Product_Name'))
			# pprint(goods[0].__dict__)
			serialized = foodSerializer(food, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetFoodByUPC(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			food = RecallsFood.objects.filter(UPCs__contains=data.pop('UPC'))
			# pprint(goods[0].__dict__)
			serialized = foodSerializer(food, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})


class GetAllFood(APIView):
	def post(self, request, format=None):
		try:
			food = RecallsFood.objects.all()
			serialized = foodSerializer(food, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllDrugs(APIView):
	def post(self, request, format=None):
		try:
			drug = RecallsDrugs.objects.all()
			serialized = drugSerializer(drug, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllCars(APIView):
	def post(self, request, format=None):
		try:
			car = RecallsCars.objects.all()
			serialized = carSerializer(car, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllGoods(APIView):
	def post(self, request, format=None):
		try:
			goods = RecallsGoods.objects.all()
			serialized = goodsSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetDrugs(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			drugs = RecallsDrugs.objects.filter(DrugName__contains=data.pop('DrugName'))
			# pprint(goods[0].__dict__)
			serialized = drugSerializer(drugs, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetDrugsByNDC(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			drugs = RecallsDrugs.objects.filter(NDCs__contains=data.pop('NDC'))
			# pprint(goods[0].__dict__)
			serialized = drugSerializer(drugs, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetCars(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			# put raise Exception('Improper Key:Value') check here ***********
			cars = RecallsCars.objects.filter(make__contains=data.pop('make'), model__contains=data.pop('model'), year__contains=data.pop('year'))
			# pprint(goods[0].__dict__)
			serialized = carSerializer(cars, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})


class InsertGoodsIssue(APIView):
	def toUser(issue_id, user_id):
		#cars.recallInfo.add(info)
		user = Users.objects.get(id=user_id)
		issue = GoodsIssues.objects.get(id=issue_id)
		user.issues_goods.add(issue)
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			for x in ['name','title','description', 'user_id']:
				if x in data:
					continue
				else:
					raise Exception('Must include name, title, description, user_id')
			user_id = data.pop('user_id')
			goods = GoodsIssues.objects.create(**data)
			InsertGoodsIssue.toUser(goods.id, user_id)
			
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertFoodIssue(APIView):
	def toUser(issue_id, user_id):
		#cars.recallInfo.add(info)
		user = Users.objects.get(id=user_id)
		issue = FoodIssues.objects.get(id=issue_id)
		user.issues_food.add(issue)
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			for x in ['name','title','description', 'user_id']:
				if x in data:
					continue
				else:
					raise Exception('Must include name, title, description, user_id')
			user_id = data.pop('user_id')
			goods = FoodIssues.objects.create(**data)
			InsertFoodIssue.toUser(goods.id, user_id)
			
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertDrugIssue(APIView):
	def toUser(issue_id, user_id):
		#cars.recallInfo.add(info)
		user = Users.objects.get(id=user_id)
		issue = DrugIssues.objects.get(id=issue_id)
		user.issues_drugs.add(issue)
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			for x in ['name','title','description', 'user_id']:
				if x in data:
					continue
				else:
					raise Exception('Must include name, title, description, user_id')
			user_id = data.pop('user_id')
			goods = DrugIssues.objects.create(**data)
			InsertDrugIssue.toUser(goods.id, user_id)
			
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class InsertCarIssue(APIView):
	def toUser(issue_id, user_id):
		#cars.recallInfo.add(info)
		user = Users.objects.get(id=user_id)
		issue = CarIssues.objects.get(id=issue_id)
		user.issues_cars.add(issue)
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			for x in ['make', 'model', 'year','title','description', 'user_id']:
				if x in data:
					continue
				else:
					raise Exception('Must include MMY, title, description, user_id')
			user_id = data.pop('user_id')
			goods = CarIssues.objects.create(**data)
			InsertCarIssue.toUser(goods.id, user_id)
			
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class addGoodsComment(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = GoodsIssues.objects.get(id=data.pop('id'))
			comm = Threads.objects.create(comment= data.pop('comment'))
			issue.goods_comment.add(comm)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class upVoteGoods(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = GoodsIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_goods.all():
				issue.votes += 1
				issue.save()
				user.votes_goods.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Up Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class addDrugComment(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = DrugIssues.objects.get(id=data.pop('id'))
			comm = Threads.objects.create(comment= data.pop('comment'))
			issue.drug_comment.add(comm)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class upVoteDrug(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = DrugIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_drug.all():
				issue.votes += 1
				issue.save()
				user.votes_drug.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Up Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class downVoteDrug(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = DrugIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_drug.all():
				issue.votes -= 1
				issue.save()
				user.votes_drug.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Down Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class addFoodComment(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = FoodIssues.objects.get(id=data.pop('id'))
			comm = Threads.objects.create(comment= data.pop('comment'))
			issue.food_comment.add(comm)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class upVoteFood(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = FoodIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_food.all():
				issue.votes += 1
				issue.save()
				user.votes_food.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Up Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class downVoteFood(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = FoodIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_food.all():
				issue.votes -= 1
				issue.save()
				user.votes_food.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Down Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class addCarComment(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = CarIssues.objects.get(id=data.pop('id'))
			comm = Threads.objects.create(comment= data.pop('comment'))
			issue.car_comment.add(comm)
			return Response({'Status':'CREATED'})  
		except Exception as e:
			return Response({'Error': repr(e)})

class upVoteCar(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = CarIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_car.all():
				issue.votes += 1
				issue.save()
				user.votes_car.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Up Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class downVoteCar(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = CarIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_car.all():
				issue.votes -= 1
				issue.save()
				user.votes_car.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Down Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})


class downVoteGoods(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			issue = GoodsIssues.objects.get(id=data.pop('id'))
			user = Users.objects.get(id=data.pop('userID'))
			if issue not in user.votes_goods.all():
				issue.votes -= 1
				issue.save()
				user.votes_goods.add(issue)
			else:
				raise Exception('This user already voted')
			return Response({'Status':'Down Voted'})
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllGoodsIssues(APIView):
	def post(self, request, format=None):
		try:
			goods = GoodsIssues.objects.all()
			serialized = goodsIssuesSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllCarsIssues(APIView):
	def post(self, request, format=None):
		try:
			goods = CarIssues.objects.all()
			serialized = carIssuesSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllFoodIssues(APIView):
	def post(self, request, format=None):
		try:
			goods = FoodIssues.objects.all()
			serialized = foodIssuesSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetAllDrugIssues(APIView):
	def post(self, request, format=None):
		try:
			goods = DrugIssues.objects.all()
			serialized = drugIssuesSerializer(goods, many=True).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetCarImage(APIView):
	def getImage(m, mo, y):
		gis = GoogleImagesSearch('AIzaSyCmMTfEgbsuRXy5aCPClCUZQjMiUULpAIg','003481545842197392659:wucdsj_bptm')
		car = str(m) + " " + str(mo) + " " + str(y)
		car_name = str(m) + "_" + str(mo) + "_" + str(y)
		download_path = Path("/home/ubuntu/UrRecalls/media/images/")
		
		#Search Parameters
		gis.search({'q': car, 'num': 1})
		# Download image to path and resize
		try:
			for image in gis.results():
				image.download(download_path)
				#image.resize(500, 500)
				
			print("Image succesfully retrieved for: " + car)
		except:
			print("Unexpected error downloading image")

		# # Get lastest file from dir
		list_of_files = download_path.glob('*')
		latest_file = max(list_of_files, key=lambda p: p.stat().st_ctime)
		# #New File Name
		car = m + mo + y
		newName = car + '.jpg'
		# #New File Path
		renamed_path = Path("/home/ubuntu/UrRecalls/media/images/" + newName)  
		# #Rename file to car name 
		os.rename(latest_file, renamed_path)
		link = "http://ec2-34-227-36-231.compute-1.amazonaws.com/media/images/" + newName
		image = CarImages.objects.create(make= m, model=mo, year=y, image=link)
		# image.image.save(car_name + '.jpg', django_file, save=True)
		# image.save()
		return "Image inserted"

	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			m = data.pop('make')
			mo = data.pop('model')
			y = data.pop('year')
			try:
				car = CarImages.objects.get(make=m, model=mo, year=y)
				serialized = carImageSerializer(car).data
				return Response(serialized)
			except Exception as e:
				#return Response({'Error': repr(e)})
				url = GetCarImage.getImage(m, mo, y)
				car = CarImages.objects.get(make=m, model=mo, year=y)
				serialized = carImageSerializer(car).data
				return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})

class GetFoodImage(APIView):
	def getImage(food_name):
		gis = GoogleImagesSearch('AIzaSyCmMTfEgbsuRXy5aCPClCUZQjMiUULpAIg','003481545842197392659:wucdsj_bptm')
		
		download_path = Path("/home/ubuntu/UrRecalls/media/images/")
		
		#Search Parameters
		gis.search({'q': food_name, 'num': 1})
		# Download image to path and resize
		try:
			for image in gis.results():
				image.download(download_path)
				image.resize(600, 600)
				
			print("Image succesfully retrieved for: " + food_name)
		except:
			print("Unexpected error downloading image")

		# # Get lastest file from dir
		list_of_files = download_path.glob('*')
		latest_file = max(list_of_files, key=lambda p: p.stat().st_ctime)
		# #New File Name
		
		newName = food_name + '.jpg'
		newName = newName.replace(" ", "")
		# #New File Path
		renamed_path = Path("/home/ubuntu/UrRecalls/media/images/" + newName)  
		# #Rename file to car name 
		os.rename(latest_file, renamed_path)
		link = "http://ec2-34-227-36-231.compute-1.amazonaws.com//media/images/" + newName
		image = FoodImages.objects.create(name=food_name, image=link)
		
		return "Image inserted"

	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }
			food_name = data.pop('food_name')
			
			try:
				food = FoodImages.objects.get(name=food_name)
				serialized = foodImageSerializer(food).data
				return Response(serialized)
			except Exception as e:
				#return Response({'Error': repr(e)})
				url = GetFoodImage.getImage(food_name)
				food = FoodImages.objects.get(name=food_name)
				serialized = foodImageSerializer(food).data
				return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})


class altProducts(APIView):
	def post(self, request, format=None):
		try:
			data = { k:request.data[k] for k in request.data }

			
			productNames = json.loads(data.pop('productNames'))
			productIngreds = json.loads(data.pop('productIngreds'))
			product_diets = json.loads(data.pop('product_diets'))
			productIngred = data.pop('productIngred')
			user_diets = data.pop('userDiets')
			
			WORD = re.compile(r'\w+')

			def get_cosine(vec1, vec2):
				intersection = set(vec1.keys()) & set(vec2.keys())
				numerator = sum([vec1[x] * vec2[x] for x in intersection])

				sum1 = sum([vec1[x]**2 for x in vec1.keys()])
				sum2 = sum([vec2[x]**2 for x in vec2.keys()])
				denominator = math.sqrt(sum1) * math.sqrt(sum2)

				if not denominator:
					return 0.0
				else:
					return float(numerator) / denominator

			def text_to_vector(text):
				words = WORD.findall(text)
				return Counter(words)


			compatibleProducts = []
			restrictDiet = []
			user_diets = user_diets.split(",")
			product_ids = list(product_diets.keys())

			if ('0' in user_diets):
				for i in range(len(user_diets)):
					if (user_diets[i] == "0"):
						restrictDiet.append(i)
			else:
				for i in range(len(product_ids)):
					compatibleProducts.append(product_ids[i])

			for i in range(len(product_ids)):
				compatible = True
				prodDiet = product_diets[product_ids[i]].replace("2","1")
				prodDiet = prodDiet.split(",")
				for j in range(len(restrictDiet)):
					if (prodDiet[restrictDiet[j]] != "0"):
						compatible = False
				if (compatible) and (product_ids[i] not in user_diets):
					compatibleProducts.append(product_ids[i])

			for i in range(len(compatibleProducts)):
					productIngreds[compatibleProducts[i]] = productIngreds[compatibleProducts[i]].replace("and", "").replace("/", "").replace("&", "").replace(".", "").replace("(", ",").replace(")", ",").replace(",,,","").replace(",,","").replace(',', "")
			print(compatibleProducts)
			print(restrictDiet)
			text2 = productIngred
			names = {}
			for i in range(len(compatibleProducts)):
					print(productIngreds[compatibleProducts[i]])
					vector1 = text_to_vector(productIngreds[compatibleProducts[i]])
					vector2 = text_to_vector(text2)
					cosine = get_cosine(vector1, vector2)
					print (cosine)
					if cosine > 0.04:
							names[compatibleProducts[i]] = (productNames[compatibleProducts[i]])


			# print ("complete")
			
			return Response({'Response': names})
		except Exception as e:
			return Response({'Error': repr(e)})

# report product
class InsertReportProduct(APIView):
	def post(self, request, format=None):
		try:
			data = {k: request.data[k] for k in request.data}
			report = ReportProduct.objects.create(**data)
			#new_data = "This is an email from urRecall. it is a user Product Report.\nBelow are the details\n"+"Name: "+report.firstname+" "+report.lastname+ "User Email: "+ report.useremail+ "User Phone no: "+report.userPhoneNumber+ "Preferred Contact Method: " + report.preferredcontactmethod + "Product UPC: "+report.upc+ "Product Type: "+ report.identifyProduct+ "Product Purchase Location: "+ report.locationOfPurchase+"Product Issue Description: " + report.describeProblem + "Doctor Name (if medical care required): "+ report.doctorName + "\n"
			new_data = "UrRecall Product Report:\n\n"+"Name: "+report.firstname+" "+ report.lastname + "\nUser Email: " + report.useremail + "\nUser phone number: " + report.userPhoneNumber + "\nPreferred Contact Method: " + report.preferredcontactmethod + "\nProduct UPC: " +report.upc + "\nProduct Type: "+ report.identifyProduct +""
			new_data+= "\nProduct Purchase Location: " + report.locationOfPurchase +", " + report.userZipCode + ""
			new_data+= "\nProduct Issue Description: " + report.describeProblem + "\nDoctor's Name : " + report.doctorName +""
			#print(new_data)
			send_mail('UrRecall Product Report by '+report.firstname+'.', new_data, 'urrecalls@gmail.com',['info@scanavert.com'], fail_silently=True)
			return Response({'Status': 'CREATED'})

		except Exception as e:
			return Response({'Error': repr(e)})


class GetAllReportProduct(APIView):
	def get(self, request, format=None):
		try:
			reports = ReportProduct.objects.last()
			print(reports)
			serialized = reportProductSerializer(reports).data
			return Response(serialized)
		except Exception as e:
			return Response({'Error': repr(e)})


class AddressView(generics.ListCreateAPIView):

	def get_queryset(self):
		userid = self.request.query_params.get('userid')
		if not userid:
			return Address.objects.first()
		else:
			return Address.objects.filter(user=userid)


	def get_serializer_class(self):
		if self.request.method == 'GET':
			return AddressListSerializer
		else:
			return AddressDetailSerializer

class InsertUserFoodProduct(APIView):
    def post(self, request, format=None):
        try:
            data = { k:request.data[k] for k in request.data }
            product = Users_products_food.objects.create(**data)
            return Response({'Status':'CREATED'})
        except Exception as e:
            return Response({'Error': repr(e)})

class GetUserFoodProduct(APIView):
    def post(self, request, format=None):
        try:
            data = { k:request.data[k] for k in request.data }
            product = Users_products_food.objects.filter(users_id=data.pop('users'))
            serialized = usersProductsFoodSerializer(product, many=True).data
            return Response(serialized)
        except Exception as e:
            return Response({'Error': repr(e)})

# send emails loads
#def sendReportEmail(requests):
   #productreport = requests.get('http://127.0.0.1:8000/general/GetreportProduct')  # call api
   #report_data = productreport.json()
   #final_data = json.dumps(report_data)
   #send_mail('New Product Report', final_data, 'urrecalls@gmail.com', ['sulekhadahiya12@gmail.com','moreanju0312@gmail.com'], fail_silently=False)