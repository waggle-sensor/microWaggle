#written by kenan arica. github.com/kenanarica if you have internships for me

import json
import requests
import os
import sys
import pprint

file = open("nodeConfigs.json", "a")

jsonNodes = []
nodes = []

access_token = ""
microWaggleConfig = [ #sensorname, sensorID, enabled/disabled, sensing freq(seconds)
    ['tempSensor', 0x01, True, 10], ['humiditySensor', 0x02, True, 10] ]



try:

    file = open("nodeConfigs.json", 'r')
except IOError:

    file = open("nodeConfigs.json", 'w')
    print("[WARNING] No previous nodes found, and no nodeConfigs.json file found. If it's your first time using the controller, don't worry. A file will be created.")



def getToken(args):
    tokenToReturn = args

    for node in jsonNodes:

        if args == node["nodeID"]:
            print("This node's token was matched with token of node " + node["nodeID"])
            tokenToReturn = node["token"]
    return tokenToReturn


def sendConfig(node, args, function):
    access_token = node["token"]

    payload = {'params': args, 'access_token':access_token}
    requests.post("https://api.particle.io/v1/devices/{0}/{1}/".format(node["deviceID"], function), payload)



def fixBool(arg):
    if arg.lower() == 'yes' or arg.lower() == 'y' or arg.lower() == 'true' or arg.lower() == 'en':
        return True
    if arg.lower() == 'no' or arg.lower() == 'n' or arg.lower() == 'false' or arg.lower == 'dis':
        return False
    else:
        rerun = input("[X] That's not a valid option, please type True, False, yes or no: ")
        return fixBool(rerun)

def createCustomConfig():
    numOfSensors = int(input("Number of Sensors to Add ? "))
    configuration = []
    for num in range(0, numOfSensors):
            print("------------------------------------")
            print("Configuring Sensor "+str(num+1)+":")
            tempConfig = []
            tempConfig.append(input("Name for sensor "+str(num+1)+ "? "))
            tempConfig.append(input("ID for sensor "+str(num+1)+ "? "))
            tempConfig.append(fixBool(input("Enabled for sensor "+str(num+1)+ "?(True/False) ")))
            tempConfig.append(input("Sensing Frequency for sensor "+str(num+1)+ "? "))
            configuration.append(tempConfig)
            print("------------------------------------")
            print("Configuration for Sensor "+str(num+1)+":")
            print(tempConfig)
            print("------------------------------------")

    print("Final Configuration for the Sensors")
    print(configuration)
    print("------------------------------------")

    return configuration




def loadNodes():
    global jsonNodes, nodes
    jsonNodes = []
    nodes = []

    configFile = open("nodeConfigs.json", "r")
    for line in configFile:
        jsonData = json.loads(line)
        jsonNodes.append(jsonData)
        if(len(jsonNodes)>0):
            print("[✓] Node with ID " + jsonData["nodeID"] + " loaded")
        else:
            print("No Nodes Loaded")

def overwriteJSON():
    os.remove("nodeConfigs.json")
    for node in jsonNodes:
        with open('nodeConfigs.json', 'a') as outfile:
            json.dump(node, outfile)
            outfile.write("\n")


def enableAllNodes():
    for node in jsonNodes:
        enableAllSensors(node)

def enableAllSensors(node):
    node["enabled"] = True
    for sensor in node["config"]:
        sensor[2] = True

    sendConfig(node, "enableall", "nodeConfig")


def disableAllNodes():
    for node in jsonNodes:
        disableAllSensors(node)

def disableAllSensors(node):
    node["enabled"] = False
    for sensor in node["config"]:
        sensor[2] = False

    sendConfig(node, "disableall", "nodeConfig")

def removeNode(nodeID):
    Notfound = True
    for i in range(len(jsonNodes)):
        if jsonNodes[i]["nodeID"] == nodeID:
            print("Deleting "+ nodeID)
            jsonNodes.pop(i)
            listNodes()
            Notfound = False
            break
    if(Notfound):
        print("Node ID "+str(nodeID)+" not found")


def reconfigure():
    for node in jsonNodes:
        reconfigureNode(node)
    listNodes()


def reconfigureNode(node):
    params = "freqreport-" + node["sendingFrequency"]
    sendConfig(node, params, "nodeConfig")

    params = "statusfreq-" + node["statusFrequency"]
    sendConfig(node, params, "nodeConfig")

    if(node["saveToSD"]):
        sendConfig(node, "enableSD", "nodeConfig")

    if(not(node["saveToSD"])):
        sendConfig(node, "disableSD", "nodeConfig")

    for sensor in node["config"]:
            reconfigureSensors(node,sensor)


def reconfigureSensors(node,sensor):
    if(sensor[2]):
         enabler = "en"
    if(not(sensor[2])):
        enabler= "dis"
    params = "{0};{1};{2}".format(sensor[1],enabler,sensor[3])
    sendConfig(node, params, "sensorConfig")



def configure(unparsedargs):

    nodeToConfigure = unparsedargs[0]
    multipleNodes = False

    if ',' in nodeToConfigure:
        nodeToConfigure = nodeToConfigure.split(",")
        multipleNodes = True


    if '-rn' in unparsedargs:
        newName = unparsedargs[unparsedargs.index("-rn") + 1]

        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously named {0} is now named {1}.".format(node["name"], newName))
                    node["name"] = newName

        else:
            for tempNode in nodeToConfigure:
                for node in jsonNodes:
                    if node["nodeID"] == tempNode:
                        print("[✓] Node previously named {0} is now named {1}.".format(node["name"], newName))
                        node["name"] = newName


    if '-id' in unparsedargs:
        newID = unparsedargs[unparsedargs.index("-id") + 1]

        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously with the ID {0} now has the ID {1}.".format(node["nodeID"], newID))
                    node["nodeID"] = newID

    if '-d' in unparsedargs:
        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node with the ID " + node["nodeID"] + " is now disabled." )
                    node["enabled"] = False
                    disableAllSensors(node)

        else:
            print(nodeToConfigure)
            for nodeIDToModify in nodeToConfigure:

                for node in jsonNodes:

                    if node["nodeID"] == nodeIDToModify:
                        node["enabled"] = False
                        print("[✓] Node with the ID " + node["nodeID"] + " is now disabled." )
                        disableAllSensors(node)



    if '-e' in unparsedargs:

        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node with the ID " + node["nodeID"] + " is now enabled." )
                    node["enabled"] = True
                    enableAllSensors(node)
        else:

            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:

                for node in jsonNodes:
                    if node["nodeID"] == nodeLabelToModify:
                        node["enabled"] = True
                        print("[✓] Node with the ID " + node["nodeID"] + " is now enabled." )
                        enableAllSensors(node)


    if '-sdf' in unparsedargs:
        newSDFSetting = unparsedargs[unparsedargs.index("-sdf") + 1]

        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously with the sending frequency setting {0} now has the setting {1} seconds.".format(node["sendingFrequency"], newSDFSetting))
                    node["sendingFrequency"] = newSDFSetting

        else:
            newSDFSetting = unparsedargs[unparsedargs.index("-sdf") + 1]
            for nodeLabelToModify in nodeToConfigure:

                for node in jsonNodes:

                    if node["nodeID"] == nodeLabelToModify:

                        print("[✓] Node previously with the sending frequency setting {0} now has the setting {1} seconds.".format(node["sendingFrequency"], newSDFSetting))
                        node["sendingFrequency"] = newSDFSetting

    if '-nsf' in unparsedargs:
        newNSFSetting = unparsedargs[unparsedargs.index("-nsf") + 1]

        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously with the sending frequency setting {0} now has the setting {1} seconds.".format(node["sendingFrequency"],newNSFSetting))
                    node["statusFrequency"] = newNSFSetting

        else:
            newNSFSetting = unparsedargs[unparsedargs.index("-nsf") + 1]

            for nodeLabelToModify in nodeToConfigure:
                #please help me what is going on here
                for node in jsonNodes:

                    if node["nodeID"] == nodeLabelToModify:

                        print("[✓] Node previously with the sending frequency setting {0} now has the setting {1} seconds.".format(node["sendingFrequency"], newNSFSetting))
                        node["statusFrequency"] = newNSFSetting




    if '-ssf' in unparsedargs:
        newSSFSetting = unparsedargs[unparsedargs.index("-ssf") + 1]
        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    for sensor in node["config"]:
                        sensor[3] = newSSFSetting
                        print("Setting sensor with ID {0} to a sensing frequency of {1} seconds".format(sensor[1], newSSFSetting))

        else:
            newSSFSetting = unparsedargs[unparsedargs.index("-ssf") + 1]
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:
                for node in jsonNodes:
                    if node["nodeID"] == nodeLabelToModify:
                        for sensor in node["config"]:
                            sensor[3] = newSSFSetting
                            print("Setting sensor with ID {0} to a sensing frequency of {1} seconds".format(sensor[1], newSSFSetting))


    if '-sd' in unparsedargs:
        newSDSetting = fixBool(unparsedargs[unparsedargs.index("-sd") + 1])
        command = ""

        if newSDSetting:
            command = "enableSD"
        else:
            command = "disableSD"

        if not multipleNodes:

            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node with ID {0} previously with the save to SD setting {1} now has the setting {2}.".format(node["nodeID"],node["saveToSD"], newSDSetting))
                    node["saveToSD"] = newSDSetting
        else:
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:

                for node in jsonNodes:

                    if node["nodeID"] == nodeLabelToModify:
                        print("[✓] Node with ID {0} previously with the save to SD setting {1} now has the setting {2}.".format(node["nodeID"],node["saveToSD"], newSDSetting))
                        node["saveToSD"] = newSDSetting

    if '-sen' in unparsedargs:
        function = unparsedargs[unparsedargs.index("-sen") + 1]

           # Ex usage: --configure [nodeID] -sen add

        if function == 'add':

            tempConfig = []
            tempConfig.append(input("Sensor name? "))
            tempConfig.append(input("Sensor ID? "))
            tempConfig.append(fixBool(input("Enabled? [True/False]")))
            tempConfig.append(input("How often, in seconds, should the sensor collect data? "))


            if not multipleNodes:

                for node in jsonNodes:

                    if node["nodeID"] == nodeToConfigure:
                        node["config"].append(tempConfig)
                        print("[✓] Sensor with ID {0} has been added to Node {1}".format(tempConfig[1], node["nodeID"]))
            else:
                for nodeLabelToModify in nodeToConfigure:

                    for node in jsonNodes:
                        if node["nodeID"] == nodeLabelToModify:
                            node["config"].append(tempConfig)
                            print("[✓] Sensor with ID {0} has been added to Node {1}".format(tempConfig[1], node["nodeID"]))

        # Ex. Usage: --configure [nodeID] -sen rm [sensorID]

        elif function == 'rm':
            if multipleNodes == False:

                sensorToRemove = unparsedargs[unparsedargs.index("rm") + 1]
                if ',' in sensorToRemove:
                    sensorToRemove = sensorToRemove.split(",")

                    for node in jsonNodes:
                        if node["nodeID"] == nodeToConfigure:
                            for individualSensor in sensorToRemove:
                                for sensor in node["config"]:
                                    if str(sensor[1]) == individualSensor:
                                        print("[✓] Removing sensor with ID " + individualSensor + " from node with ID " + node["nodeID"])
                                        node["config"].remove(sensor)

                else:
                        for node in jsonNodes:

                            if node["nodeID"] == nodeToConfigure:
                                for sensor in node["config"]:
                                    if str(sensor[1]) == sensorToRemove:
                                        print("Removing Sensors ")
                                        print("[✓] removing sensor with ID " + sensorToRemove)
                                        node["config"].remove(sensor)
            else:

                for individualNode in nodeToConfigure:

                    sensorToRemove = unparsedargs[unparsedargs.index("rm") + 1]
                    if ',' in sensorToRemove:
                        sensorToRemove = sensorToRemove.split(",")

                        for node in jsonNodes:
                            if node["nodeID"] == individualNode:
                                for individualSensor in sensorToRemove:
                                    for sensor in node["config"]:
                                        if str(sensor[1]) == individualSensor:
                                            print("[✓] removing sensor with ID " + individualSensor + " from node with ID " + node["nodeID"])
                                            node["config"].remove(sensor)

                    else:

                            for node in jsonNodes:
                                if node["nodeID"] == individualNode:

                                    for sensor in node["config"]:
                                        if str(sensor[1]) == sensorToRemove:
                                            print("[✓] removing sensor with ID " + sensorToRemove + " from node with ID " + node["nodeID"])
                                            node["config"].remove(sensor)

        # ex. Usage: --configure [nodeID] -sen dis [sensorID]

        elif function.lower() == 'dis':

            sensorToDisable = unparsedargs[unparsedargs.index("dis") + 1]

            if not multipleNodes:

                if ',' in sensorToDisable:
                    sensorToDisable = sensorToDisable.split(',')

                    for individualSensor in sensorToDisable:
                        for node in jsonNodes:
                            if node["nodeID"] == nodeToConfigure:
                                for sensor in node["config"]:
                                    if str(sensor[1]) == individualSensor:
                                        sensor[2] = False
                                        print("Setting sensor with ID " + individualSensor + " to disabled.")

                else:

                    for node in jsonNodes:
                        if node["nodeID"] == nodeToConfigure:

                            for sensor in node["config"]:
                                if str(sensor[1]) == sensorToDisable:
                                    sensor[2] = False
                                    print("Setting sensor with ID " + sensorToDisable + " to disabled.")

            else:

                for individualNode in nodeToConfigure:

                    sensorToDisable = unparsedargs[unparsedargs.index("dis") + 1]
                    if ',' in sensorToDisable:
                        sensorToDisable = sensorToDisable.split(",")

                        for node in jsonNodes:
                            if node["nodeID"] == individualNode:
                                for individualSensor in sensorToDisable:
                                    for sensor in node["config"]:
                                        if str(sensor[1]) == individualSensor:
                                            sensor[2] = False
                                            print("Setting sensor with ID " + individualSensor + " to disabled.")

                    else:

                            for node in jsonNodes:
                                if node["nodeID"] == individualNode:

                                    for sensor in node["config"]:
                                        if str(sensor[1]) == sensorToDisable:
                                            sensor[2] = False
                                            print("Setting sensor with ID " + sensorToDisable + " to disabled.")


        elif function.lower() == 'en':

                sensorToEnable = unparsedargs[unparsedargs.index("en") + 1]

                if not multipleNodes:

                    if ',' in sensorToEnable :
                        sensorToEnable  = sensorToEnable .split(',')

                        for individualSensor in sensorToEnable :
                            for node in jsonNodes:
                                if node["nodeID"] == nodeToConfigure:
                                    for sensor in node["config"]:
                                        if str(sensor[1]) == individualSensor:
                                            sensor[2] = True
                                            print("Setting sensor with ID " + individualSensor + " to enabled.")

                    else:

                        for node in jsonNodes:
                            if node["nodeID"] == nodeToConfigure:

                                for sensor in node["config"]:
                                    if str(sensor[1]) == sensorToEnable :
                                        sensor[2] = True
                                        print("Setting sensor with ID " + sensorToEnable  + " to enabled.")

                else:

                    for individualNode in nodeToConfigure:

                        sensorToEnable  = unparsedargs[unparsedargs.index("en") + 1]
                        if ',' in sensorToEnable :
                            sensorToEnable  = sensorToEnable .split(",")

                            for node in jsonNodes:
                                if node["nodeID"] == individualNode:
                                    for individualSensor in sensorToEnable :
                                        for sensor in node["config"]:
                                            if str(sensor[1]) == individualSensor:
                                                sensor[2] = True
                                                print("Setting sensor with ID " + individualSensor  + " to enabled.")

                        else:

                                for node in jsonNodes:
                                    if node["nodeID"] == individualNode:

                                        for sensor in node["config"]:
                                            if str(sensor[1]) == sensorToEnable :
                                                sensor[2] = True
                                                print("Setting sensor with ID " + sensorToEnable  + " to enabled.")




        elif function.lower() == 'freq':

            sensorToFreq = unparsedargs[unparsedargs.index("freq") + 2]
            print("Sensor:"+sensorToFreq)
            newFreqSetting = unparsedargs[unparsedargs.index("freq") + 1]

            if not multipleNodes:

                if ',' in sensorToFreq:
                    sensorToFreq = sensorToFreq.split(',')

                    for individualSensor in sensorToFreq:


                        for node in jsonNodes:
                            if node["nodeID"] == nodeToConfigure:
                                print("Multiple Nodes")
                                for sensor in node["config"]:
                                    if str(sensor[1]) == individualSensor:
                                        sensor[3] = newFreqSetting
                                        print("Setting sensor with ID " + individualSensor + " to a sensing freq of " + newFreqSetting + " seconds.")

                else:

                    for node in jsonNodes:
                        if node["nodeID"] == nodeToConfigure:
                            for sensor in node["config"]:
                                if str(sensor[1]) == sensorToFreq:
                                    sensor[3] = newFreqSetting
                                    print("Setting sensor with ID " + sensorToFreq + " to a sensing freq of " + newFreqSetting + " seconds.")

            else:

                for individualNode in nodeToConfigure:

                    sensorToFreq  = unparsedargs[unparsedargs.index("freq") + 2]
                    if ',' in sensorToFreq :
                        sensorToFreq  = sensorToFreq .split(",")

                        for node in jsonNodes:
                            if node["nodeID"] == individualNode:
                                for individualSensor in sensorToFreq :
                                    for sensor in node["config"]:
                                        if str(sensor[1]) == individualSensor:
                                            sensor[3] = newFreqSetting
                                            print("Setting sensor with ID " + individualSensor + " to a sensing freq of " + newFreqSetting + " seconds.")

                    else:

                        for node in jsonNodes:
                            if node["nodeID"] == individualNode:
                                for sensor in node["config"]:
                                    if str(sensor[1]) == sensorToFreq :
                                        sensor[3] = newFreqSetting
                                        print("Setting sensor with ID " + sensorToFreq + " to a sensing freq of " + newFreqSetting + " seconds.")



    print("Reconfiguring")
    reconfigure()



def listNodes():

    pp = pprint.PrettyPrinter(depth=4)

    if(len(jsonNodes)>0):
        print("---------------Micro-Waggle-Controller----------------")
        pp.pprint(jsonNodes)
        print("------------------------------------------------------")
    else:
        print("No Nodes to Display")




def addNode():
    print("\n-----------------New Node Parametors------------------------")
    nodeName = input("Node Name? ")
    nodeID = input("Node ID? ")
    deviceID = input("Device ID? ")
    sendingFrequency = input("Data Publish Frequency? ")
    statusFrequency = input("Status Publish Frequency? ")
    saveToSD = fixBool(str(input("SD Card Active? [True/False] ")))
    tempToken = getToken(input("Access Token ? "))
    defaultConfigYN = fixBool(str(input("Use the default Micro-waggle Config? [True/False] ")))
    sensorConfig = []
    if (defaultConfigYN):
        sensorConfig = microWaggleConfig
    if (not(defaultConfigYN)):
        sensorConfig = createCustomConfig()


    jsonToAppend = {
    "name" : nodeName, # -rn
    "nodeID" : nodeID, # -id
    "deviceID" : deviceID, # -d
    "enabled" : True, # -e
    "statusFrequency":statusFrequency,
    "sendingFrequency" : sendingFrequency, # -sdf
    "saveToSD" : saveToSD, # - sd
    "config" : sensorConfig, # - sen
    "token" : tempToken
    }

    jsonNodes.append(jsonToAppend)

    print('Updating Nodes')
    reconfigure()

    with open('nodeConfigs.json', 'a') as outfile:
        json.dump(jsonToAppend, outfile)
        outfile.write("\n")


loadNodes()

args = sys.argv[1:]

if len(args) > 0:

    if args[0] == "--help" or args[0] == "help":

        print("\nThis is a tool to configure your micro-waggle modules! Here's a list of commands: \n\n --help : gives you all the help you need! \n --list : lists all nodes and their configurations \n --enAll : enables all nodes! By default, all nodes are off out of the box. \n --disAll : disables all nodes \n --add: adds a new node, the parameters come after you type it! \n --rm : lists your nodes and allows you to remove one \n ")

    elif args[0] == "--list":

        listNodes()

    elif args[0] == "--enAll":

        enableAllNodes()
        listNodes()

    elif args[0] == "--disAll":

        disableAllNodes()
        listNodes()

    elif args[0] == "--add":
        addNode()

    elif args[0] == "--rm":
        deviceIDtoRemove = input(" Node ID of the Node you want to Remove? ")
        removeNode(deviceIDtoRemove)

    elif args[0] == "--configure":

        configure(args[1:])
    else:
        print("Invalid Command")

    # --config [node name] -sensorID []
else:
    print("---------------Micro-Waggle-Controller----------------")
    print("Commands list: \n --help : gives you all the help you need! \n --list : Lists all nodes and their configurations \n --enAll : Enables all nodes! \n --disAll : Disables all nodes \n --add: Adds a new node \n --rm : lists your nodes and allows you to remove one ")
    print("-------------------------------------------------------------")



#     ## Save our changes to JSON file
overwriteJSON()
