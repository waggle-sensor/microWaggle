from datetime import datetime
from threading import Thread
import json
from sseclient import SSEClient
import waggle.plugin
import os
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


def startStream(access_token):
    IDMapping = load_mapping_ID()

    messages = SSEClient('https://api.particle.io/v1/devices/events?access_token={}'
                         .format(access_token))

    plugins = {}

    for msg in messages:
        event = msg.event
        data = msg.data

        if not data:
            continue

        jsonData = json.loads(data)
        data = jsonData['data']
        particleID = jsonData['coreid']

        try:
            beehiveID = IDMapping[particleID]
        except KeyError:
            continue

        if particleID not in plugins:
            print('[RELAY-SERVER] Initial event for', particleID)

            credentials = waggle.plugin.Credentials(
                host='beehive1.mcs.anl.gov',
                node_id=beehiveID,
                sub_id='0000000000000001',
                cacert='devices/'+str(particleID)+'/cacert.pem',
                cert='devices/'+str(particleID)+'/cert.pem',
                key='devices/'+str(particleID)+'/key.pem',
            )

            try:
                plugins[particleID] = waggle.plugin.Plugin(id=100, version=(0, 0, 1), credentials=credentials)
            except Exception as exc:
                print(exc)
                raise

            print('[RELAY-SERVER] Plugin ready for', particleID)

        plugin = plugins[particleID]

        print("--------------------------------------")
        print('[RELAY-SERVER] Forwarding messages from', particleID, 'to', beehiveID)

        with open("relay-log.txt", 'a') as file:
            json.dump(data, file)
            file.write( "\t\t" + event + " -> TOKEN {0} ".format(access_token) + " at: " + jsonData["published_at"] + '\n' )

        if event == 'sensorgram':
            sensorgrams = data.split(";")

            for sensorgram in sensorgrams:
                plugin.add_measurement(bytes.fromhex(sensorgram))
                plugin.publish_measurements()


def main():
    access_tokens = load_access_tokens('relay-config.txt')

    if len(access_tokens) == 0:
        print("[WARNING] No access tokens found. Please input access tokens into relay-config.txt")
        sys.exit(1)

    for token in access_tokens:
        print("[RELAY-SERVER] Access token {0} loaded".format(token))
        logFile.write("[RELAY-SERVER] Access token {0} loaded".format(token) + "\n")

    threads = [Thread(target=startStream, args=(token,), name=token) for token in access_tokens]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
