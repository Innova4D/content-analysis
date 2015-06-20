# -*- coding: utf-8 -*-
from pattern.web import URL, plaintext
from google_wrapper import GoogleWrapper
import re

class WebInfo():
	'''
		Class used to mine data from GoogleWrapper.
		Obtains description and schedule (if exists) from POI
	'''

	DOWNLOADABLE = ['text/plain', 'text/html']
	DAYS =u'lunes, martes, miércoles, jueves, viernes, sábado, domingo'
	separator = \
	u'\n--------------------------------------------------------------------\n'
	def __init__(self):
		'''
			Initializing GoogleWrapper
		'''
		self.google = GoogleWrapper()


	def get_data(self, query):
		'''
			Get data from google results
			Iterates over results and downloads description and 
			schedule information
		'''	
		google_result_list = self.google.simple_search(query)
		# Regex for hours
		re_h1 = re.compile(ur'de (\d{1,2}:\d{1,2}) a (\d{1,2}:\d{1,2})')
		re_h2 = re.compile(ur'(\d{1,2}:\d{1,2}) - (\d{1,2}:\d{1,2})')
		re_h3 = re.compile(ur' (\d{1,2}) a (\d{1,2}) ')
		# Regex for days
		re_day = re.compile(ur'de (\S{5,9}) a (\S{5,9})')
		description = []
		schedule = []
		link = ''
		try:
			exception = google_result_list[0]['link']
		except:
			print 'No results from Google'
			return {'description': '',
					'schedule': [],
					'url': ''}
		for result in google_result_list:
			if query.lower() in result['title'].lower() and \
			   query.lower() in result['snippet'].lower() or \
			   'es.wikipedia.org' in result['link']:
			   	# Storing first match
			   	if not link:
			   		link = result['link']
			   	# URL
				url = URL(result['link'])
				print url
				text = []
				if url.mimetype in self.DOWNLOADABLE:
					try:
						text = plaintext(url.download()).split('\n')
					except:
						print 'No response from:', url
				for line in text:
					if len(line.split()) > 50:
						description.append(line)
					# 
					schedule += re_h1.findall(line.lower()) + \
							    re_h2.findall(line.lower()) + \
							    re_h3.findall(line.lower())
					try:
						match = re_day.findall(line.lower())
						for m in match:
							if m[0] in self.DAYS or m[1] in self.DAYS:
								schedule += re_day.findall(line.lower())
					except:
						pass
		return {'description': self.separator.join(description), 
				'schedule': list(set(schedule)),
				'url': link}
