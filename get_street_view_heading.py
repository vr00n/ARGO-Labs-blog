import time
import socks
import socket
import unirest

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
socket.create_connection = create_connection
import urllib


#https://developers.google.com/maps/documentation/streetview/?hl=en
url = "http://maps.googleapis.com/maps/api/streetview?size=480x480&pitch=-22&fov=70&location="
#url = "http://maps.googleapis.com/maps/api/streetview?size=480x480&pitch=-10&fov=60&heading=-95&location="

#This determines the start and end addresses
num_list=range(112,500)
#Getting only even numbers to look on the same side of the street
evensList = [x for x in num_list if x % 2 == 0]
#Iterate through various heading to simulate a "sweep"
headinglist = [-20,-10,0,10,20,30,40,50,60,70,80,90]
counter=0

def get_image(inputFileURL, inputFileName):
    error=0
    try:
        print "\n",inputFileURL
        imageFile.retrieve(inputFileURL, inputFileName)
        print "Saved"+str(i)+"+East+"+str(a)+"+Street+NYC"
        error = 0
    except IOError as e:
        print "ERROR - SLEEPING for 10",e
        error +=1
        if (error > 5):
            socket.socket = socks.socksocket
            socket.create_connection = create_connection
            return
        time.sleep(10)
        get_image(inputFileURL, inputFileName)

#USING CAMFIND API
def identify_image(inputFileURL):
    response = unirest.post("https://camfind.p.mashape.com/image_requests",
  headers={
    "X-Mashape-Key": "9UyIuOYhCKmshb72Y27ctmWYJReGp1G3LaBjsndZ3QPhPjjHMl"
  },
  params={
    "focus[x]": "480",
    "focus[y]": "480",
    "image_request[language]": "en",
    "image_request[locale]": "en_US",
    "image_request[remote_image_url]": ""+str(inputFileURL)+""
  }
)

    token = response.body['token'] # The parsed response
    print token
    response2 = unirest.get("https://camfind.p.mashape.com/image_responses/"+str(token),
  headers={
    "X-Mashape-Key": "9UyIuOYhCKmshb72Y27ctmWYJReGp1G3LaBjsndZ3QPhPjjHMl"
  }
)
    time.sleep(1)
    while (response2.body['status'] == 'not completed'):
        response2 = unirest.get("https://camfind.p.mashape.com/image_responses/"+str(token),
    headers={
        "X-Mashape-Key": "9UyIuOYhCKmshb72Y27ctmWYJReGp1G3LaBjsndZ3QPhPjjHMl"
    }
    )
    print "Sleeping"
    time.sleep(1)

    #print response2.body
    print response2.raw_body


#This sets the specific street you want to start touring
a=59
for i in evensList:
    #If you want to enable "sweep mode" uncomment the below 2 lines
    #for j in headinglist:
    print "Parsing East",a,"Street with heading 10"#,j
    #pdb.set_trace()
    counter = counter + 1
    if (counter < 10):
        inputFileURL=url+str(i)+"+East+"+str(a)+"+Street+NYC"+"&heading=10"#+str(j)
        inputFileName = str(i)+"+East+"+str(a)+"+Street+NYC_Heading10.jpg"#+str(j)+".jpg"
        print "\n"
        print inputFileURL,inputFileName
        imageFile = urllib.URLopener()
        get_image(inputFileURL,inputFileName)
        identify_image(inputFileURL)
    else:
        print "Sleeping"
        time.sleep(5)
        counter = 0


