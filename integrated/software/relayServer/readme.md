# Relay Server
Particle.io devices can only publish their data to the Particle.io Cloud. As such, a separate module is used to send data from the Particle.io cloud to the Waggle Beehive server at Argonne National Laboratory (ANL). The relayServer module manages this task.

## Configuration

* Obtain Beehive credentials:
  Before the implementation, micro-Waggle users must obtain Beehive server credentials from the Waggle team at ANL.

* Setting up the directory structure:
For each Particle.io device, the Waggle team will provide 4 files named 'node_id', 'cacert.pem', 'key.pem' and 'cert.pem' which carry the necessary credentials for the relayServer module to connect to Beehive. Each device should have its own directory on the machine running the relayServer, named after the Particle.io Device ID and containing only these four files. An example of this file structure is given below:

```
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

* Add access tokens

Access tokens are stored in `relay-config.txt` with one access token per line.

```
6162a1ea17d65b9e0d2ede5cc728a116ea5c3a86
8ef5574ba6ff9e3790947b0af6fccb93a5a00f5b
2b7e2c30d254731a8c5a6c67e5bf4d57f711640a
...
```

A process will be run for each access token which forwards its devices.

## First time usage:
- Run `relay-server.py` with no args. -> `python3 relay-server.py`. The`--help` prompt gives you the basic options that the controller provides.
- On its initial run`controller.py` will create `nodeConfig.json` and the `relay-log.txt` file.
    - `nodeConfig.json` : Once this file is created, copy and paste the access token of your Particle account to this file. The module will access this file each time it is implemented.
    -  `relay-log.txt`  : This file will keep a log of all data coming out of the Particle.io nodes descibed by the file structure setup on the previous step.

## Implementing the relayServer
Upon completion of the previous steps, run the command ```python3 relay-server.py ``` to send data from your devices to the Beehive Server. Once this command is executed, the module will display the data being recieved from the Particle.io cloud in the terminal. To further verify that the data is being sent to the Beehive server please contact the Waggle Team at ANL for access to the most updated data portal.

**Special Note: Particle.io does not store the data on its cloud. As such, make sure to run the releayServer module appropriately to avoid data loss**
