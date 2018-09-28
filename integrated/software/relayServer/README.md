# Relay Server
Particle.io devices can only publish its data to the Particle.io cloud. As such, a separate module is used to send data from the Particle.io cloud to Argonnes Beehive server. The relayServer module is designed to manage this task.

## Usage  
A description of how the relay server module is implimented is given below:
- Obtaining Beehive Credentials:
  Before the implimentation of the python module the microWaggle users must obtain Beehive server Credentials from the Waggle team at Argonne.  These credentials can be requested through any of the following Waggle team members:
    - 
    - 

- Setting up the directory structure: 
For each Particle Device, the Waggle team will provide 3 files named 'node_id', 'Key.pem' and 'Cert.pem' which carry the necessary credentials for the Relay server module to connect to Beehive. These files should be put under the Unique directories defined by the respective Device IDs of each Particle.io microWaggle Device. An implimentation of the said file structure is given below:

```bash
├── parentDirectory
│   ├── relay-server.py
│   ├── microWaggleNodes
│   │   ├──53002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
│   │   ├──53002a000c24353432384231
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
│   │   ├──87002a000c51353432383931
│   │   │   ├──node_id
│   │   │   ├──Key.pem 
│   │   │   ├──Cert.pem
................
```
- Running the relay server module
Once the defined file sturture is set up, you can run the following command to send the appropriate data to Beehive. 
```python3 relay-server.py microWaggleNodes```
