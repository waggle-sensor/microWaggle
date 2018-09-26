import requests
from datetime import datetime
from threading import Thread
import json
from sseclient import SSEClient
import time
import waggle.plugin
import os
from pprint import pprint


def read_file(path):
    with open(path) as file:
        return file.read()


def load_mapping_ID():
    mapping = {}

    for particleID in os.listdir('devices'):
        nodeID = read_file(os.path.join('devices', particleID, 'node_id')).strip()
        mapping[particleID] = nodeID

    return mapping

def load_mapping_Key():
    mapping = {}

    for particleID in os.listdir('devices'):
        Key = read_file(os.path.join('devices', particleID, 'key.pem')).strip()
        mapping[particleID] = Key

    return mapping


def load_mapping_Cert():
    mapping = {}

    for particleID in os.listdir('devices'):
        Cert = read_file(os.path.join('devices', particleID, 'cert.pem')).strip()
        mapping[particleID] = Cert

    return mapping


access_tokens = []
dataLog = []


#actualPlugin = waggle.plugin.Plugin()

#hecking and creating files

try:
    logFile = open("relay-log.txt", 'r')
    print("[RELAY-SERVER] Log file loaded.")

except IOError:
    file = open("relay-log.txt", 'w')
    print("[RELAY-SERVER] No log file was found, so one was created.")
    file.write("[CREATED] This log file was created at " + str(datetime.now()) + "\n")
#
#
try:
    file = open("relay-config.txt", 'r')
except IOError:
    print("[RELAY-SERVER] No config file was found, so one was created. Please load in access tokens. \n\t\tRun relay-server --help for more information.")
    file = open("relay-config.txt", 'w')
    with open("relay-log.txt", 'a') as logFile:
        logFile.write("Config file created at " + str(datetime.now()) + "\n")
#
# ############################################################################################################
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


#
#
#



def startStream(threadID):

    # https://api.particle.io/v1/devices/events?access_token=39d8ecf072b907ccf6303b994b38c9ca357f491f
    #ACCESS_TOKEN = "39d8ecf072b907ccf6303b994b38c9ca357f491f"
    #deviceId = "3a0045000851363136363935"

    IDMapping = load_mapping_ID()
    KeyMapping = load_mapping_Key()
    CertMapping = load_mapping_Cert()

    messages = SSEClient('https://api.particle.io/v1/devices/events?access_token={}'
                         .format(access_tokens[threadID]))
    for msg in messages:
        event = msg.event
        data = msg.data

        if not data:
            continue

        jsonData = json.loads(data)
        data = jsonData['data']

        print("Data:" + str(data))
        particleID = jsonData['coreid']
        print("ParticleID:" + str(particleID))
        try:
            beehiveID = IDMapping[particleID]
            beehiveKey = KeyMapping[particleID]
            beehiveCert = CertMapping[particleID]

        except KeyError:
            continue

        print(particleID, '->', beehiveID)

        print(data + " -> THREAD ID {0}".format(threadID))
        with open("relay-log.txt", 'a') as file:

            json.dump(data, file)
            file.write( "\t\t" + event + " -> THREAD ID {0} ".format(threadID) + " at: " + jsonData["published_at"] + '\n' )

            if event == 'sensorgram':
                sensorgrams = data.split(";")
                for sensorgram in sensorgrams:

                    print('devices/'+str(particleID)+'/cacert.pem')
                    credentials = waggle.plugin.Credentials(
                        host='cookie',
                        node_id=beehiveID,
                        sub_id='0000000000000001',
                        cacert='devices/'+str(particleID)+'/cacert.pem',
                        cert='devices/'+str(particleID)+'/cert.pem',
                        key='devices/'+str(particleID)+'/key.pem',
                    )


                    plugin = waggle.plugin.Plugin(
                        id=37,
                        version=(2, 4, 1),
                        credentials=credentials)


                    # print("Particle ID:" + str(particleID))
                    # print("Beehive ID:"+ str(beehiveID))
                    # print("Beehive Key:" + str(beehiveKey))
                    # print("Beehive Cert:" + str(beehiveCert))

                    pprint(waggle.protocol.unpack_sensorgrams(bytes.fromhex(sensorgram)))
                    print(bytes.fromhex(sensorgram))
                    plugin.add_measurement(bytes.fromhex(sensorgram))
                    plugin.publish_measurements()

#
# #something something JSON isn't working here, fix it.
#

#The thread for loop only works on the last thread for some reason. figure it out : )
for i in enumerate(access_tokens):
     #print(i[1])
     t = Thread(target=startStream, args=(i[0], ))
     t.start()
