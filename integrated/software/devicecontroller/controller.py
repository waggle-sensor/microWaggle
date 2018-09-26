#written by kenan arica. github.com/kenanarica if you have internships for me

from prettytable import PrettyTable
import json
import requests
import os
import sys
file = open("nodeConfigs.json", "a")
nodes = []
jsonNodes = []
access_token = ""
bikeWaggleConfig = [ #sensorname, sensorID, enabled/disabled, sensing freq(seconds)
    ['MetMAC', 0x00, False, 30], ['TMP112', 0x01, False, 30], ['HTU21D', 0x02, False, 30], ['HIH4030', 0x03, False, 30], 
    ['BMP180', 0x04, False, 30], ['PR103J2', 0x05, False, 30], ['TSL250RDMS', 0x06, False, 30], ['MMA8452Q', 0x07, False, 30],
    ['SPV1840LR5H-B', 0x08, False, 30], ['TSYS01', 0x09, False, 30], ['HMC5883L', 0x0A, False, 30], ['HIH6130', 0x0B, False, 30],
    ['APDS_9006_020', 0x0C, False, 30], ['TSL260', 0x0D, False, 30], ['TSL250RDLS', 0x0E, False, 30], ['MLX75305', 0x0F, False, 30],
     ['ML8511', 0x10, False, 30], ['TMP421', 0x13, False, 30], ['Chemsense', 0x2A, False, 30], ['AlphaHisto', 0x28, False, 30]
]

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
    

""" TODO:

* do -h for --configure
* make disAll and enAll, dis and en multi-node function
* do the removeNode function
* make -e and -d disable/enable all nodes on given node, and make it multi-node if it isn't-d



"""



def fixBool(arg):
    if arg.lower() == 'yes' or arg.lower() == 'y' or arg.lower() == 'true' or arg.lower() == 'en':
        return True
    if arg.lower() == 'no' or arg.lower() == 'n' or arg.lower() == 'false' or arg.lower == 'dis':
        return False
    else:
        rerun = input("[X] That's not a valid option, please type True, False, yes or no: ")
        return fixBool(rerun)

# changeSensorConfig(newargs = ID, enabled, senseFreq)
# changeNodeConfig()
# changeSensorConfig(newArgs = "001;en;30")
#print(fixBool(input("test")))

#seeing if the config file exists. if it doesn't, create it.

#seeing if the nodeConfigs.json file exists. if it doesn't, create it.
try:
    
    file = open("nodeConfigs.json", 'r')
except IOError:

    file = open("nodeConfigs.json", 'w')
    print("[WARNING] No previous nodes found, and no nodeConfigs.json file found. If it's your first time using the controller, don't worry. A file will be created.")






"""
Stuff to do: A lot!

add a function to change enabling on different sensors and changing the frequency of sensing



"""
#change this to a request called "enableAllSensors" in the particle cloud
def enableAll():
    for node in jsonNodes:
        sendConfig(node, "enableall", "nodeConfig")
            

        
#change this to a request called "enableAllSensors" in the particle cloud
def disableAll():
    for node in jsonNodes:
        sendConfig(node, "disableall", "nodeConfig")
    
def createCustomConfig(): 
    numOfSensors = int(input("How many sensors would you like to have on your node?"))
    configuration = []
    for num in range(0, numOfSensors):
            tempConfig = []
            tempConfig.append(input("Sensor name? "))
            tempConfig.append(input("Sensor ID? "))
            tempConfig.append(fixBool(input("Enabled? [True/False]")))
            tempConfig.append(input("How often, in seconds, should the sensor collect data? "))
            configuration.append(tempConfig)
            print(tempConfig)
    print(configuration)
    return configuration
    



def loadNodes():
    global jsonNodes, nodes
    jsonNodes = []
    nodes = []
   
    configFile = open("nodeConfigs.json", "r")
    for line in configFile:
        jsonData = json.loads(line)
        print("[✓] Node with ID " + jsonData["nodeID"] + " loaded")
        jsonNodes.append(jsonData)
        #nodes.append(tempNodeObject)
    #print(jsonNodes)
    #print(nodes)

def configure(unparsedargs):
    #make sure nodes are loaded, we're going to overwrite the configs file every time this function is called.
    #print(unparsedargs)
    nodeToConfigure = unparsedargs[0] #name of the node that the user wants to configure
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
        newDisabledSetting = unparsedargs[unparsedargs.index("-d") + 1]
        
        if not multipleNodes:
            
            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node with the ID " + node["nodeID"] + " is now disabled." )
                    node["enabled"] = False
                    sendConfig(node, "disableall", "nodeConfig")
                    
        else:
            newDisabledSetting = unparsedargs[unparsedargs.index("-d") + 1]
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:
                #please help me what is going on here
                for node in jsonNodes:
                
                    if node["name"] == nodeLabelToModify:
                        
                        print("[✓] Node with the ID " + node["nodeID"] + " is now disabled." )
                        node["enabled"] = False

                        sendConfig(node, "disableall", "nodeConfig")
    


    if '-e' in unparsedargs:
        newEnabledSetting = unparsedargs[unparsedargs.index("-e") + 1]
        
        if not multipleNodes:
            
            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node with the ID " + node["nodeID"] + " is now enabled." )
                    node["enabled"] = True
                    sendConfig(node, "enableall", "nodeConfig")
        
        else:
            newEnabledSetting = unparsedargs[unparsedargs.index("-e") + 1]
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:
                #please help me what is going on here
                for node in jsonNodes:
                
                    if node["nodeID"] == nodeLabelToModify:
                        print("[✓] Node with the ID " + node["nodeID"] + " is now enabled." )
                        node["enabled"] = True
                        sendConfig(node, "enableall", "nodeConfig")
        
    


    if '-sdf' in unparsedargs:
        newSDFSetting = unparsedargs[unparsedargs.index("-sdf") + 1]
        
        if not multipleNodes:
            
            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously with the sending frequency setting {0} now has the setting {1} seconds.".format(node["sendingFrequency"], newSDFSetting))
                    node["sendingFrequency"] = newSDFSetting
                    params = "freqreport-" + newSDFSetting
                    sendConfig(node, params, "nodeConfig")

        else:
            newSDFSetting = unparsedargs[unparsedargs.index("-sdf") + 1]
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:
                #please help me what is going on here
                for node in jsonNodes:
                
                    if node["nodeID"] == nodeLabelToModify:
                       
                        print("[✓] Node previously with the sending frequency setting {0} now has the setting {1} seconds.".format(node["sendingFrequency"], newSDFSetting))
                        node["sendingFrequency"] = newSDFSetting
                        params = "freqreport-" + newSDFSetting
                        sendConfig(node, params, "nodeConfig")
    



    if '-ssf' in unparsedargs:
        newSSFSetting = unparsedargs[unparsedargs.index("-ssf") + 1]
        if not multipleNodes:
            
            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously with the sensing frequency setting {0} now has the setting {1} seconds.".format(node["sensingFrequency"], newSSFSetting))
                    node["sensingFrequency"] = newSSFSetting

                    for sensor in node["config"]:
                        sensor[3] = newSSFSetting
                        print("Setting sensor with ID {0} to a sensing frequency of {1} seconds".format(sensor[3], newSSFSetting))
                        params = "{0};_;{1}".format(sensor[1], newSSFSetting)
                        sendConfig(node, params, "sensorConfig")


        else:
            newSSFSetting = unparsedargs[unparsedargs.index("-ssf") + 1]
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:
                #please help me what is going on here
                for node in jsonNodes:
                
                    if node["nodeID"] == nodeLabelToModify:
                        print("[✓] Node previously with the sensing frequency setting {0} now has the setting {1} seconds.".format(node["sensingFrequency"], newSSFSetting))
                        node["sensingFrequency"] = newSSFSetting
                        

                        for sensor in node["config"]:
                            sensor[3] = newSSFSetting
                            print("Setting sensor with ID {0} to a sensing frequency of {1} seconds".format(sensor[3], newSSFSetting))
                            params = "{0};_;{1}".format(sensor[1], newSSFSetting)
                            sendConfig(node, params, "sensorConfig")

    
    if '-sm' in unparsedargs:
        newStatusSetting = fixBool(unparsedargs[unparsedargs.index("-sm") + 1])
        command = ""

        if newStatusSetting:
            command = "Status" #STATUS MESSAGE NOT IMPLEMENTED
        else: 
            command = "notStatus"

        if not multipleNodes:
            
            for node in jsonNodes:
                if node["nodeID"] == nodeToConfigure:
                    print("[✓] Node previously with the status message setting {0} now has the setting {1}.".format(node["statusMessage"], newStatusSetting))
                    node["statusMessage"] = newStatusSetting
        else:
            newStatusSetting = unparsedargs[unparsedargs.index("-sm") + 1]
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:
                #please help me what is going on here
                for node in jsonNodes:
                
                    if node["nodeID"] == nodeLabelToModify:
                        print("[✓] Node previously with the status message setting {0} now has the setting {1}.".format(node["statusMessage"], newStatusSetting))
                        node["statusMessage"] = newStatusSetting
        
        #params = command
        #payload = {'params': params, 'access_token': access_token}
        #requests.post("https://api.particle.io/v1/devices/{0}/{1}/".format(node["deviceID"], "nodeConfig"), payload)

    


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
                    print("[✓] Node previously with the save to SD setting {0} now has the setting {1}.".format(node["saveToSD"], newSDSetting))
                    node["saveToSD"] = newSDSetting
                    params = command
                    sendConfig(node, params, "nodeConfig")
        else:
            print(nodeToConfigure)
            for nodeLabelToModify in nodeToConfigure:

                for node in jsonNodes:
                
                    if node["nodeID"] == nodeLabelToModify:
                        print("[✓] Node previously with the save to SD setting {0} now has the setting {1}.".format(node["saveToSD"], newSDSetting))
                        node["saveToSD"] = newSDSetting
                        print("Sending command...")
                        params = command
                        sendConfig(node, params, "nodeConfig")


        #sen functions:
        # add/remove sensor
        # redo entire sensor config
        # change individual sensor configs  

###########SEN BLOCK


    if '-sen' in unparsedargs: 
        function = unparsedargs[unparsedargs.index("-sen") + 1]
        
        ###adding or removing a sensor. --configure [nodeName(s)] -sen [sensorID(s)] [add/remove/config] [-e [T/F], -id [newID], -ssf [seconds] ] ]

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
                                    if sensor[1] == individualSensor:
                                        print("[✓] removing sensor with ID " + individualSensor + " from node with ID " + node["nodeID"])
                                        node["config"].remove(sensor)

                else:
                        
                        for node in jsonNodes:
                            if node["nodeID"] == nodeToConfigure:

                                for sensor in node["config"]:
                                    if sensor[1] == sensorToRemove:
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
                                        if sensor[1] == individualSensor:
                                            print("[✓] removing sensor with ID " + individualSensor + " from node with ID " + node["nodeID"])
                                            node["config"].remove(sensor)

                    else:
                            
                            for node in jsonNodes:
                                if node["nodeID"] == individualNode:

                                    for sensor in node["config"]:
                                        if sensor[1] == sensorToRemove:
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
                                    if sensor[1] == individualSensor:
                                        sensor[2] = False
                                        print("Setting sensor with ID " + individualSensor + " to disabled.")
                                    
                                        params = "{0};dis;_".format(sensor[1])
                                        sendConfig(node, params, "sensorConfig")
                else:

                    for node in jsonNodes:
                        if node["nodeID"] == nodeToConfigure:

                            for sensor in node["config"]:
                                if sensor[1] == sensorToDisable:
                                    sensor[2] = False
                                    print("Setting sensor with ID " + sensorToDisable + " to disabled.")
                                
                                    params = "{0};dis;_".format(sensor[1])
                                    sendConfig(node, params, "sensorConfig")

        # ex. Usage: --configure [nodeID] -sen en [sensorID]


        elif function.lower() == 'en':

            sensorToEnable = unparsedargs[unparsedargs.index("en") + 1]

            if not multipleNodes:
                
                if ',' in sensorToEnable:
                    sensorToEnable = sensorToEnable.split(',')

                    for individualSensor in sensorToEnable:
                        

                        for node in jsonNodes:
                            if node["nodeID"] == nodeToConfigure:

                                for sensor in node["config"]:
                                    if sensor[1] == individualSensor:
                                        sensor[2] = True
                                        print("Setting sensor with ID " + individualSensor + " to Enabled.")
                                    
                                        params = "{0};en;_".format(sensor[1])
                                        sendConfig(node, params, "sensorConfig")
                else:

                    for node in jsonNodes:
                        if node["nodeID"] == nodeToConfigure:

                            for sensor in node["config"]:
                                if sensor[1] == sensorToEnable:
                                    sensor[2] = True
                                    print("Setting sensor with ID " + sensorToEnable + " to Enabled.")

                                    params = "{0};en;_".format(sensor[1])
                                    sendConfig(node, params, "sensorConfig")

        # ex. Usage: --configure [nodeID] -sen freq [newSetting] [sensorID]

        elif function.lower() == 'freq':

            sensorToFreq = unparsedargs[unparsedargs.index("freq") + 2]
            newFreqSetting = unparsedargs[unparsedargs.index("freq") + 1]

            if not multipleNodes:
                
                if ',' in sensorToFreq:
                    sensorToFreq = sensorToFreq.split(',')

                    for individualSensor in sensorToFreq:
                        

                        for node in jsonNodes:
                            if node["nodeID"] == nodeToConfigure:

                                for sensor in node["config"]:
                                    if sensor[1] == individualSensor:
                                        sensor[2] = True
                                        print("Setting sensor with ID " + individualSensor + " to a sensing freq of " + newFreqSetting + " seconds.")
                                        params = "{0};_;{1}".format(sensor[1], newFreqSetting)
                                        sendConfig(node, params, "sensorConfig")    
                                        
                else:

                    for node in jsonNodes:
                        if node["nodeID"] == nodeToConfigure:

                            for sensor in node["config"]:
                                if sensor[1] == sensorToFreq:
                                    sensor[2] = True
                                    print("Setting sensor with ID " + individualSensor + " to a sensing freq of " + newFreqSetting + " seconds.")

                                    params = "{0};_;{1}".format(sensor[1], newFreqSetting)
                                    sendConfig(node, params, "sensorConfig")

    with open('nodeConfigs.json', 'w') as outfile:
        for node in jsonNodes:
            json.dump(node, outfile)
            outfile.write("\n")
    #at the end we're going to save this to our objects and overwrite the nodeConfigs.json file.


def listNodes(args):

    # --list -sen [nodeID]


    if '-sen' in args:
        t = PrettyTable(['Sensor name', 'Sensor ID', 'Enabled/Disabled', 'Reporting Frequency'])
        nodeToSelect = args[args.index("-sen") + 1]
        for node in jsonNodes:
            if node["nodeID"] == nodeToSelect:
                for sensor in node["config"]:
                    t.add_row([sensor[0], sensor[1], sensor[2], sensor[3]])
    else:
                
        t = PrettyTable(['Name', 'nodeID', 'deviceID', 'enabled', 'Sending Freq', 'Sensing Freq', 'Status Message', 'Save to SD', 'Access token'])
        for node in jsonNodes:
            
            t.add_row([node["name"], node["nodeID"], node["deviceID"], node["enabled"], node["sendingFrequency"], node["sensingFrequency"], node["statusMessage"], node["saveToSD"], node["token"]])
    print(t)



def addNode():
    nodeName = input("What would you like to name your node? ")
    nodeID = input("What is the node ID? ")
    deviceID = input("What is the deviceID? ")
    sendingFrequency = input("What would you like the SENDING frequency to be? ")
    sensingFrequency = input("What would you like the SENSING frequency to be? ")
    statusMessage = input("Would you like the node to send a status message? [True/False] ")
    saveToSD = input("Would you like the node to save to SD during connection loss? [True/False] ")
    defaultConfigYN = input("Use default config for bike waggle? [True/False]")
    tempToken = getToken(input("What is this node's access token? If you want to use the same token as an existing node, just input the ID."))
    
    sensorConfig = []
    if defaultConfigYN.lower().startswith("t"):
        sensorConfig = bikeWaggleConfig
    elif defaultConfigYN.lower().startswith("f"):
        sensorConfig = createCustomConfig()


    jsonToAppend = {
    "name" : nodeName, # -rn 
    "nodeID" : nodeID, # -id
    "deviceID" : deviceID, # -d
    "enabled" : False, # -e
    "sendingFrequency" : sendingFrequency, # -sdf
    "sensingFrequency" : sensingFrequency, # -ssf
    "statusMessage" : statusMessage, # -sm
    "saveToSD" : saveToSD, # - sd
    "config" : sensorConfig, # - sen
    "token" : tempToken
    }
    
    jsonNodes.append(jsonToAppend)

    
    with open('nodeConfigs.json', 'a') as outfile:
        json.dump(jsonToAppend, outfile)
        outfile.write("\n")
    print(jsonNodes)
    #configString = "{{ \"name\" : \"{}\",  }}"

loadNodes()
#list of node names or node ID's. compare this to a node-lookup table if it's in name form.

#import OS package and get args
args = sys.argv[1:] #get args here, removing the first "controller.py entry"
#first, check if args are equal to non-function commands such as list nodes, help, disableAll, enableAll, addNode, removeNode
if len(args) > 0:
        
    if args[0] == "--help" or args[0] == "help":

        print("\nThis is a tool to configure your micro-waggle modules! Here's a list of commands: \n\n --help : gives you all the help you need! \n --list : lists all nodes and their configurations \n --enAll : enables all nodes! By default, all nodes are off out of the box. \n --disAll : disables all nodes \n --add: adds a new node, the parameters come after you type it! \n --rm : lists your nodes and allows you to remove one \n ")

    elif args[0] == "--list":

        listNodes(args)

    elif args[0] == "--enAll":

        enableAll()

    elif args[0] == "--disAll":

        disableAll(args[1:])

    elif args[0] == "--add":

        addNode()

    elif args[0] == "--rm":

        removeNode()

    elif args[0] == "--configure":

        configure(args[1:])

    # --config [node name] -sensorID []
else: 
    print("\nThis is a tool to configure your micro-waggle modules! Here's a list of commands: \n\n --help : gives you all the help you need! \n --list : lists all nodes and their configurations \n --enAll : enables all nodes! By default, all nodes are off out of the box. \n --disAll : disables all nodes \n --add: adds a new node, the parameters come after you type it! \n --rm : lists your nodes and allows you to remove one \n ")

# I have to fix the --help interface. I'll get to it one day.

