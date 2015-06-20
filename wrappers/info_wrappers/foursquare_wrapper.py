#Created by: Esteban castillo 
#links related:
#https://developer.foursquare.com/docs/venues/search
#Pagina Wrapper github: https://github.com/mLewisLogic/foursquare
#pip install foursquare


"""Structure of the returned json:


{
 "query": "text",
 "place": "text",
 "POI_1":
  {
    "category": "text",
    "name": "text",
    "description": text,
    "latitude": "decimal number",
    "longitud": "decimal number",
    "country": "text",
    "state": "text",
    "city": "text",
    "address": "text",
    "phone": "text",
    "url": "text",
    "comments": python list of comments,
    "statistics":
      {
        "rating": int,
        "checkinsCount": int,
        "usersCount": int
        "popularity": int
      }    
  },

  ...
  
 "POI_N":
  {
    "categorie": "text",
    "name": "text",
    "description": text,
    "latitude": "decimal number",
    "longitud": "decimal number",
    "country": "text",
    "state": "text",
    "city": "text",
    "address": "text",
    "phone": "text",
    "url": "text",
    "comments": python list of comments,
    "statistics":
      {
        "rating": int
        "checkinsCount": int
        "usersCount": int
        "popularity": int
      }    
  }
}
  
"""
from __future__ import division
from math import log10
import unicodedata
import foursquare
import codecs
import json
import os

class FoursquareWrapper():


    #Foursquare tokens, used to connect with the API
    CLIENT_ID="XJFEN52URK1N1D2WZDBPKNCJICMNZCZYQPULR2XF31K1BJB2"
    CLIENT_SECRET="3NN4ESQ0YUBCRYG0KBX4JPZAWFPYMLCC44ZSSWVFOZJAUVX4"
    client=None
    result_Json=None
    CATEGORIES = {}
    BASE_DIR = os.path.dirname(__file__)

    with open(BASE_DIR + '/jsons/CategoriesTranslated.json', 'r') as f:
             CATEGORIES = json.loads(f.read())


    def __init__(self):
      """Constructor, used to initialize the atributes of the class Foursquare"""
      try:

             self.client = foursquare.Foursquare(self.CLIENT_ID, self.CLIENT_SECRET)
      except:
             description={"error":"initialization failure, Could not instantiate the Foursquare wrapper"}
             return description   


    def category_mapper(self,category,language='es'):
        """Function to map english to spanish categories

         Keyword arguments:
           category -- name of category
           language -- language 'en' or 'es'
           
         Return:
          Foursquare ID of the category

        """
        if language == 'es':
             with open(self.BASE_DIR + '/jsons/FoursquareCategoriesTranslated.json', 'r') as f:
                  dictionary = json.loads(f.read())
             try:
                return dictionary[category.title()]
             except KeyError as e:
                print "No category found"
                return ""
        if language == 'en':
             with open(self.BASE_DIR + '/jsons/FoursquareCategories.json', 'r') as f:
                dictionary = json.loads(f.read())
             try:
                return dictionary[category.title()]
             except KeyError as e:
                print "No category found"
                return ""
        else:
             return ""


    def iterate_dictionary(self,dictionary):
        """Function used to extract the information of a POI

         Keyword arguments:
           dictionary -- information extracted of Foursquare API
           
         Return:
          Json with the POIS obtained

        """
        try:
                if "venues" in dictionary:
                    places=dictionary["venues"]

                    counter=1
                    for x in places:
                       result_POI={}
                       
                       #get the category of the POI
                       
                       if "name" in x["categories"][0]:
                            category=x["categories"][0]["name"]
                            result_POI["category"] = u""+self.CATEGORIES[category]
                       else:    
                            result_POI["category"]=u""

                       #get the name of the POI     

                       if "name" in x:
                            result_POI["name"]=u""+x["name"]
                       else:
                            result_POI["name"]=u""

                       #get the latitude of the POI      
                       if "lat" in x["location"]:
                           result_POI["latitude"]=unicode(x["location"]["lat"])
                       else:
                           result_POI["latitude"]=u""
                           
                       #get the longitud" of the POI
                       if "lng" in x["location"]:
                           result_POI["longitud"]= unicode(x["location"]["lng"])
                       else:
                           result_POI["Longitud"]=u""

                       #get the country of the POI                          

                       if "country" in x["location"]:
                           result_POI["country"]= u""+x["location"]["country"]
                       else:
                           result_POI["country"]=u""

                       #get the state of the POI     

                       if "state" in x["location"]:
                           result_POI["state"]= u""+x["location"]["state"]
                       else:
                           result_POI["state"]=u""    

                       #get the city of the POI 
                       if "city" in x["location"]:
                           result_POI["city"]= u""+x["location"]["city"]
                       else:
                           result_POI["city"]=u""        

                       #get the address of the POI 
                       if "address" in x["location"]:
                           result_POI["address"]= u""+x["location"]["address"]
                       else:
                           result_POI["address"]=u""     

                       #get the phone of the POI
                       if "phone" in x["contact"]:
                           result_POI["phone"]= unicode(x["contact"]["phone"])

                       else:
                           result_POI["phone"]=u""    

                       #get the url of the POI
                       if "url" in x:
                           result_POI["url"]= unicode(x["url"])

                       else:
                           result_POI["url"]=u""    

                       result_POI_Statistics={}

                       #get all the Statistics of a POI

                       if "checkinsCount" in x["stats"]:
                           result_POI_Statistics["checkinsCount"]= x["stats"]["checkinsCount"]
                       else:
                           result_POI_Statistics["checkinsCount"]=0    

                       if "usersCount" in x["stats"]:
                           result_POI_Statistics["usersCount"]= x["stats"]["usersCount"]
                       else:
                           result_POI_Statistics["usersCount"]=0

                       # Arbitrary popularity measure
                       users_count = result_POI_Statistics["usersCount"]
                       checkins_count = result_POI_Statistics["checkinsCount"]
                       print (users_count + checkins_count + 1)  / 5
                       popularity = 2 + log10((users_count + checkins_count + 1)  / 5)
                       result_POI_Statistics["popularity"] = popularity

                       details= self.client.venues(x["id"])

                       if "venue" in details:
                         detail_place=details["venue"]

                         #get the rating(provided by Foursquare) of the POI
                         if "rating" in detail_place:
                           result_POI_Statistics["rating"] = detail_place["rating"]
                         else:
                           result_POI_Statistics["rating"] = 0                        
                           
                         if  "tips" in  detail_place:
                             if "groups" in detail_place["tips"]:
                                 if "items" in detail_place["tips"]["groups"][0]:
                                     contador=0
                                     list_comments=[]
                                     for x in detail_place["tips"]["groups"][0]["items"]:
                                         if "text" in x:
                                             if contador!=0:
                                                #get all the associated comments of a POI
                                                list_comments.append(x["text"])
                                             contador=1

                                 result_POI["statistics"]= result_POI_Statistics
                                 result_POI["comments"]= list_comments
                                 
                                 if "items" in detail_place["tips"]["groups"][0]:
                                    if len(detail_place["tips"]["groups"][0]["items"])>0:
                                        #get the description of a POI
                                         result_POI["description"]= u""+detail_place["tips"]["groups"][0]["items"][0]["text"]
                                    else:     
                                         result_POI["description"]=u""

                       self.result_Json["POI_"+unicode(counter)]=result_POI
                       counter=counter+1

                    return self.result_Json
                else:
                    description={"warning":"no results for this query"}
                    return description
        except Exception as e:
                print e          
                return {}


    def query_place(self,query,place,category="",category_lang='es',limit=50):
        """Function used to get all the information about a POI (using a standard query)

         Keyword arguments:
           query -- String about a topic to search
           place -- String about a place
           category -- Type of POI, example: "4d4b7104d754a06370d81259" (Arts & Entertainment)
           limit -- Number of results to return(must not exceed 50 Results)

         Return:
          Json with the POIS obtained

        """
        try:

             if isinstance(query, unicode) and isinstance(place, unicode) and isinstance(limit, int):
                self.result_Json={} 
                str_query = unicodedata.normalize('NFKD', query).encode('ascii','ignore')
                text_category=self.category_mapper(category,category_lang)
                if text_category=="":
                    result = self.client.venues.search(params={'query': str_query,'near':place ,'limit':limit})
                else:
                    result = self.client.venues.search(params={'query': query,'near':place ,'categoryId': text_category,
                                                               'limit':limit})
                self.result_Json["query"]=query
                self.result_Json["place"]=place

                return self.iterate_dictionary(result)
                    
             else:
                 description={"error":"Failed query, any of the input parameters is incorrect"}
                 return description
            
        except Exception as e:
             print e         
             description={"error":"Failed query, could not search on the Foursquare wrapper"}
             return description

             

    def query_lat_long(self,query,lat_long,category="",category_lang='es',radius=1000,limit=50):
        """Function used to get all the information about a POI (using lat, long and radius)
         Keyword arguments:
           query -- String about a topic to search
           lat_long -- Latitude and longitud about a place in decimal format, example: '19.04334,-98.20193'
           limit --  Number of results to return(must not exceed 50 Results)
           radius -- Limit results to venues within this many meters of the specified location
                    (The maximum supported radius is currently 100,000 meters).

         Return:
          Json with the POIS obtained

        """
        try:

             if isinstance(query, unicode) and isinstance(lat_long, unicode) and isinstance(limit, int) and isinstance(radius, int):
                self.result_Json={} 
                str_query = unicodedata.normalize('NFKD', query).encode('ascii','ignore')
                text_category = self.category_mapper(category,category_lang )
                if text_category=="":
                    result = self.client.venues.search(params={'query': str_query,'ll': lat_long,'radius': radius,
                                                               'limit': limit})
                else:
                    result = self.client.venues.search(params={'query': query,'ll': lat_long,'radius': radius,
                                                               'categoryId': text_category,'limit': limit})
                self.result_Json["query"]=query
                self.result_Json["place"]=place
                return self.iterate_dictionary(result)
             else:
                 description={"error":"Failed query, any of the input parameters is incorrect"}
                 return description           
        except:
             description={"error":"Failed query, could not search on the Foursquare wrapper"}
             return description

