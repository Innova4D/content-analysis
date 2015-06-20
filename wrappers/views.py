from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from info_wrappers.foursquare_wrapper import FoursquareWrapper
from info_wrappers.wikipedia_wrapper import WikipediaWrapper
from info_wrappers.web_info import WebInfo
from social_wrappers.facebook_wrapper import FacebookWrapper 
from social_wrappers.twitter_wrapper import TwitterWrapper
from social_wrappers.linkedin_wrapper import LinkedinWrapper
from response_format import ResponseFormat



class PointOfInterest(APIView):
    """
    Get information about a POI using Foursquare, Wikipedia and Web results from Google.
    """


    def __init__(self):
    	'''
    	Initializing Wrappers
    	'''
    	self.foursquare = FoursquareWrapper()
        self.web_info = WebInfo()
        self.format = ResponseFormat()


    def get(self, request, format=None):
        '''
            Gets info about a Point of Interest, it needs exact POI name
            QUERY_PARAMS:
                poi_name: (example: "Museo Amparo") MANDATORY
                city_country: (example: "Puebla, MX") OPTIONAL but highly recommended
                lat_long :(example: "19.04334,-98.20193") OPTIONAL 
        '''
        # Wrappers
        FSW = self.foursquare
        print FSW, type(FSW)
        WI = self.web_info
        print WI, type(WI)

        # Query params
        poi_name = request.QUERY_PARAMS.get('poi_name', u'')
        if not poi_name:
        	return Response('No Point of Interest defined', 
                            status=status.HTTP_400_BAD_REQUEST)
        lat_long = request.QUERY_PARAMS.get('lat_long', u'')
        city_country = request.QUERY_PARAMS.get('city_country', u'Puebla, MX')
        

        print poi_name, type(poi_name)
        print city_country, type(city_country)
        print lat_long, type(lat_long)
        # Retrieving data from wrappers
        if lat_long:
            print 'entering lat_long'
            foursquare_data = FSW.query_lat_long(poi_name, lat_long, limit=1)
        else:
            print 'entering city_country'
            foursquare_data = FSW.query_place(poi_name, city_country, limit=1)
        print foursquare_data

        web_data = WI.get_data(poi_name)
        print web_data
        # Response
        res = self.format.poi_format(poi_name,foursquare_data, web_data)
        return Response(res, status=status.HTTP_200_OK)



class User(APIView):
    '''
        Get information from user from Facebook and Twitter 
    '''


    def __init__(self):
        '''
            Initializing wrappers
        '''
        self.twitter = TwitterWrapper()
        self.format = ResponseFormat()


    def get(self, request, format=None):
        '''
            Gets info about a User, it needs Facebook permision token
            QUERY_PARAMS:
                facebook_token:  (example: 'Axoaoxoxox...soj7ZD') MANDATORY
                twitter_account: (example: "@username") OPTIONAL but highly recommended 
        '''
        # Wrappers
        TW = self.twitter
        facebook_token = request.QUERY_PARAMS.get('facebook_token', '')
        print facebook_token, type(facebook_token)
        FW = FacebookWrapper(facebook_token)

        # Query params
        twitter_account = request.QUERY_PARAMS.get('twitter_account', '')

        # Retrieving data from wrappers
        facebook_data = FW.get_user_profile()
        print type(facebook_data)
        twitter_data = TW.get_user_profile(twitter_account)
        print twitter_data

        # Response
        res = self.format.user_format(facebook_data, twitter_data)
        return Response(res, status=status.HTTP_200_OK)



class Foursquare(APIView):
    '''
        Get information from Foursquare Wrapper
    '''


    def __init__(self):
        '''
            Initializing Foursquare Wrapper
        '''
        self.foursquare = FoursquareWrapper()


    def get(self, request, format=None):
        '''
            Gets info about using foursquare data
            QUERY_PARAMS:
                query: (example: "Museo Amparo") OPTIONAL
                city_country: (example: "Puebla, MX") MANDATORY if not lat_long
                lat_long:(example: "19.04334,-98.20193") MANDATORY if not city_country
                category: (example: "Museo de Arte") OPTIONAL
                category_lang: ('en' or 'es') allowed OPTIONAL
        '''
       # Wrapper
        FSW = self.foursquare

        # Query params
        query = request.QUERY_PARAMS.get('query', u' ')
        lat_long = request.QUERY_PARAMS.get('lat_long', u'')
        city_country = request.QUERY_PARAMS.get('city_country', u'')
        category = request.QUERY_PARAMS.get('category', u'')
        category_lang = request.QUERY_PARAMS.get('category_lang', u'es')

        # Retrieving info from foursquare
        if lat_long:
            print 'entering lat_long'
            foursquare_data = FSW.query_lat_long(query, lat_long, 
                                                 category=category, 
                                                 category_lang=category_lang, 
                                                 limit=20)
        elif city_country:
            print 'entering city_country'
            foursquare_data = FSW.query_place(query, city_country,
                                              category=category, 
                                              category_lang=category_lang, 
                                              limit=20)
        else:
            return Response ('No city_country or lat_long provided',
                              status=status.HTTP_400_BAD_REQUEST)

        #Response
        return Response(foursquare_data, status=status.HTTP_200_OK)



class WebData(APIView):
    '''
        Gets info using Google web results

    '''


    def __init__(self):
        '''
            Initializing
        '''
        self.web_info = WebInfo()


    def get(self, request, format=None):
        '''
        QUERY_PARAMS:
            query: (example: "Museo Amparo") MANDATORY  
        '''
        # Query params
        query = request.QUERY_PARAMS.get('query', u' ')       

        web_data = self.web_info.get_data(query)

        return Response(web_data, status=status.HTTP_200_OK)



class Facebook(APIView):
    '''
        Gets info from a facebook user
    '''


    def __init__(self):
        pass


    def get(self, request, format=None):
        '''
        QUERY_PARAMS:
            facebook_token:  (example: 'Axoaoxoxox...soj7ZD') MANDATORY
            profile: boolean default (True)
            posts: boolean
            friends: boolean
            likes: boolean
        '''
        # Initializing wrapper
        facebook_token = request.QUERY_PARAMS.get('facebook_token', '')
        FW = FacebookWrapper(facebook_token)

        # Query params
        profile = request.QUERY_PARAMS.get('profile', 1)
        posts = request.QUERY_PARAMS.get('posts', 0)
        friends = request.QUERY_PARAMS.get('friends', 0)
        likes = request.QUERY_PARAMS.get('likes', 0)

        # Retrieving info
        if profile:
            user_profile = FW.get_user_profile()
        else:
            user_profile = {}
        if posts:
            user_posts = FW.get_user_posts()
        else:
            user_posts = []
        if friends:
            user_friends = FW.get_user_friends()
        else:
            user_friends = []
        if likes:
            user_likes = FW.get_user_likes()
        else:
            user_likes = []

        # Response
        res = {'profile': user_profile, 'posts': user_posts,
               'friends': user_friends, 'likes': user_likes}
        return Response(res, status=status.HTTP_200_OK)



class Twitter(APIView):
    '''
        Gets info from a twitter account
    '''


    def __init__(self):
        self.twitter = TwitterWrapper()


    def get(self, request, format=None):
        '''
        QUERY_PARAMS:
            twitter_account:  (example: '@username') MANDATORY
            profile: boolean default (True)
            tweets: boolean
            friends: boolean
            followers: boolean
        '''
        # Initialized wrapper
        TW = self.twitter

        # Query params
        username = request.QUERY_PARAMS.get('twitter_account', ' ')
        profile = request.QUERY_PARAMS.get('profile', 1)
        tweets = request.QUERY_PARAMS.get('tweets', 0)
        friends = request.QUERY_PARAMS.get('friends', 0)
        followers = request.QUERY_PARAMS.get('followers', 0)

        # Retrieving info
        if profile:
            user_profile = TW.get_user_profile(username)
        else:
            user_profile = {}
        if tweets:
            user_tweets = TW.get_user_tweets(username)
        else:
            user_tweets = []
        if friends:
            user_friends = TW.get_friends(username)
        else:
            user_friends = []
        if followers:
            user_followers = TW.get_followers(username)
        else:
            user_followers = []

        # Response
        res = {'profile': user_profile, 'tweets': user_tweets,
               'friends': user_friends, 'followers': user_followers}
        return Response(res, status=status.HTTP_200_OK)  



class Linkedin(APIView):
    '''
        Gets info from linkedin data
    '''


    def __init__(self):
        '''
            Initializing
        '''
        self.linkedin = LinkedinWrapper()


    def get(self, request, format=None):
        '''
        QUERY_PARAMS:
            name: full name of the person to search for (MANDATORY if not keywords)
            keywords: comma separated words associated with person (MANDATORY if not name)
        '''
        # Wrapper
        LW = self.linkedin

        # Query params
        username = request.QUERY_PARAMS.get('person_name', ' ')
        keywords = request.QUERY_PARAMS.get('keywords', '')

        # Retrieving info
        linkedin_data = LW.search_people([username] + keywords.split(','))

        # Response
        return Response(linkedin_data, status=status.HTTP_200_OK)


class Wikipedia(APIView):
    '''
        Gets info from wikipedia pages
    '''

    def __init__(self):
        '''
            Initializing
        '''
        self.wikipedia = WikipediaWrapper()



    def get(self, request, format=None):
        '''
        QUERY_PARAMS
            query: string
        '''
        WW = WikipediaWrapper()
        query = request.QUERY_PARAMS.get('query', '')

        wikipedia_data = WW.search(query)

        return Response(wikipedia_data, status=status.HTTP_200_OK)





