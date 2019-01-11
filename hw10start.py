import tkinter
from tkinter import Entry, Label, Button
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json

# To run the program, call the last function in this file: startGUI().


# The Globals class demonstrates a better style of managing "global variables"
# than simply scattering the globals around the code and using "global x" within
# functions to identify a variable as global.
#
# We make all of the variables that we wish to access from various places in the
# program properties of this Globals class.  They get initial values here
# and then can be referenced and set anywhere in the program via code like
# e.g. Globals.zoomLevel = Globals.zoomLevel + 1
#
class Globals:
   mapT = 'Roadmap'
   rootWindow = None
   mapLabel = None
   defaultLocation = "Mauna Kea, Hawaii"
   mapLocation = defaultLocation
   enteredLocation = None
   zoomLabel = None
   mapFileName = 'googlemap.gif'
   mapSize = 400
   zoomLevel = 9

   
# Given a string representing a location, return 2-element tuple
# (latitude, longitude) for that location 
#
# See https://developers.google.com/maps/documentation/geocoding/
# for details
#
def geocodeAddress(addressString):
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   url = urlbase + quote_plus(addressString)
   #
   # Google's documentation says that should provide an API key with
   # the URL, and tells you how to register for and obtain a free API key
   # I strongly recommend you get one you and then uncomment the line below and replace
   # YOUR-API-KEY with your key.
   # Get one here:
   #   https://developers.google.com/maps/documentation/geocoding/get-api-key
   # IF YOU DO NOT get an API KEY, this code often still works but sometimes
   # you will get "OVER_QUERY_LIMIT" errors from Google.
   #
   url = url + "&key=" + "AIzaSyD4G8iTKR__8hNb5Z4AZjGegjutR3fIzzw"

   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(url, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      return
   loc = jsonResult['results'][0]['geometry']['location']
   return (float(loc['lat']),float(loc['lng']))


# Contruct a Google Static Maps API URL that specifies a map that is:
# - width-by-height in size (in pixels)
# - is centered at latitude lat and longitude long
# - is "zoomed" to the give Google Maps zoom level
#
# See https://developers.google.com/maps/documentation/static-maps/
#
# YOU WILL NEED TO MODIFY THIS TO BE ABLE TO
# 1) DISPLAY A PIN ON THE MAP
# 2) SPECIFY MAP TYPE - terrain vs road vs ...
#
def getMapUrl(width, height, lat, lng, zoom):
   urlbase = "http://maps.google.com/maps/api/staticmap?"
   args = "center={},{}&zoom={}&size={}x{}&maptype={}&format=gif&markers=color:red|{},{}|".format(lat,lng,zoom,width,height,Globals.mapT,lat,lng)
   return  urlbase+args

# Retrieve a map image via Google Static Maps API:
# - centered at the location specified by global propery mapLocation
# - zoomed according to global property zoomLevel (Google's zoom levels range from 0 to 21)
# - width and height equal to global property mapSize
# Store the returned image in file name specified by global variable mapFileName
#
def retrieveMapFromGoogle():
   lat, lng = geocodeAddress(Globals.mapLocation)
   url = getMapUrl(Globals.mapSize, Globals.mapSize, lat, lng, Globals.zoomLevel)
   urlretrieve(url, Globals.mapFileName)

########## 
#  basic GUI code

def displayMap():
   retrieveMapFromGoogle()    
   mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
   Globals.mapLabel.configure(image=mapImage)
   # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
   Globals.mapLabel.mapImage = mapImage
   
def readEntryAndDisplayMap():
   #### you should change this function to read from the location from an Entry widget
   #### instead of using the default location
   Globals.mapLocation = str(Globals.enteredLocation.get())
   displayMap()
     
def initializeGUIetc():

   Globals.rootWindow = tkinter.Tk()
   Globals.rootWindow.title("HW9 Q2")
   mainFrame = tkinter.Frame(Globals.rootWindow) 
   mainFrame.pack()
   
   
   Globals.enteredLocation = Entry(mainFrame)
   locationLabel = Label(mainFrame, text = 'Enter a location:')
   locationLabel.pack()
   Globals.enteredLocation.pack()
   Globals.zoomLabel= Label(mainFrame, text = 'Zoom Level:9')
   increaseButton = Button(mainFrame, text = '+', command = increaseBy1 )
   decreaseButton = Button(mainFrame, text = '-', command = decreaseBy1)
   defaultButton = Button(mainFrame,text = 'Standard map', command = standardMap)
   satButton = Button(mainFrame, text = 'Satellite map', command = changeMapSat)
   terrButton = Button(mainFrame, text = 'Terrain map', command = changeMapTerrain)
   hybButton = Button(mainFrame, text = 'Hybrid map',command = changeMapHybrid)
   readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map!", command=readEntryAndDisplayMap)
   readEntryAndDisplayMapButton.pack()
   mapTypeslabel = Label(mainFrame, text = "Choose desired map below:")
   mapTypeslabel.pack()
   defaultButton.pack()
   satButton.pack()
   terrButton.pack()
   hybButton.pack()
   # we use a tkinter Label to display the map image
   Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
   Globals.mapLabel.pack()
   increaseButton.pack()
   Globals.zoomLabel.pack()
   decreaseButton.pack()

def increaseBy1():
    if Globals.zoomLevel < 22:
       Globals.zoomLevel = Globals.zoomLevel + 1
    updateZoomLabel()

def decreaseBy1():
    if Globals.zoomLevel > 0:
        Globals.zoomLevel = Globals.zoomLevel - 1
    updateZoomLabel()
    
def updateZoomLabel():
    Globals.zoomLabel.configure(text="Zoom: {}".format(Globals.zoomLevel))
    displayMap()
    
def standardMap():
    Globals.mapT = 'roadmap'
    displayMap()
    
def changeMapSat():
    Globals.mapT = "satellite"
    displayMap()

def changeMapTerrain():
    Globals.mapT = 'terrain'
    displayMap()

def changeMapHybrid():
    Globals.mapT = 'hybrid'
    displayMap()
    
def startGUI():
    initializeGUIetc()
    displayMap()
    Globals.rootWindow.mainloop()
