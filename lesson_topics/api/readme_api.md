## Connecting to API

https://opendata.transport.nsw.gov.au/user-guide
https://opendata.transport.nsw.gov.au/get-started
https://opendata.transport.nsw.gov.au/documentation
https://opendata.transport.nsw.gov.au/api-basics


## Suggested APIs

Timetables and routes
https://opendata.transport.nsw.gov.au/dataset/public-transport-timetables-realtime/resource/9b3bfa13-0053-4008-8575-e30151f05d54

Changed schedules
https://opendata.transport.nsw.gov.au/dataset/public-transport-realtime-trip-update

Realtime vehicles positions
https://opendata.transport.nsw.gov.au/dataset/public-transport-realtime-vehicle-positions
trains: https://opendata.transport.nsw.gov.au/dataset/public-transport-realtime-vehicle-positions-v2

Historical position for ferries and metro
https://opendata.transport.nsw.gov.au/dataset/historical-gtfs-and-gtfs-realtime

### GTFS worked example

https://medium.com/@bhaveshpatelaus/gtfs-realtime-vehicle-positions-using-python-and-databricks-tfnsw-a33b98f22e97


Read this second: https://opendata.transport.nsw.gov.au/developer-information
https://opendata.transport.nsw.gov.au/how-use-open-data-develop-application

https://opendata.transport.nsw.gov.au/developers/api-explorer

### Adding the netskope certificate

https://levelup.gitconnected.com/solve-the-dreadful-certificate-issues-in-python-requests-module-2020d922c72f
https://stackoverflow.com/questions/30405867/how-to-get-python-requests-to-trust-a-self-signed-ssl-certificate

## Adding the certificate to a request

open Chrome
go to https://opendata.transport.nsw.gov.au/node/9582/exploreapi
Click on the padlock icon
Select the top certificate in the list (netskope)
Click ("Export")
Save the file somewhere
Refer to this file in the request verify='C:\\repos\\advanced_python\\caadmin.netskope.com.pem', 


Public Transport - Realtime - Alerts - v2
Public Transport - Realtime Vehicle Positions API v2
Public Transport - Realtime Trip Update API v2
Transport Routes
Public Transport - Realtime Trip Updates API
Trip Planner APIs
Public Transport - Timetables - Complete - GTFS
Public Transport - Timetables - For Realtime
Public Transport - Realtime Vehicle Positions API