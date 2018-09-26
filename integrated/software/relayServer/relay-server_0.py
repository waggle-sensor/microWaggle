import requests
from datetime import datetime
from threading import Thread
import json
from sseclient import SSEClient
import time
import waggle.plugin
access_tokens = []
dataLog = []

plugin = waggle.plugin.PrintPlugin()
#actualPlugin = waggle.plugin.Plugin()

#checking and creating files 

try: 
    logFile = open("relay-log.txt", 'r')
    print("[RELAY-SERVER] Log file loaded.")

except IOError:
    file = open("relay-log.txt", 'w')
    print("[RELAY-SERVER] No log file was found, so one was created.")
    file.write("[CREATED] This log file was created at " + str(datetime.now()) + "\n")


try:    
    file = open("relay-config.txt", 'r')
except IOError:
    print("[RELAY-SERVER] No config file was found, so one was created. Please load in access tokens. \n\t\tRun relay-server --help for more information.")
    file = open("relay-config.txt", 'w')
    with open("relay-log.txt", 'a') as logFile:
        logFile.write("Config file created at " + str(datetime.now()) + "\n")

############################################################################################################
logFile = open("relay-log.txt", 'a')
configFile = open("relay-config.txt", 'r')
for line in configFile: 
    if len(line.strip()) == 0:
        print("[WARNING] No access tokens found. Please input access tokens into relay-config.txt")

    if '\n' in line: 
        line = line.split('\n')[0]

    access_tokens.append(line)
    print("[RELAY-SERVER] Access token {0} loaded".format(line))
    logFile.write("[RELAY-SERVER] Access token {0} loaded".format(line) + "\n")





def startStream(threadID):

    # https://api.particle.io/v1/devices/events?access_token=39d8ecf072b907ccf6303b994b38c9ca357f491f
    #ACCESS_TOKEN = "39d8ecf072b907ccf6303b994b38c9ca357f491f"
    #deviceId = "3a0045000851363136363935"

    messages = SSEClient('https://api.particle.io/v1/devices/events?access_token={}'
                        .format(access_tokens[threadID]))
    for msg in messages:
        event = msg.event
        data = msg.data
    
        if not data:
            continue

        jsonData = json.loads(data)
        data = jsonData['data']
        
        print(data + " -> THREAD ID {0}".format(threadID))
        with open("relay-log.txt", 'a') as file:

            json.dump(data, file)
            file.write( "\t\t" + event + " -> THREAD ID {0} ".format(threadID) + " at: " + jsonData["published_at"] + '\n' )
            
            if event == 'sensorgram':
                sensorgrams = data.split(";")
                for sensorgram in sensorgrams:
                    print(bytes.fromhex(sensorgram))
                    plugin.add_measurement(bytes.fromhex(sensorgram))
                    #actualPlugin.add_measurement(bytes.fromhex(sensorgram))
                plugin.publish_measurements()
                #actualPlugin.publish_measurements()


#something something JSON isn't working here, fix it.

#The thread for loop only works on the last thread for some reason. figure it out : ) 
for i in enumerate(access_tokens):
     #print(i[1])
     t = Thread(target=startStream, args=(i[0], ))
     t.start()


