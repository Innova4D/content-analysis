from google_wrapper import GoogleWrapper
from pattern.web import Wikipedia
import re



class WikipediaWrapper():
	'''
		Get info from Wikipedia
	'''


	def __init__(self):
		'''
			Initializing GoogleWrapper
		'''
		self.google = GoogleWrapper()
		self.url_pattern ='http://es.wikipedia.org/wiki'
		self.title_pattern = 'Wikipedia, la enciclopedia libre'


	def search(self, query, language='es'):
		'''
			query: string
			language: 'en' or 'es'
		'''
		wikipedia = Wikipedia(language=language)
		google_result_list = self.google.simple_search(query + ' ' + 'wikipedia')
		wikipedia_results = []
		for result in google_result_list:
			try:
				if self.url_pattern in result['link']:
					article = {}
					title = result['title'].split(' - ')[0]
					print title
					art = wikipedia.search(title)
					print art
					article['title'] = art.title
					article['text'] = art.string
					article['related'] = art.links
					wikipedia_results.append(article)
			except:
				pass
		return wikipedia_results
