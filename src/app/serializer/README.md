# Serializer Package

Here we have all of the classes to serialize models or other objects used by 
the MPD Analysis API. 

When an endpoint in `web.app.main.controller` receives a request, the 
response has to be converted into a JSON representation for consumption. This
 process of converting to JSON is called "serialization" and is handled by 
 code called a "data transfer object (DTO)"   