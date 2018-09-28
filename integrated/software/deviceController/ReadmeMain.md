# DeviceController

The Device controller module gives users of MicroWaggle Devices a form of user control over there devices. The module is capable of 
prompting status messages, changing frequencies of reading and publishing data as well as enabling & disabling of Device sensors. 

# Micro-Waggle Configuration CLI guide


The script `controller.py` is everything you should need to change configuration of your Micro-Waggle network. It's still a WIP, so bear with us! Please let us know if you have any questions or concerns.  
## Some really important things to know: 

* Version 1.1 was released as of 8/20/18. Mostly cleaned up the code, but now **access tokens are node-specific, and upon creation can use the same access token as the existing node. Just follow the "add node" prompt when you do** `python3 controller.py --add`.
* If two or more nodes have the same ID, any change made to one node with a corresponding ID to another will undergo the same change. For example, if you have two nodes with the ID 45, you'll add the same sensor to both nodes after using the `--configure 45 -sen add` command, because they share the same ID.

## First time usage: 
* **If you want to use an existing configuration**, just make sure your `nodeConfigs.json` and `config.txt` files are in the same folder as `controller.py`. Everything should be smooth sailing from there.
* Run `controller.py` with no args. -> `python3 controller.py`. The `--help` prompt will come up, that's normal.
* `controller.py` will create any files needed, such as `config.txt` and `nodeConfig.json`. 
* You'll be prompted to enter your access token. After you enter it, setup should be done.


## Usage
* **The script must be run in PYTHON3 with one of the following args seen below:**

`--help` or `help` : Lists all commands, as well as their respective syntaxes and functions.

* Ex. Usage: `python3 controller.py --help` 

`--list [OPTIONAL ARGS: -sen <nodeID>]`: Lists all nodes, respective information such as nodeID and deviceID, and sensor configuration. Using the `-sen` flag will list all sensors and their attributes on the given `nodeID`.
* Ex. Usage: `python3 controller.py --list`
* Ex. Usage, **Given that node with ID 22 exists**: `python3 controller.py --list -sen 22`

`--enAll` : Enables all sensors on on all nodes.
* Ex. Usage: `python3 controller.py --enAll`

`--disAll` : Disables all sensors on all nodes.
* Ex. Usage: `python3 controller.py --disAll`

`--rm <nodeID>` : removes the node with the specified name
* Ex. Usage, **Given a node with nodeID 33 exists** : `python3 controller.py --rm <nodeID>`

`--add` : Starts the prompt to add a new node.
* Ex. Usage: `python3 controller.py --add`

`--configure <nodeID> [-rn/-id/-d/-e/-sdf/-ssf/-sm/-sd/-sen]`
* Ex. Usage: **See below**

## The configure command

The configure command is the main attraction, and how you modify your node. Here are the args you can use.

`-rn <new name>` : Renames the entered node. You can specify multiply nodes to rename to the same thing, by putting a comma in between the nodes you want to rename. Ex. Usage below. 
* **NODE NAMES CANNOT HAVE SPACES!**
* Ex. Usage, **Given a node with the nodeID 33 exists**: `python3 controller.py --configure 33 -rn bar` -> Node 33 is now named bar.
* Ex. Usage, **Given nodes with the nodeID 33, 99, and 66 exist**: `python3 controller.py --configure 33,66,99 -rn Field_node` -> nodes with the nodeID 33, 66, and 99 are now named "Field_node".


`-id <new nodeID>` : changes the nodeID of the entered node. 
* Ex. Usage, **Given a node with the nodeID 33 exists**: `python3 controller.py --configure 33 -id 96024` -> Node with ID 33 now has the nodeID 96024.
* Node ID's certaintly don't have to have numbers or letters exclusively, as the controller supports both. However, try to keep it concise. I haven't tested the controller with longer, more complex ID's, so they may not work. Please contact me if you have any issues regarding this.
* **USE CAREFULLY. ANY CHANGES DONE TO A NODE WITH A SPECIFIED ID WILL BE DONE TO ALL NODES WITH THE MATCHING ID.**

`-d` : Disables all sensors on the given node. Can disable all sensors on more than one node at once if the nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 34 exists**: `python3 controller.py --configure 34 -d` -> Node with ID 34 is disabled.
* Ex. Usage, **Given nodes with the nodeID 35, 36, 37, & 38 exist**: `python3 controller.py --configure 35,36,37,38 -d` -> Sensors on nodes with ID 35, 36, 37, & 38 are disabled.

`-e` : Enables all sensors on the given node. Can enable all sensors on more than one node at once if the nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 34 exists**: `python3 controller.py --configure 34 -e` -> Node with ID 34 is enabled.
* Ex. Usage, **Given nodes with the nodeID 39, 40, 41, & 42 exist**: `python3 controller.py --configure 39,40,41,42 -e` -> Sensors on nodes with ID 39, 40, 41, & 42 are enabled.

`-sdf <new sending frequency in seconds>` : Changes the frequency at which the selected node sends data. Can change multiple node's setting if nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 43 exists**: `python3 controller.py --configure 43 -sdf 15` -> Node with ID 43 now has a sending frequency of 15 seconds. 
* Ex. Usage, **Given nodes with the nodeID 44, 45, and 46 exist**: `python3 controller.py --configure 44,45,46 -sdf 15` -> Nodes ID 44, 45, & 46 now have a sending frequency of 15 seconds. 

`-ssf <new sensing frequency in seconds>` : Changes the frequency at which the selected node senses data. Can change multiple node's setting if nodeID's are separated by a comma. Example usage below.
* Ex. Usage, **Given a node with the nodeID 47 exists**: `python3 controller.py --configure 47 -ssf 15` -> Node with ID 47 now has a sensing frequency of 15 seconds. 
* Ex. Usage, **Given nodes with the nodeID 48, 49, and 50 exist**: `python3 controller.py --configure 44,45,46 -ssf 15` -> Nodes ID 48, 49, & 50 now have a sensing frequency of 15 seconds.

`-sm <True/False>` : Sets if the node should send a status message periodically. True = Yes, False = No. You can use this command on multiple nodes, provided there's a comma in between the nodeIDs. Example usage below. 
* Ex. Usage: `python3 controller.py --configure 51 -sm True` -> Node with the ID 51 will send status messages.
* Ex. Usage: `python3 controller.py --configure 52,53,54,55,56 -sm False` -> Node with the IDs 52, 53, 54, 55, & 56 will not send status messages.

`-sd <True/False>` : Sets if the node should save data to SD storage when disconnected from Wi-Fi. True = Yes, False = No. You can use this command on multiple nodes, provided there's a comma in between the nodeIDs. Example usage below. 
* Ex. Usage: `python3 controller.py --configure 57 -sd True` -> Node with the ID 51 will store to SD.
* Ex. Usage: `python3 controller.py --configure 58,59,60,61,62 -sm False` -> Node with the IDs 58, 59, 60, 61, & 62 will not save to SD storage.

### The sen configure commmand

The `-sen` subcommand of the `--configure` command has two parts, so it gets it's own subsection. This is where you can configure individual sensors on your node without having to make a new Node/Configuration.

`-sen add` : Adds a new sensor to the the given node. It will take you through the prompt for adding a new sensor. If you specify multiple nodes in this command, the sensor form you fill out will be applied to **all** nodes specified. 

* Ex. Usage: `python3 controller.py --configure 63 -sen add
* Ex. Usage: `python3 controller.py --configure 64,65,66,67 -sen add

`-sen rm <sensor ID to remove>` : Removes a sensor from the given node. If you specifiy multiple nodes in this command, the sensor will be removed on each node, **provided the sensor with the corresponding ID exists**. If it doesn't exist, no worries! Nothing bad will happen.
* Ex. Usage: `python3 controller.py --configure 68 -sen rm 01` -> Sensor 01 gets removed from node with ID 68.
* Ex. Usage: `python3 controller.py --configure 69, 70 -sen rm 01` -> Sensor 01 gets removed from nodes with ID's 69 & 70.

`-sen dis <sensor ID to disable>` : Disables the selected sensor. If you specify multiple sensors using this command, all sensors specified will be affected. 
* **THIS DOES NOT WORK FOR MULTIPLE NODES AS OF VERISON 1, AND WILL BE ADDED LATER.** 
* Ex. Usage, **Given node 71 with sensor with ID 0 exists**: `python3 controller.py --configure 71 -sen dis 0`


`-sen en <sensor ID to disable>` : Enables the selected sensor. If you specify multiple sensors using this command, all sensors specified will be affected. 
* **THIS DOES NOT WORK FOR MULTIPLE NODES AS OF VERISON 1, AND WILL BE ADDED LATER.** 
* Ex. Usage, **Given node 72 with sensor with ID 0 exists**: `python3 controller.py --configure 72 -sen en 0`

`-sen freq [sensing frequency in seconds] <sensor ID to affect>` : Changes the frequency of sensing for the selected sensor.
* Ex. Usage, **Given node 73 with sensor with ID 0 exists**: `python3 controller.py --configure 73 -sen freq 45 0`
