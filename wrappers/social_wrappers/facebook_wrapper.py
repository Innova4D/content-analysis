from datetime import datetime, date
import facebook
import logging as log



# Facebook access tokens should be provided on the initialization of the
# FacebookWrapper class.
# For details see:
# https://developers.facebook.com/docs/facebook-login/access-tokens

class FacebookWrapper():


	log.basicConfig(filename='facebook.log', 
					format='%(asctime)s, %(levelname)s: %(message)s',
					level=log.DEBUG)


	def __init__(self, oauth_access_token):
		'''
			oauth_access_token: string 
		'''
		self.facebook_graph = facebook.GraphAPI(oauth_access_token)


	def simple_fql_query(self, SELECT, FROM, WHERE):
		'''
			Create a simple fql query 
			SELECT message FROM status WHERE uid = me()
			SELECT: list of elemenets to retrieve
			FROM: table in https://developers.facebook.com/docs/reference/fql
			WHERE: condition
		'''
		_select = "" 
		for s in SELECT:
			_select = _select + ' ' + s + ','
		_select = _select[:-1]
		return 'SELECT ' + _select +' FROM ' + FROM + ' WHERE ' + WHERE


	def get_user_posts_fql(self):
		'''
			Get user post using Facebook Query Language
			This method is still valid for GraphAPI v2.2 and earlier versions
		'''
		facebook_graph = self.facebook_graph
		q = self.simple_fql_query(['message', 'time', 'status_id'], 'status', 'uid = me()')
		try:
			user_posts = facebook_graph.fql(q)
		except Exception as e:
			log.exception(e)
			return e[0]
		list = []
		try:
			for p in user_posts:
				post = {}
				post['id'] = p['status_id']
				post['text'] = p['message']
				post['date'] = datetime.fromtimestamp(p['time']).strftime('%Y-%m-%d %H:%M:%S')
				list.append(post)
		except KeyError as e:
			log.warning('Acces Token or User has not the following info: %s', e)
			return "Access Token or User has not the following info: 'statuses'"
		return list


	def get_user_posts(self):
		'''
			Get user post using GraphAPI - GET method
		'''
		try:
			user_posts = self.facebook_graph.get_object('me', fields='statuses')
			list = []
			try:
				for p in user_posts['statuses']['data']:
					post = {}
					post['id'] = p['id']
					post['text'] = p['message']
					post['date'] = p['updated_time']
					list.append(post)
			except KeyError as e:
				log.warning('Access Token or User has not the following info: %s', e)
				return "Access Token or User has not the following info: 'statuses'"
		except Exception as e:
			log.exception(e)
			return e[0]
 		if list:
 			return list
 		else:
 			log.warning("Access Token or User has not the following info: 'posts'")
 			return "Access Token or User has not the following info: 'posts'"


	def get_user_profile(self):
		'''
			Get user profile using GraphAPI - GET method
		'''
		facebook_graph = self.facebook_graph
		user = {}
		try:
			user_profile = facebook_graph.get_object('me')
			user['name'] = user_profile['name']
			user['gender'] = user_profile['gender']
			user['id'] = user_profile['id']
			user['lang'] = user_profile['locale'][:2]
			ext_user_profile = facebook_graph.get_object('me', 
														 fields=['birthday', 
														 'location', 'bio',
														 'quotes'])
		except Exception as e:
			log.exception(e)
			return e[0]
		try:
			user['birthday'] = ext_user_profile['birthday']
			y = user['birthday'].split('/')[2]
			m = user['birthday'].split('/')[0]
			d = user['birthday'].split('/')[1]
			birthdate = date(int(y), int(m), int(d)).toordinal()
			today = date.today().toordinal()
			user['age'] = (today - birthdate) / 365
		except KeyError as e:
			log.warning('Access Token or User has not the following info: %s', e)
			user[e[0]] = ''
			user['age'] = ''
		try:
			user['bio'] = ext_user_profile['bio']
		except KeyError as e:
			log.warning('Access Token or User has not the following info: %s', e)
			user[e[0]] = ''
		try:
			user['quotes'] = ext_user_profile['quotes']
		except KeyError as e:
			log.warning('Access Token or User has not the following info: %s', e)
			user[e[0]] = ''
		try:
			user['location'] = ext_user_profile['location']['name']
		except KeyError as e:
			log.warning('Access Token or User has not the following info: %s', e)
			user[e[0]] = ''

		return user


	def get_user_friends(self):
		'''
			Get user friends using GraphAPI - GET method
		'''
		facebook_graph = self.facebook_graph
		try:
			user_friends = facebook_graph.get_connections(id='me', 
													  connection_name='friends',
									   				  fields=['gender','name'])
			list = []
			try:
				for friend in user_friends['data']:
					list.append(friend)
			except KeyError as e:
				log.warning(e)
				return e[0]
		except Exception as e:
			log.exception(e)
			return e[0]
 		if list:
 			return list
 		else:
 			log.warning("Access Token or User has not the following info: 'friends'")
 			return "Access Token or User has not the following info: 'friends'"


	def get_user_likes(self):
		'''
			Get user likes using GraphAPI - GET method
		'''
		try:
 			user_likes = self.facebook_graph.get_connections(id='me', 
 														 connection_name='likes',
 														 fields='', limit=1000)
 			list = []
	 		try:
	 			for like in user_likes['data']:
	 				likes = {}
	 				likes['category'] = like['category']
	 				likes['name'] = like['name']
	 				list.append(likes)
	 		except KeyError as e:
	 			log.warning(e)
	 			return e[0]
	 	except Exception as e:
 			log.exception(e)
 			return e[0]
 		if list:
 			return list
 		else:
 			log.warning("Access Token or User has not the following info: 'likes'")
 			return "Access Token or User has not the following info: 'likes'"


 	def generate_user_graph(self, graph):
 		'''
	 		Generate facebook user graph. 
	 		In order to use this method a graph object is needed with two methods: 
	 		add_node(node) and add_edge(node_1, node_2)
 		'''
 		me = self.get_user_profile()['name']
 		graph.add_node(me)
 		friends = self.get_user_friends()
 		for friend in friends:
 			graph.add_node(friend['name'])
 			graph.add_edge(me, friend['name'])
 		return graph

