from __future__ import division
from math import log10
from twython import Twython, TwythonError
import logging


# Twitter API Credentials  
# Username: @spribo_content
# Password: ContentAnalysis

APP_KEY ='s1ElxA7pIkHIB8l9nrpcGxeMx'
APP_SECRET ='xuiJIUvzlFjSyJgnQX0aAidpTzycUcyadFRfDUXwsZhLcxk5VG'      
OAUTH_TOKEN ='2547091116-0CuTsxASDvXF0jK1d50EdCrR9TTdyCglsNCxZWA'
OAUTH_TOKEN_SECRET ='j7dkRMivK6O5QvuRFtEa8eQfG3pCKWingoG3eet4eURrE'

class TwitterWrapper():

	logging.basicConfig(filename='twitter.log', 
					format='%(asctime)s, %(levelname)s: %(message)s',
					level=logging.DEBUG)

	def __init__(self, **kwargs):
		'''
			**kwargs for twitter credentials 
			{'APP_KEY': value, 'APP_SECRET': value, 
			'OAUTH_TOKEN': value, 'OAUTH_TOKEN_SECRET': value}
		'''
		# Initializing twitter instance
		if kwargs:
			print 'User-defined Credentials'
			app_key = kwargs['APP_KEY']
			app_secret = kwargs['APP_SECRET']
			oauth_token = kwargs['OAUTH_TOKEN']
			oauth_token_secret = kwargs['OAUTH_TOKEN_SECRET']
			self.twitter = Twython(app_key, app_secret, oauth_token, 
				                   oauth_token_secret)
		else:
			print 'Spribo Credentials'
			self.twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, 
				                   OAUTH_TOKEN_SECRET)


	def get_user_tweets(self, username, simple=True):
		'''
			Retrieves last tweets from single user
			username: string "@username"
			simple: if True response is minimal, if False response is full
		'''
		twitter = self.twitter
		username = username.replace('@', '')
		try:
			user_timeline = twitter.get_user_timeline(screen_name=username)
			if not user_timeline:
				print 'There are no tweets in this account'
				return {}
			list = []
			for t in user_timeline:
				tweet = {}
				tweet['id'] = t['id']
				tweet['text'] = t['text']
				tweet['lang'] = t['lang']
				tweet['hashtags'] = [h['text'] for h in t['entities']['hashtags']]
				tweet['mentions'] = [n['name'] for n in t['entities']['user_mentions']]
				tweet['urls'] = [u['expanded_url'] for u in t['entities']['urls']]
				tweet['date'] = t['created_at']
				list.append(tweet)
			user = user_timeline[0]['user']
			if simple:
				return list
			else:
				return user_timeline
		except TwythonError as e:
			logging.error(e)
			return e


	def get_user_profile(self, username, simple=True):
		'''
			Retrieves profile from user
			username: string "@username"
			simple: if True response is minimal, if False response is full
		'''
		twitter = self.twitter
		username = username.replace('@', '')
		try:
			user_profile = twitter.show_user(screen_name=username)
			if user_profile['protected']:
				print 'User profile protected'
			user = {}
			user['id'] = user_profile['id']
			user['description'] = user_profile['description']
			user['account'] = '@' + user_profile['screen_name']
			user['lang'] = user_profile['lang']
			user['name'] = user_profile['name']
			user['protected'] = user_profile['protected']
			user['followers_count'] = user_profile['followers_count']
			user['listed_count'] = user_profile['listed_count']
			# Arbitrary user popularity
			user['popularity'] = log10(user['followers_count'] / 5) + \
								 log10(user['listed_count'] + 1) 
			if simple:
				return user
			else:
				return user_profile
		except TwythonError as e:
			print e

 
	def get_friends(self, username):
		'''
			Get user friends
		'''
		twitter = self.twitter
		username = username.replace('@', '')
		
		try:
			friends_ids = twitter.get_friends_ids(screen_name=username)
			list=[]
			for i in friends_ids['ids']:
				user = twitter.show_user(user_id=i)
				list.append(user['screen_name'])
			return list
		except TwythonError as e:
			print e


	def get_followers(self, username):
		'''
			Get user followers
		'''
		twitter = self.twitter
		username = username.replace('@', '')
		try:
			followers_ids = twitter.get_followers_ids(screen_name=username)
			list=[]
			for i in followers_ids['ids']:
				user = twitter.show_user(user_id=i)
				list.append(user['screen_name'])
			return list
		except TwythonError as e:
			print e


	def generate_users_graph(self, username_list, graph, levels=1):
		'''
			Generate user graph
			In order to use this method a graph object is needed with two methods: 
	 		add_node(node) and add_edge(node_1, node_2) 
		'''
		if levels > 0:
			try:
				for username in username_list:
					username = username.replace('@', '')
					graph.add_node(username)
					friends = self.get_friends(username)
					followers = self.get_followers(username)
					if friends is not None:
						for friend in friends:
							graph.add_node(friend)
							graph.add_edge(username, friend)
					else:
						friends = []
					if followers is not None:
						for follower in followers:
							graph.add_node(follower)
							graph.add_edge(follower, username)
					else:
						followers = []
					# Recursive call
					graph = self.generate_users_graph(friends + followers, 
													  graph, levels-1)
				return graph
			except TwythonError as e:
				print e
				return graph
		else:
			return graph



	def generate_ids_graph(self, user_ids_list, graph, levels=2, direction='DOWN'):
		'''
			Generate twitter graph 
			In order to use this method a graph object is needed with two methods: 
		 	add_node(node) and add_edge(node_1, node_2)
		'''
		twitter = self.twitter
		if levels > 0:
			try:
				for user_id in user_ids_list:
					friends = []
					followers = []
					graph.add_node(user_id)
					if direction == 'UP' or direction == 'UP_DOWN':
						friends = twitter.get_friends_ids(user_id=user_id)['ids']
					if direction == 'DOWN' or direction =='UP_DOWN':
						followers = twitter.get_followers_ids(user_id=user_id)['ids']
					if friends is not None:
						for friend in friends:
							graph.add_node(friend)
							graph.add_edge(user_id, friend)
					else:
						friends = []
					if followers is not None:
						for follower in followers:
							graph.add_node(follower)
							graph.add_edge(follower, user_id)
					else:
						followers = []
					# Recursive call
					graph = self.generate_ids_graph(friends + followers, 
													graph, levels-1)
				return graph
			except TwythonError as e:
				print e
				return graph
		else:
			return graph




