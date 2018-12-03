from datetime import datetime
from threading import Thread
import json
from sseclient import SSEClient
import waggle.plugin
import os
from pprint import pprint
import sys

access_tokens = []
dataLog = []


def read_file(path):
    with open(path) as file:
        return file.read()


def load_access_tokens(path):
    return read_file(path).splitlines()


def load_mapping_ID():
    mapping = {}

    for particleID in os.listdir('devices'):
        nodeID = read_file(os.path.join('devices', particleID, 'node_id')).strip()
        mapping[particleID] = nodeID

    return mapping


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
#
# ############################################################################################################
logFile = open("relay-log.txt", 'a')

access_tokens = load_access_tokens('relay-config.txt')

if len(access_tokens) == 0:
    print("[WARNING] No access tokens found. Please input access tokens into relay-config.txt")
    sys.exit(1)

for token in access_tokens:
    print("[RELAY-SERVER] Access token {0} loaded".format(token))
    logFile.write("[RELAY-SERVER] Access token {0} loaded".format(token) + "\n")


def startStream(threadID):
    IDMapping = load_mapping_ID()

    messages = SSEClient('https://api.particle.io/v1/devices/events?access_token={}'
                         .format(access_tokens[threadID]))

    for msg in messages:
        event = msg.event
        data = msg.data

        if not data:
            continue

        jsonData = json.loads(data)
        data = jsonData['data']
        particleID = jsonData['coreid']

        print("--------------------------------------")

        print("ParticleID:" + str(particleID))

        try:
            beehiveID = IDMapping[particleID]
        except KeyError:
            continue

        with open("relay-log.txt", 'a') as file:
            json.dump(data, file)
            file.write( "\t\t" + event + " -> THREAD ID {0} ".format(threadID) + " at: " + jsonData["published_at"] + '\n' )

            if event == 'sensorgram':
                sensorgrams = data.split(";")
                for sensorgram in sensorgrams:

                    credentials = waggle.plugin.Credentials(
                        host='cookie',
                        node_id=beehiveID,
                        sub_id='0000000000000001',
                        cacert='devices/'+str(particleID)+'/cacert.pem',
                        cert='devices/'+str(particleID)+'/cert.pem',
                        key='devices/'+str(particleID)+'/key.pem',
                    )

                    # Sending data to Beehive
                    plugin = waggle.plugin.Plugin(
                        id=37,
                        version=(2, 4, 1),
                        credentials=credentials)

                    try:
                        pprint(waggle.protocol.unpack_sensorgrams(bytes.fromhex(sensorgram)))
                    except KeyError:
                        pass

                    plugin.add_measurement(bytes.fromhex(sensorgram))
                    plugin.publish_measurements()


for i in enumerate(access_tokens):
    t = Thread(target=startStream, args=(i[0], ))
    t.start()
