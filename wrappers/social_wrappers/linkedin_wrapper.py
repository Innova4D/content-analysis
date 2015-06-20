#Created by: Esteban castillo

from linkedin import linkedin #pip install python-linkedin
from oauthlib import *
import math
import codecs
import json


"""Structure of the returned json:


{
 "query": "text",

 "Person_1":
  {
    "publicProfileUrl": "text"
    "location":  "text",
    "firstName": "text",
    "lastName":  "text",
    "industry":  "text",
    "headline":  "text",
    "summary":   "text" 
  },

  ...
  
 "Person_N":
  {
    "publicProfileUrl": "text"
    "location":  "text",
    "firstName": "text",
    "lastName":  "text",
    "industry":  "text",
    "headline":  "text",
    "summary":   "text" 
  }
}
  
"""


class LinkedinWrapper:

    #Linkedin tokens, used to connect with the API
    CONSUMER_KEY='7ttzk2irt03s'
    CONSUMER_SECRET='wXUI0ElymQ0DX9Yc'
    USER_TOKEN='9dc20491-aca5-41df-a5f8-e6c8f8801fa6'
    USER_SECRET='5b75220e-46fe-4185-941b-6985e76600eb'
    RETURN_URL=''
    result_Json=None
    
    """Constructor, used to initialize the atributes of the class Foursquare"""
    def __init__(self):
        self.auth = linkedin.LinkedInDeveloperAuthentication(self.CONSUMER_KEY, self.CONSUMER_SECRET, 
                                self.USER_TOKEN, self.USER_SECRET, 
                                self.RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())
        self.app = linkedin.LinkedInApplication(self.auth)
        



    """Function used to get all the information about a Person (using a list of elements related to the search)
     Keyword arguments:
       query -- Python list of elements related
     Return:
      Json with the Persons obtained

    """


    def search_people(self,query):
        
      try:
          if isinstance(query, list):
                selectors=[{'people': ['first-name', 'last-name',"headline","industry","location","summary","public-profile-url"]}]
                params={}
                params["keywords"]=query;
                params["start"]=0
                params["count"]=20
                result=self.app.search_profile(selectors,params)
                numResult=result["people"]["_total"]
                counter=1
                self.result_Json={}
                self.result_Json["query"]=query
                # no associated results were found in the search
                if (numResult==0):  
                    descripcion={"error":"No associated results were found in the API search"}
                    return descripcion
                
                # there are search results and the page rank covers all values
                elif(numResult >0 and numResult <= 20):
                    for x in  result["people"]["values"]:
                         result_Person={}
                         #get the firstName of the person
                         if "firstName" in x:
                             result_Person["firstName"]=x["firstName"]
                         else:
                             result_Person["firstName"]=""
                             
                         #get the lastName of the person    
                         if "lastName" in x:
                             result_Person["lastName"]=x["lastName"]
                         else:
                             result_Person["lastName"]=""

                         #get the headline of the person
                         if "headline" in x:
                             result_Person["headline"]=x["headline"]
                         else:
                             result_Person["headline"]="" 

                         #get the name of the industry where the person works
                         if "industry" in x:
                             result_Person["industry"]=x["industry"]
                         else:
                             result_Person["industry"]=""  

                         #get the publicProfileUrl of the person
                         if "publicProfileUrl" in x:
                             result_Person["publicProfileUrl"]=x["publicProfileUrl"]
                         else:
                             result_Person["publicProfileUrl"]=""
                             
                         #get the name of the place where the person lives
                         if "location" in x:
                             result_Person["location"]=x["location"]["name"]
                         else:
                             result_Person["location"]=""
                             
                         #get a brief description of the person
                         if "summary" in x:
                            descripcion=x["summary"]
                            result_Person["summary"]=(descripcion.replace("\n", "")).replace("\r","")
                          
                         else:
                            result_Person["summary"]=""

                         self.result_Json["Person_"+str(counter)]=result_Person
                         counter=counter+1
                    return self.result_Json
                    
                # there are search results and the page rank not covers all values                
                else:
                        for x in range(0, numResult, 20):
                          if x <= 60:
                            params["start"]=x
                            params["count"]=20
                            result2=self.app.search_profile(selectors,params)
                            for x in result2["people"]["values"]: 
                                 result_Person={}
                        
                                 if "firstName" in x:
                                     result_Person["firstName"]=x["firstName"]
                                 else:
                                     result_Person["firstName"]=""  

                                 if "lastName" in x:
                                     result_Person["lastName"]=x["lastName"]
                                 else:
                                     result_Person["lastName"]=""  

                                 if "headline" in x:
                                     result_Person["headline"]=x["headline"]
                                 else:
                                     result_Person["headline"]=""  

                                 if "industry" in x:
                                     result_Person["industry"]=x["industry"]
                                 else:
                                     result_Person["industry"]=""

                                 if "publicProfileUrl" in x:
                                     result_Person["publicProfileUrl"]=x["publicProfileUrl"]
                                 else:
                                     result_Person["publicProfileUrl"]=""  

                                 if "location" in x:
                                     result_Person["location"]=x["location"]["name"]
                                 else:
                                     result_Person["location"]="" 

                                 if "summary" in x:

                                     descripcion=x["summary"]
                                     result_Person["summary"]=(descripcion.replace("\n", "")).replace("\r","")
                                 else:
                                     result_Person["summary"]=""

                                 self.result_Json["Person_"+str(counter)]=result_Person
                                 counter=counter+1    
                        return self.result_Json
          else:
                 descripcion={"error":"Failed query, any of the input parameters is incorrect"}
                 return descripcion
      except:
             descripcion={"error":"Failed query, could not search on the Linkedin wrapper"}
             return descripcion


