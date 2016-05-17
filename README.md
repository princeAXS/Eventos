"EVENTOS"

Project Description

The project is to build a client server application which will help
users to find out events happening near them in a particular area (decided on the
basis of fence creation).


Features of the Project

1. The user will be able to create fences at different locations.
2. As user enters the fence, he will be able to see the upcoming events happening around him in the area enclosed by the fence.
3. The upcoming events will be displayed on the basis of proximity to the user.
4. On clicking the particular event from the list, the user will be able to see the details of the event.
5. Details of the event would include time of the event, date of the event, location of the event, category of the event (if available).
6. User can write reviews about a particular event.
7. As the user clicks on the event, the app will also navigate him to the particular event location.
8. User will be able to delete his/her private fences if he wants to.
9. User will be able to view all the fences created by him.
10. App will show all the fences while the user creating/ editing a new fence if he wants to.


Upcoming Features

1. User will be able to check in at a particular event through Facebook.
2. As soon as the user enters the fence, he will be notified about all the events happening in that fence even if the app on the user’s mobile is not open.

TECHNICAL OVERVIEW

Client-Side: Android
1. The user will be able to sign in into the app if the user already has an account on the app.
2. If however, the user does not have the account, he will be prompted to create the account.
3. The user will be able to see the total number of fences and the location of different fences.
4. There will be a create button on the app which will allow the user to create a new fence.
5. If the user clicks on the already created fence, he will see a pop up that will have two options to delete or edit the fence.
6. Once the user creates the fence, he will be asked to save the fence and give the confirmation in terms of an alert box which will have two clicks ‘ok’ or ‘cancel’.

Server-Side:
1. Web server will be getting the data from multiple API’s and storing it in a spatial database server.
2. The web server will be getting data from database and convert the data into JSON.
3. The JSON data will be fetched by Android using an API call

Details of code files

/ In src folder

-Individual Python scripts(eventbrite.py and eventful.py) to get required data(i.e event name, description, long and lat, start_time, end_time, event_url, logo_url) from multiple event data API(i.e eventbrite, eventful).These scripts will do cleaning and mapping of data parameters.

-Core python script(eventos.py) to import data(json formatted) which have been extracted from individual python scripts, implement de-duplication of events records(on the factor if two events have same time and location then its redundant) and then the final step is to insert all the events records to DB( (postgre + postgis) host on amazon RDS).

-Crons.py file to do get latest data from API and update DB by running above python scripts in every 24 hours.

-sample json data file(eventbrite_data.json, eventful_data.json) which contains data that can be extracted from individual python scripts.

-please ignore .pyc files and helper files(they are for debug purposes)



/ In php_src folder

-php script(a.php) to create a data api for clients.

-methods
 * API URL, endpoints and methods have been specified .
 * A field selector is a important param in every call to data api.
 * Selector has different value for different VALUE FOR different tasks.for eg: Selector =1 will perform user signup, 2 will perform user login and so on
 * For every call it will return json data with a by default params such as success(which will represent if any operation on data api was a success or not. Value will be True and false) and error message(which will represent what went wrong during the operation on API)
 for more details pls read php_src/methods file

- eventos folder is to deploy php application to AWS. make any chances in a.php then copy code from a.php to eventos/index.php. compress the folder and upload to AWS. After successfully uploading deploy the last uploaded application.

/ In lib folder

- SQL queries to create tables and insert queries with sample data in db lies in 587sqlcommands.text
- logs.rtf represents data that can be achieved from python scripts at every steps
