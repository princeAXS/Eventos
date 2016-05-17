from eventful import *
from eventbrite import *
from helper import *
import simplejson as json
import psycopg2
import sys





def db_insert(cur,data,con):

    for i in range(len(data)-1):
        #removing non ascii characters which has been added while decoding json into list
        name  = data[i]['name'].encode('utf-8')[0:199]
        description  = data[i]['description'].encode('utf-8')[0:199]
        event_url  = data[i]['event_url'][0:199]
        logo_url  = data[i]['logo_url'][0:199]
        
        #As of now givin source weigtage 1 to every API, Not giving priority to deduplication. Will focus on other functionality
        source = "1"

        
        # if the time is null coming from indvidual scripts then the qoutes should be removed to avoid insert query error

        if len(data[i]['end_time'])>4:
            end_time = "'"+data[i]['end_time']+"'"
            
        else:
            end_time = data[i]['end_time']

            
         
        if len(data[i]['start_time'])>4:
            start_time = "'"+data[i]['start_time']+"'"
        else:
            start_time = data[i]['start_time']
        
        query = "INSERT INTO Events ( eventName, description, logo_url, end_time, start_time, sourceWeightage, eventWebsiteURL, location) VALUES('"+name+"','"+description+"','"+logo_url+"',"+end_time+","+start_time+",'"+source+"','"+event_url+"',"+"ST_GeographyFromText('SRID=4326;POINT("+data[i]['long']+" "+data[i]['lat']+")'))"
   
        cur.execute(query)
            
    con.commit()
    print "Records created successfully";
        
    
        

def main():
    
    #getting data from indvidual event data API
    eventDataEF_json = collectingDataEventFul()
    eventDataEB_json = collectingDataEventBrite()

    # decodeing json into list
    eventDataEF = json.loads(eventDataEF_json)
    eventDataEB = json.loads(eventDataEB_json)


    con = None

    try:

        con = psycopg2.connect(database="eventos", user="eventos", password="12345678", host="eventos.cyeijrrcwqvl.us-west-2.rds.amazonaws.com", port="5590")

        cur = con.cursor()   
        
        #inserting data into DB
        db_insert(cur,eventDataEF['events'],con)
        db_insert(cur,eventDataEB['events'],con)
        



    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)


    finally:

        if con:
            con.close()

if  __name__ =='__main__':main()

