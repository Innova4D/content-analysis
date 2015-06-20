import unicodedata
import json

class ResponseFormat(object):
	'''
		ResponseFormat class allows to simplify format according to 
		MongoDB schema
	'''
	separator = \
	u'\n--------------------------------------------------------------------\n'
	def __init__(self):
		pass


	def poi_format(self, poi_name, foursquare_data, web_data, tags=[]):
		'''
			POI format for storing in MongoDB. 

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
		'''
		#-----------Validating foursquare_data-------------#
		try:
			foursquare = foursquare_data['POI_1']
			name = foursquare['name'].lower()
			print type(name)
			name_poi = unicodedata.normalize('NFKD', name).encode('ascii',
																  'ignore')
			poi_name = unicodedata.normalize('NFKD', 
									poi_name.lower()).encode('ascii','ignore')
			if poi_name != name_poi:
				print poi_name
				print name
				print 'POI retrieved is different from query'
				return 'No info retrieved from foursquare, ' + \
				       'status: POI_RETRIEVED_DIFFERENT_FROM_QUERY'

		except KeyError as e:
			print 'No info retrieved from foursquare'
			return 'No info retrieved from foursquare, ' + \
				   'status: EMPTY_FOURSQUARE_RESULT_LIST'
			
		#--------------- Defining schema------------------#
		poi_schema = {}
		poi_schema['CONTEXT_INFO'] = {}
		poi_schema['STATS_INFO'] = {}
		# NAME
		poi_schema['POI_NAME'] = foursquare['name']

		# DESCRIPTION
		description = foursquare['description'] + self.separator + \
					  web_data['description']
		poi_schema['POI_DESCRIPTION'] = description

		# CONTEXT
		address = foursquare['address'] + ', ' + \
				  foursquare['city'] + ', ' + \
				  foursquare['state'] + ', ' + \
				  foursquare['country']
		poi_schema['CONTEXT_INFO']['addr'] = address
		
		lat_long = foursquare['latitude'] + ', ' + \
				   foursquare['longitud']
		poi_schema['CONTEXT_INFO']['lat_long'] = lat_long
		
		poi_schema['CONTEXT_INFO']['skd'] = web_data['schedule']
		
		url = foursquare['url'] or web_data['url']
		poi_schema['CONTEXT_INFO']['url'] = url

		# STATISTICS
		rating = foursquare['statistics']['rating']
		poi_schema['STATS_INFO']['rating'] = rating

		poi_schema['STATS_INFO']['pop'] = foursquare['statistics']['popularity']

		# TAGS
		category = foursquare['category']
		poi_schema['TAGS'] = [category] + tags

		return poi_schema



	def user_format(self, facebook_data, twitter_data, pos_tags=[], 
					neg_tags=[]):
		'''
			USER format for storing in MongoDB

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
		'''
		#--------------- Defining schema------------------#
		user_schema = {}
		user_schema['USER_NAME'] = {}
		user_schema['DEMOGRAPHICS'] = {}

		if isinstance(facebook_data, dict) :
			# USER_NAME
			user_schema['USER_NAME']['fb'] = facebook_data['name']

			# DEMOGRAPHICS
			user_schema['DEMOGRAPHICS']['gender'] = facebook_data['gender']
			user_schema['DEMOGRAPHICS']['age'] = facebook_data['age']
			user_schema['DEMOGRAPHICS']['lang'] = facebook_data['lang']
			user_schema['DEMOGRAPHICS']['from'] = facebook_data['location']

			# USER_DESCRIPTION
			description = facebook_data['bio'] + ' ' + facebook_data['quotes']
			user_schema['USER_DESCRIPTION'] = description

			# USER_LIKES
			user_schema['USER_LIKES'] = pos_tags

			# USER_DISLIKES
			user_schema['USER_DISLIKES'] = neg_tags


			if twitter_data:
				# USER_NAME
				user_schema['USER_NAME']['tw'] = twitter_data['account'] + \
											     ', ' + twitter_data['name']
				# DEMOGRAPHICS
				user_schema['DEMOGRAPHICS']['pop'] = twitter_data['popularity']

				#USER_DESCRIPTION
				user_schema['USER_DESCRIPTION'] += ' ' +  \
												twitter_data['description']

			else:
				user_schema['USER_NAME']['tw'] = ''				
				user_schema['DEMOGRAPHICS']['pop'] = ''

			return user_schema
		else:
			print 'No info retrieved from facebook'
			return facebook_data




