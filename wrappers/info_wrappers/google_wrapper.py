# -*- coding: utf-8 -*-
# $ pip install --upgrade google-api-python-client
# first it is created a google custom search service at http://www.google.com/cse/
# -then configure it to search the entire web
# -obtain cx_key from code snippet
# -finally obtain API_KEY from API ACCESS in the API control panel
try:
	from googleapiclient.discovery import build
except:
	from apiclient.discovery import build



# Spribo credentials:
# In order to use this code outside you need to get your own credentials
API_KEY = "AIzaSyAdHnvmBSL6k0vY_qJQcnAuqagSZ3LjoSM"
cx_key  = '011033102363583886669:avf3hux4mn4'


class GoogleWrapper(object):
	'''
		Class to wrap Google Custom Search service
	'''


	def __init__(self, license=None, language='lang_es', geolocation='mx'):
	    """ 
	    	license     : license key for the API
	    	geolocation : default country of search is defined as Mexico
	    """
	    if license:
	    	self.license = license
	    else:
	    	self.license = API_KEY
	    	print 'Spribo Credentials'
	    self.geolocation = geolocation
	    self.language = language


	def search(self, query, num_results=10, starting_at=1):
	    """ 
		    Returns a dict of results from Google for the given query.
		    - num_results: number of displayed results (from 1 to 10)
		    - starting_at: number of starting point,
		    - there is a daily limit of 100 free queries. Google Custom Search is 
		      a paid service if more queries are needed.
	    """
	    try:
		    if isinstance(query, str):
		    	query = unicode(query, "utf-8", "xmlcharrefreplace")
		    service = build("customsearch", "v1", developerKey=self.license)
		    result  = service.cse().list( q     = query, 
										  gl    = self.geolocation,
										  lr	= self.language, 
										  num   = num_results,
										  start = starting_at,
										  cx	= cx_key,).execute()
		    return result
	    except Exception as e:
	    	print e
        	return {}


	def simple_search(self, query):
		""" 
			Returns short list of results to a user query
			- query: string of the query
		"""
		results = self.search(query)
		if results:
			list = []
			try:
					for result in results['items']:
						dictionary  = {}
						dictionary['title'] = result['title']
						dictionary['link'] = result['link']
						dictionary['snippet'] = result['snippet']
						list.append(dictionary)
					return list
			except KeyError as  e:
					print 'No information in the result', e
					return []
		else:
			print 'Google API returned None'
			return []




