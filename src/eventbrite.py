from urllib2 import Request, urlopen, URLError
import simplejson as json


#api parameters
city = "los angeles"
api_url = "https://www.eventbriteapi.com/v3/events/search/?"
venue_url = "https://www.eventbriteapi.com/v3/venues/"
api_token = "P3T4I4MKKLCNVVOYVTRB"

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

#to remove non ASCII characters
def encoding(string):
    if(string):
        return string.encode('utf-8')
    else:
        return "null"

#checking if a string is null in data api 
def checkNull(string):
    if(string):
        return string
    else:
        return "null"
    
#JSON formation of data collected before any exception    
def collectingDataEventBrite():
        full_data="{"+'"events"'+":["
        
        for ecd in clean_events_data:
            try:
                #converting list into json
                full_data+=ecd.to_JSON()
                full_data+=","
            except TypeError:
                print "-------------abc--------------"
                
                print ecd.name
                print ecd.description
                print ecd.start_time
                print ecd.logo_url
                print ecd.event_url
                print ecd.long
                print ecd.lat
        
        full_data+="{}]}"
        return full_data
        
#URL formation for initial page
request_url = api_url+"venue.city="+city.replace(" ","+")+"&token="+api_token


try:
        #requesting and reading data from API
	request = Request(request_url)
        response = urlopen(request)
	api_data = response.read()
        
        # JSON to list conversion
        json_data = json.loads(api_data)

        
        try:
            page_count = json_data['pagination']['page_count']
        except:
            page_count = 0
            
        request_url+="&page="
        
        #making GET call for each page
        for this_page in range(1,page_count):
            
            # have to make script sleep for an hour as API KEY gets expire after some requests
            if(this_page>0 and this_page%5==0):
                time.sleep(3900)
                
            request = Request(request_url+str(this_page))
            response = urlopen(request)
            api_data = response.read()
            json_data = json.loads(api_data)

            try:
                page_size = json_data['pagination']['page_size']
            except:
                page_size = 0
            for event in range(1,page_size):
                try:
                    name = encoding(checkNull(json_data['events'][event]['name']['text']))
                except:
                    name = encoding(checkNull("none"))
                
                # replacing quotes and slashes from string because it creates problem while inserting data in DB | As of now
                name = name.replace("\\",'');
                name = name.replace("'",'');
                name = name.replace("",'');
                
                
                try:
                    description = checkNull(json_data['events'][event]['description']['text'])
                except:
                    description = checkNull("null")
                # replacing quotes and slashes from string because it creates problem while inserting data in DB | As of now
                description = description.replace("\\",'');
                description = description.replace("'",'');
                description = description.replace('"','');
                
                try:
                    start_time =  json_data['events'][event]['start']['local']
                except:
                    start_time="null"
                try:
                    end_time =  json_data['events'][event]['end']['local']
                except:
                    end_time = "null"
                try:
                    logo_url =  encoding(checkNull(json_data['events'][event]['logo']['url']))
                except:
                    logo_url =  encoding(checkNull("null"))
                try:
                    event_url =  encoding(checkNull(json_data['events'][event]['url']))
                except:
                    event_url =  encoding(checkNull("null"))    
                long=0
                lat=0
                try : 
                    # need to make call to venue API for each event to get LONG and LAT
                    venue_request_url = venue_url+json_data['events'][event]['venue_id']+"/?token="+api_token

                    request = Request(venue_request_url)
                    response = urlopen(request)
                    venue_data = response.read()
                    json_venue_data = json.loads(venue_data)

                    try:
                        long=json_venue_data['longitude']
                    except:
                        long=0
                    try:
                        lat=json_venue_data['latitude']
                    except:
                        lat=0
                    
                except:
                    long="null"
                    lat="null"
                
                # adding each record one by one in class object
                clean_events_data.append(eventData(name,description,event_url,start_time,end_time,logo_url,long,lat))
        
        # if there is no error so far it will return all the acquired data
        collectingDataEventBrite()

except URLError, e:
    print 'No kittez. Got an error code:', e
    #if any error occurs It will return the data whatever has been collected safetly
    collectingDataEventBrite()
    
    
    
    
