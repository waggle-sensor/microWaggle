# Relay Server
Particle.io devices can only publish its data to the Particle.io cloud. As such, a separate module is used to send data from the Particle.io cloud to Argonnes Beehive server. The relayServer module is designed to manage this task.

## Prerequisites

- Obtaining Beehive Credentials:
  Before the implimentation of the python module the microWaggle users must obtain Beehive server Credentials from the Waggle team at Argonne.  These credentials can be requested through any of the following Waggle team members:

- Setting up the directory structure: 
For each Particle.io device, the Waggle team will provide 4 files named 'node_id', 'cacert.pem', 'key.pem' and 'cert.pem' which carry the necessary credentials for the relayServer module to connect to Beehive. These files should be put under the Unique directories defined by the respective Device IDs of each Particle.io microWaggle Device. An implimentation of the said file structure is given below:

```bash
├── parentDirectory
│   ├── relay-server.py
│   ├── devices
│   │   ├──53002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──cacert.pem
│   │   │   ├──key.pem 
│   │   │   ├──cert.pem
│   │   ├──53002a000c24353432384231
│   │   │   ├──node_id
│   │   │   ├──cacert.pem
│   │   │   ├──key.pem 
│   │   │   ├──cert.pem
│   │   ├──87002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──cacert.pem
│   │   │   ├──key.pem 
│   │   │   ├──cert.pem
................
```
## First time usage: 
- Run `relay-server.py` with no args. -> `python3 relay-server.py`. The`--help` prompt gives you the basic options that the controller provides.
- On its initial run`controller.py` will create `nodeConfig.json` and the `rela-log.txt` file.
    - `nodeConfig.json` : Once this file is created, copy and paste the access token of your particle.io to this file. The module will access this file each time it is implimented. 
    -  `relay-log.txt`  : This file will keep a log of all data coming out of the Particle.io nodes descibed by the file structure setup on the previous step.
 
## Implimenting the relayServer     
In completion of the previous steps are completed, run the command ```python3 relay-server.py ``` to send data from your devices to the Beehive Server. Once this command is ran, it will display data being recieved from the Particle.io cloud on the CLI. To further verify if the data is being sent to the Beehive server please contact the Wagge Team at Argonne National Labs.   

**Special Note: Particle.io does not store the data on its cloud. As such, make sure to run the releayServer module appropriately to avoid data loss** 
