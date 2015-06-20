from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bson.objectid import ObjectId 
from pymongo import MongoClient



class Database(APIView):
	'''
		Retrieve all collections in a MongoDB database 
	'''


	def get(self, request):
		'''
			Gets all items of a determined collection in MongoDB
			QUERY_PARAMS:
				url: (uri:port) from mongodb instance 
					 - default: mongodb://localhost:27017/
				user: string (user for read_only ops) 
					 - default: spribo_r 
					 - be careful, do not provide admin credentials
				psw: string (password for read_only ops)
					 - default: ContentAnalysis
					 - be careful, do not provide admin credentials
				database: string (database name)
					 - default: communities_db
		'''
		# Query Params
		url = request.QUERY_PARAMS.get('url', 'mongodb://localhost:27017/')
		user = request.QUERY_PARAMS.get('user', 'spribo_r')
		psw = request.QUERY_PARAMS.get('psw', 'ContentAnalysis')
		database = request.QUERY_PARAMS.get('database', 'communities_db')

		# MongoClient
		self.client = MongoClient(url)
		self.db = self.client[database]
		# Authenticate as read_only according to default credentials
		try:
			auth = self.db.authenticate(user, psw)
		except Exception as e:
			print e 
			return Response('Authentication failed, wrong reading credentials', 
				    status=status.HTTP_401_UNAUTHORIZED)
		# Read collections in database
		res = []
		try:
			all_collections = self.db.collection_names()
			for collection in all_collections:
				res.append('communities/read/'+collection.split('_')[0]+'/')
		except:
			print 'Check permissions for MongoDB'
			return Response('Check permissions for MongoDB', 
				            status=status.HTTP_401_UNAUTHORIZED)
		# Exiting DB
		self.db.logout()	
		# Response
		return Response(set(res), status=status.HTTP_200_OK)




class Community(APIView):
	'''
		Retrieve all collections in a MongoDB database 
	'''


	def get(self, request, pk):
		'''
			Gets all items of a determined collection in MongoDB
			QUERY_PARAMS:
				url: (uri:port) from mongodb instance 
					 - default: mongodb://localhost:27017/
				user: string (user for read_only ops) 
					 - default: spribo_r 
					 - be careful, do not provide admin credentials
				psw: string (password for read_only ops)
					 - default: ContentAnalysis
					 - be careful, do not provide admin credentials
				database: string (database name)
					 - default: communities_db
		'''
		# Query Params
		url = request.QUERY_PARAMS.get('url', 'mongodb://localhost:27017/')
		user = request.QUERY_PARAMS.get('user', 'spribo_r')
		psw = request.QUERY_PARAMS.get('psw', 'ContentAnalysis')
		database = request.QUERY_PARAMS.get('database', 'communities_db')

		# MongoClient
		self.client = MongoClient(url)
		self.db = self.client[database]
		# Authenticate as read_only according to default credentials
		try:
			auth = self.db.authenticate(user, psw)
		except Exception as e:
			print e 
			return Response('Authentication failed, wrong reading credentials', 
				    status=status.HTTP_401_UNAUTHORIZED)
		# Read collections in database
		name_pois = pk.split('/')[0] + '_pois'
		name_users = pk.split('/')[0] + '_users'
		users = []
		pois = []
		try:
			all_collections = self.db.collection_names()
			self.collection_pois = self.db[name_pois]
			self.collection_users = self.db[name_users]
			users = list(self.collection_users.find())
			for user in users:
				user['_id'] = unicode(user['_id'])
			pois = list(self.collection_pois.find())
			for poi in pois:
				poi['_id'] = unicode(poi['_id'])
		except:
			print 'Check permissions for MongoDB'
			return Response('Check permissions for MongoDB', 
				            status=status.HTTP_401_UNAUTHORIZED)
		# Exiting db
		self.db.logout()
		# Response	
		return Response({'users': users, 'pois': pois},
						 status=status.HTTP_200_OK)
			



class Collection(APIView):
	'''
		Retrieve all collections in a MongoDB database 
	'''


	def get(self, request, pk):
		'''
			Gets all items of a determined collection in MongoDB
			QUERY_PARAMS: (optional)
				url: (uri:port) from mongodb instance 
					 - default: mongodb://localhost:27017/
				user: string (user for read_only ops) 
					 - default: spribo_r 
					 - be careful, do not provide admin credentials
				psw: string (password for read_only ops)
					 - default: ContentAnalysis
					 - be careful, do not provide admin credentials
				database: string (database name)
					 - default: communities_db
		'''
		# Query Params
		url = request.QUERY_PARAMS.get('url', 'mongodb://localhost:27017/')
		user = request.QUERY_PARAMS.get('user', 'spribo_r')
		psw = request.QUERY_PARAMS.get('psw', 'ContentAnalysis')
		database = request.QUERY_PARAMS.get('database', 'communities_db')

		# MongoClient
		self.client = MongoClient(url)
		self.db = self.client[database]
		# Authenticate as read_only according to default credentials
		try:
			auth = self.db.authenticate(user, psw)
		except Exception as e:
			print e 
			return Response('Authentication failed, wrong reading credentials', 
				    status=status.HTTP_401_UNAUTHORIZED)
		# Read collections in database
		collection_name = pk.split('/')[0] + '_' + pk.split('/')[1]
		try:
			self.collection = self.db[collection_name]

			items = list(self.collection.find())
			for item in items:
				item['_id'] = unicode(item['_id'])
		except:
			print 'Check permissions for MongoDB'
			return Response('Check permissions for MongoDB', 
				            status=status.HTTP_401_UNAUTHORIZED)
		# Exiting db
		self.db.logout()
		# Response	
		return Response(items, status=status.HTTP_200_OK)



class Document(APIView):
	'''
		Retrieve all collections in a MongoDB database 
	'''


	def get(self, request, pk):
		'''
			Gets all items of a determined collection in MongoDB
			QUERY_PARAMS: (optional)
				url: (uri:port) from mongodb instance 
					 - default: mongodb://localhost:27017/
				user: string (user for read_only ops) 
					 - default: spribo_r 
					 - be careful, do not provide admin credentials
				psw: string (password for read_only ops)
					 - default: ContentAnalysis
					 - be careful, do not provide admin credentials
				database: string (database name)
					 - default: communities_db
		'''
		# Query Params
		url = request.QUERY_PARAMS.get('url', 'mongodb://localhost:27017/')
		user = request.QUERY_PARAMS.get('user', 'spribo_r')
		psw = request.QUERY_PARAMS.get('psw', 'ContentAnalysis')
		database = request.QUERY_PARAMS.get('database', 'communities_db')

		# MongoClient
		self.client = MongoClient(url)
		self.db = self.client[database]
		# Authenticate as read_only according to default credentials
		try:
			auth = self.db.authenticate(user, psw)
		except Exception as e:
			print e 
			return Response('Authentication failed, wrong reading credentials', 
				    status=status.HTTP_401_UNAUTHORIZED)
		# Read collections in database
		collection_name = pk.split('/')[0] + '_' + pk.split('/')[1]
		item_id = ObjectId(oid=pk.split('/')[2])
		try:
			self.collection = self.db[collection_name]
			item = self.collection.find_one({'_id':item_id})
			item['_id'] = unicode(item['_id'])
		except:
			print 'Check permissions for MongoDB'
			return Response('Check permissions for MongoDB', 
				            status=status.HTTP_401_UNAUTHORIZED)
		# Exiting db
		self.db.logout()
		# Response	
		return Response(item, status=status.HTTP_200_OK)




class ModifyCollection(APIView):
	'''
		Retrieve all collections in a MongoDB database 
	'''
	# Authentication
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def __init__(self):
		self.collection_view = Collection()


	def get(self, request, pk):
		'''
			Gets all items of a determined collection in MongoDB
			QUERY_PARAMS: (optional)
				url: (uri:port) from mongodb instance 
					 - default: mongodb://localhost:27017/
				user: string (user for read_only ops) 
					 - default: spribo_r 
					 - be careful, do not provide admin credentials
				psw: string (password for read_only ops)
					 - default: ContentAnalysis
					 - be careful, do not provide admin credentials
				database: string (database name)
					 - default: communities_db
				content_enabled: boolean (1,0) show content if 1
					 - default: 0
		'''
		res = []
		content_enabled = request.QUERY_PARAMS.get('content_enabled', 0)
		if content_enabled:
			res = self.collection_view.get(request, pk)
			return res
		else:
			return Response(res)


	def post(self, request, format=None):
		'''
			Savinga a list of items (users or pois) into MongoDB

		
			POI SCHEMA
			------------------------------------------------------------------
			{
			 "_ID": "53a084e7d1dfc7bc403f71c0"  // given by MongoDB
			 "POI_NAME": "name",
			 "POI_DESCRIPTION": "description...",
			 "CONTEXT_INFO": {
			 					"addr": "full address",
			 					"lat_long": "latitud, longitud",
			 					"skd": [["day","day"] or/and ["hour","hour"]],
			 					"url": URL
			 				 },
			 "STATS_INFO": {
			 					"rating": 10,
			 					"pop": 10 (arbitrary measure of popularity)
			 				 },
			 "TAGS": [word_1,... word_N]
			 }
			------------------------------------------------------------------


			USER SCHEMA
			------------------------------------------------------------------
			{
			 "_ID": "53a084e7d1dfc7bc403f71c1" // given by MongoDB
			 "USER_NAME": {
			 				"fb": "facebook name",
			 				"tw": "twitter name (account, name)"
			 			  },
			 "DEMOGRAPHICS":{
			 				  "gender": "male or female",
			 				  "age" : 21,
			 				  "lang": "es",
			 				  "from": "MX",
			 				  "pop" : 10 (arbitrary popularity measure)
			 			    },
			 "USER_DESCRIPTION" : "description ...",
			 "USER_LIKES": [word_1,...word_N],
			 "USER_DISLIKES": [word_1,...word_N]
			}
			------------------------------------------------------------------

			JSON FORMAT
				{ 
					"client":{
								"url": "uri of mongod instance" 
								(default:mongodb://localhost:27017/)
								"user":"username",
								"psw":"password"
							
							}, 
					"database":{
								 "name":"database name" (default: communities_db),
								 "community_name": "name of the community",
								 "type": "users" or "pois"							 
							}
					"data":[user_or_poi_schema_1, user_or_poi_schema_2,..., 
							user_or_por_schema_N
							]

				}
		'''
		datum = request.DATA
		# MongoClient
		try:
			self.client = MongoClient(datum['client']['url'])
			self.db = self.client[datum['database']['name']]
			# Authenticate as read_only according to default credentials
			try:
				auth = self.db.authenticate(datum['client']['user'], 
											datum['client']['psw'])
			except Exception as e:
				print e 
				return Response('Authentication failed, wrong reading credentials', 
					    status=status.HTTP_401_UNAUTHORIZED)


			# Creating items in MongoDB
			#try:
			collection_name = datum['database']['community_name'] + '_' + \
							  datum['database']['collection_type']
			self.collection = self.db[collection_name]
			# Insert
			_ids = self.collection.insert(datum['data'])

			for _id in _ids:
				_id = unicode(_id)

			return Response('ok', status=status.HTTP_201_CREATED)

		except:
			pass




class ModifyDocument(APIView):
	'''
		Retrieve all collections in a MongoDB database 
	'''
	# Authentication
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def __init__(self):
		self.document_view = Document()


	def get(self, request, pk):
		'''
			Gets all items of a determined collection in MongoDB
			QUERY_PARAMS: (optional)
				url: (uri:port) from mongodb instance 
					 - default: mongodb://localhost:27017/
				user: string (user for read_only ops) 
					 - default: spribo_r 
					 - be careful, do not provide admin credentials
				psw: string (password for read_only ops)
					 - default: ContentAnalysis
					 - be careful, do not provide admin credentials
				database: string (database name)
					 - default: communities_db
				content_enabled: boolean (1,0) show content if 1
					 - default: 0
		'''
		res = []
		print pk
		content_enabled = request.QUERY_PARAMS.get('content_enabled', 0)
		if content_enabled:
			res = self.document_view.get(request, pk)
			return res
		else:
			return Response(res)


	def put(self, request, format=None):
		'''
			UPDATE a single document

			JSON FORMAT
			{
				"client":{
							"url": "mongodb://localhost:27017/",
							"user":"spribo_r_w",
							"psw":"ContentAnalysis"
						
						}, 
				"database":{
							 "name":"communities_db",
							 "community_name": "dummy",
							 "collection_type": "pois" or "users"							 
						},
				"document"{
							"_id":"53a29ca6d1dfc7e21d3e0b31",

							(fields to change or to add)
							"changes":	{
							 			"name": "new_name",
							 			"new_field": "new_info"
							}
				}
			}
		'''
		datum = request.DATA
		# MongoClient
		try:
			self.client = MongoClient(datum['client']['url'])
			self.db = self.client[datum['database']['name']]
			# Authenticate as read_only according to default credentials
			try:
				auth = self.db.authenticate(datum['client']['user'], 
											datum['client']['psw'])
			except Exception as e:
				print e 
				return Response('Authentication failed, wrong reading credentials', 
					    status=status.HTTP_401_UNAUTHORIZED)

			#try:
			collection_name = datum['database']['community_name'] + '_' + \
							  datum['database']['collection_type']
			self.collection = self.db[collection_name]
			# Update
			item_id = ObjectId(oid=datum['document']['_id'])
			update = self.collection.update({"_id":item_id}, datum['document']['changes'])


			self.db.logout()

			return Response(update, status=status.HTTP_201_CREATED)
		except:
			pass
		


	def delete(self, request, format=None):
		pass
