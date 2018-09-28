# DeviceController

The device controller module gives users of microWaggle nodes a form of remote user control. The module is capable of changing frequencies of reading and publishing data as well as enabling & disabling of device sensors. 
 
## Micro-Waggle deviceController CLI guide

The device controller module lets you manage a microWaggle node network through a CLI. It should be noted that the **access tokens** and the unique **device IDs** privided by Particle.io needs to be at hand before the implimentation of the module. 

## First time usage: 
- Run `controller.py` with no args. -> `python3 controller.py`. The`--help` prompt gives you the basic options that the controller provides.
- On its initial run`controller.py` will create `nodeConfig.json` file which keeps the node configuration the user intends to have. Everytime the module is implimented, it will seek to mimic the configuration defined on `nodeConfig.json`on the actual microWaggle network.  

### Local Node Configuration
The command  `python3 controller.py --add` is intened to be used in adding new nodes to the local configuration file. An example usage of the said command is given below:
<img src="https://raw.githubusercontent.com/waggle-sensor/microWaggle/master/integrated/software/deviceController/resources/images/add.png" width="700">

As the diagram indicates the user will be prompted to provide the following details for a given node:
- Node Name : User defined name for the intened microWaggle node **(Cannot have spaces)**
- Node ID   : User defined name for the intened microWaggle node **(Cannot have spaces)**
- Device ID : The Device ID provided by Particle.io for the intened node
- Data Publish Frequency : The frequency in which sensor data should be published to the Particle.io cloud
- Status Publish Frequency: The frequency in which node status data should be published to the Particle.io cloud
- Access Token : The access token provided by Particle.io for the intened node
- Use the default Micro-waggle Config: The desired configuration of the sensors present on the node. **First time users are recommended to keep the default microWaggle Configuration**. If you choose to keep a diffent configuration the following information needs to be provided.
- Number of Sensors to be added : The number of sensors present in the actual microWaggle code 
- Names of each sensor : Use specified names for each sensor **(Cannot have spaces)**
- ID for sensor : The sensor ID's specified on the firmware of the microWaggle device for the intended sensor **(Cannot have spaces)**
- Enabled for sensor : State wheather the sensor is enabled or disabled on the specific sensor
- Sensing Frequency for sensor : State how often the sensor needs to read data
An example usage of the prompt is given below.
<img src="https://github.com/waggle-sensor/microWaggle/blob/master/integrated/software/deviceController/resources/images/userDefined.png" width="700">

Once a local configuration is set `python3 controller.py --list` command can be used to verify the intened configuration. An example configuration is given below:
<img src="https://github.com/waggle-sensor/microWaggle/blob/master/integrated/software/deviceController/resources/images/list.png" width="700">

## Basic use cases

- `--help` : Lists all commands, as well as their respective syntaxes and functions.
   - Ex. Usage: `python3 controller.py --help` 

- `--list`: Lists all nodes present on the local config file. The respective information such as nodeID and deviceID, and sensor configuration will also be displayed.
  - Ex. Usage: `python3 controller.py --list`

- `--enAll` : Enables all sensors on on all nodes.
   - Ex. Usage: `python3 controller.py --enAll`

- `--disAll` : Disables all sensors on all nodes.
   - Ex. Usage: `python3 controller.py --disAll`

- `--rm <nodeID>` : removes the node with the specified name
   - Ex. Usage: **Given a node with nodeID 33 exists** : `python3 controller.py --rm <nodeID>`

- `--add` : Starts the prompt to add a new node.
   - Ex. Usage: `python3 controller.py --add`

- `--configure <nodeID> [-rn/-id/-d/-e/-sdf/-ssf/-sm/-sd/-sen]`
   - Ex. Usage: **See below**

## The 'configure' command

The configure command lets you remotely control your nodes and there sensors after the intended nodes is included on the local config file. 

- `-rn <new name>` : Renames the entered node.
  **NODE NAMES CANNOT HAVE SPACES!**
  - Ex. Usage: **Given a node with the nodeID 33 exists**: `python3 controller.py --configure 33 -rn bar` -> Node 33 is now named bar.
  - Ex. Usage: **Given nodes with the nodeID 33, 99, and 66 exist**: `python3 controller.py --configure 33,66,99 -rn Field_node` -> nodes with the nodeID 33, 66, and 99 are now named "Field_node".

- `-id <new nodeID>` : changes the nodeID of the entered node. 
  - Ex. Usage: **Given a node with the nodeID 33 exists**: `python3 controller.py --configure 33 -id 96024` -> Node with ID 33 now has the nodeID 96024.
 **ANY CHANGES DONE TO A NODE WITH A SPECIFIED ID WILL BE DONE TO ALL NODES WITH THE MATCHING ID.**

- `-d` : Disables all sensors on the given node. Can disable all sensors on more than one node at once if the nodeID's are separated by a comma. Example usage:
  - Ex. Usage: **Given a node with the nodeID 34 exists**: `python3 controller.py --configure 34 -d` -> Node with ID 34 is disabled.
  - Ex. Usage: **Given nodes with the nodeID 35, 36, 37, & 38 exist**: `python3 controller.py --configure 35,36,37,38 -d` -> Sensors on nodes with ID 35, 36, 37, & 38 are disabled.

- `-e` : Enables all sensors on the given node. Can enable all sensors on more than one node at once if the nodeID's are separated by a comma. Example usage:
  - Ex. Usage: **Given a node with the nodeID 34 exists**: `python3 controller.py --configure 34 -e` -> Node with ID 34 is enabled.
  - Ex. Usage: **Given nodes with the nodeID 39, 40, 41, & 42 exist**: `python3 controller.py --configure 39,40,41,42 -e` -> Sensors on nodes with ID 39, 40, 41, & 42 are enabled.

- `-sdf` : Changes the frequency at which the selected node sends data. Can change multiple node's setting if nodeID's are separated by a comma. Example usage:
  - Ex. Usage: **Given a node with the nodeID 43 exists**: `python3 controller.py --configure 43 -sdf 15` -> Node with ID 43 now has a sending frequency of 15 seconds. 
  - Ex. Usage: **Given nodes with the nodeID 44, 45, and 46 exist**: `python3 controller.py --configure 44,45,46 -sdf 15` -> Nodes ID 44, 45, & 46 now have a sending frequency of 15 seconds. 

- `-nsf` : Changes the frequency at which the selected node sends status messages. Can change multiple node's setting if nodeID's are separated by a comma. Example usage:
  - Ex. Usage: **Given a node with the nodeID 43 exists**: `python3 controller.py --configure 43 -sdf 15` -> Node with ID 43 now has a status publish frequency of 15 seconds. 
  - Ex. Usage: **Given nodes with the nodeID 44, 45, and 46 exist**: `python3 controller.py --configure 44,45,46 -sdf 15` -> Nodes ID 44, 45, & 46 now have a status publish frequency of 15 seconds. 

- `-ssf `: Changes the frequency at which the selected node senses data(for all sensors). Can change multiple node setting if nodeID's are separated by a comma. Example usage below.
  - Ex. Usage: **Given a node with the nodeID 47 exists**: `python3 controller.py --configure 47 -ssf 15` -> Node with ID 47 now has a sensing frequency of 15 seconds. 
  - Ex. Usage: **Given nodes with the nodeID 48, 49, and 50 exist**: `python3 controller.py --configure 44,45,46 -ssf 15` -> Nodes ID 48, 49, & 50 now have a sensing frequency of 15 seconds.

- `-sd <True/False>` : Sets if the node should save data to SD storage when disconnected from Wi-Fi. True = Yes, False = No. You can use this command on multiple nodes, provided there's a comma in between the nodeIDs. Example usage below. 
  - Ex. Usage: `python3 controller.py --configure 57 -sd True` -> Node with the ID 51 will store to SD.
  - Ex. Usage: `python3 controller.py --configure 58,59,60,61,62 -sm False` -> Node with the IDs 58, 59, 60, 61, & 62 will not save to SD storage.

### The 'sen configure' commmand

The `-sen` subcommand of the `--configure` command lets the users configure individual sensors on microWaggle nodes.

- `-sen add` : Adds a new sensor to the the given node via a user command prompt. If you specify multiple nodes in this command, the sensor form you fill out will be applied to **all** nodes specified. 
   - Ex. Usage: `python3 controller.py --configure 63 -sen add
   - Ex. Usage: `python3 controller.py --configure 64,65,66,67 -sen add

- `-sen rm <sensor ID to remove>` : Removes a sensor from the given node. If you specifiy multiple nodes in this command, the sensor will be removed on each node, **provided the sensor with the corresponding ID exists**.
   - Ex. Usage: `python3 controller.py --configure 68 -sen rm 01` -> Sensor 01 gets removed from node with ID 68.
   - Ex. Usage: `python3 controller.py --configure 69, 70 -sen rm 01` -> Sensor 01 gets removed from nodes with ID's 69 & 70.

- `-sen dis <sensor ID to disable>` : Disables the selected sensor. If you specify multiple sensors using this command, all sensors specified will be affected. 
   - Ex. Usage: **Given node 71 with sensor with ID 0 exists**: `python3 controller.py --configure 71 -sen dis 0`

- `-sen en <sensor ID to disable>` : Enables the selected sensor. If you specify multiple sensors using this command, all sensors specified will be affected. 
   - Ex. Usage: **Given node 72 with sensor with ID 0 exists**: `python3 controller.py --configure 72 -sen en 0`

- `-sen freq [sensing frequency in seconds] <sensor ID to affect>` : Changes the frequency of sensing for the selected sensor.
   - Ex. Usage: **Given node 73 with sensor with ID 0 exists**: `python3 controller.py --configure 73 -sen freq 45 0`
