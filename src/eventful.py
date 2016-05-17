from urllib2 import Request, urlopen, URLError
import simplejson as json


#api parameters
city = "los angeles"
api_url = "http://api.eventful.com/json/events/search?"
api_token = "96MwLvP5qM2g3Xfx"

#data container which will collect the temporary data before JSON formation
clean_events_data = []

class eventData(object):
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __init__(self,name="none",description="none",event_url="none",start_time="none",end_time="none",logo_url="none",long="null",lat="null"):
        self.name=name
        self.description=description
        self.event_url=event_url
        self.start_time=start_time
        self.end_time=end_time
        self.logo_url=logo_url
        self.long=long
        self.lat=lat
        
#JSON formation of data collected before any exception
def collectingDataEventFul():
        full_data="{"+"\"events\""+":["
        
        for ecd in clean_events_data:
            try:
                #converting list into json
                full_data+=ecd.to_JSON()
                full_data+=","
            except TypeError:
              
                print ecd.name
                print ecd.description
                print ecd.start_time
                print ecd.logo_url
                print ecd.event_url
                print ecd.long
                print ecd.lat
        
        full_data+="{}]}"
        return full_data
        
         
#checking if a string is null in data api 
def checkNull(string):
    if(string):
        return string
    else:
        return "null"
    
#to remove non ASCII characters
def encoding(string):
    if(string):
        return string.encode('utf-8')
    else:
        return "null"

#URL formation for initial page
request_url = api_url+"location="+city.replace(" ","+")+"&app_key="+api_token

try:
        #requesting and reading data from API
	request = Request(request_url)
        response = urlopen(request)
	api_data = response.read()
        
        # JSON to list conversion
        json_data = json.loads(api_data)

        
        try:
            page_count = int(json_data['page_count'])
        except:
            page_count = 0
            
        request_url+="&page="
        
        #making GET call for each page 
        for this_page in range(1,page_count):
            
            
            request = Request(request_url+str(this_page))
            response = urlopen(request)
            api_data = response.read()
            json_data = json.loads(api_data)
            
            try:
                page_size = int(json_data['page_size'])
            except:
                page_size = 0
            for event in range(1,page_size):
                try:
                    name = encoding(checkNull(json_data['events']['event'][event]['title']))
                except:
                    name = encoding(checkNull("null"))
                
                # replacing quotes and slashes from string because it creates problem while inserting data in DB | As of now
                name = name.replace("\\",'');
                name = name.replace("'",'');
                name = name.replace("",'');
                
                try:
                    description = encoding(checkNull(json_data['events']['event'][event]['description']))
                except:
                    description = encoding(checkNull("none")) 
                
                # replacing quotes and slashes from string because it creates problem while inserting data in DB | As of now
                description = description.replace("\\",'');
                description = description.replace("'",'');
                description = description.replace('"','');
               
                
                try:
                    start_time =  json_data['events']['event'][event]['start_time']
                except:
                    start_time="null"
                    
                try:
                    end_time =  checkNull(json_data['events']['event'][event]['stop_time'])
                except:
                    end_time="null"
                     
                try:
                    logo_url =  json_data['events']['event'][event]['image']['medium']['url']
                except:
                    logo_url =  encoding(checkNull("null"))
                
                #removing spaces from URLs appended in the beginning
                logo_url = logo_url.replace(" ","")
                
                try:
                    event_url = encoding(checkNull(json_data['events']['event'][event]['url']))
                except:
                    event_url = encoding(checkNull("none")) 
                #removing spaces from URLs appended in the beginning
                event_url = event_url.replace(" ","")
                
                try:
                    long = encoding(checkNull(json_data['events']['event'][event]['longitude']))
                except:
                    long = encoding(checkNull("null")) 
                    
                try:
                    lat = encoding(checkNull(json_data['events']['event'][event]['latitude']))
                except:
                    lat = encoding(checkNull("null")) 
                
                # adding each record one by one in class object
                clean_events_data.append(eventData(name,description,event_url,start_time,end_time,logo_url,long,lat))
        
        # if there is no error so far it will return all the acquired data
        collectingDataEventFul()
            
except URLError, e:
    print 'No kittez. Got an error code:', e
    #if any error occurs It will return the data whatever has been collected safetly
    collectingDataEventFul()
    