# ONION-NETWORK-P2P-CHAT

## Programming language
- Python
  - version 3
  
## Data format
- JSON

## Technologies
- [P2P network application architecture](https://en.wikipedia.org/wiki/Peer-to-peer)
- [Public and private key system](https://en.wikipedia.org/wiki/Public-key_cryptography)
  - [RSA algorithm](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Onion network](https://en.wikipedia.org/wiki/Onion_routing)

## How does it work?
![Graph 1](https://github.coventry.ac.uk/ribeiro7/GROUP1-ONION-NETWORK-P2P-CHAT/blob/master/img/how-does-it-works.jpg?raw=true)

1. The data is sent via p2p network application architecture

2. When you send a message it will be sent through each node to all the connected clients to the chat

3. Each node will decrypt the data using their private key

## How is the data encrypted?
- To decrypt and encrypt the data we will use the public and private key system.

## What's needed?

- Beaglebones to encrypt and decrypt the data
- Clients - computers that will be using the p2p chat


## How to get it working
- Download the [client.py](https://pages.github.com/) and connect to the ip of the desired chat
- Download the [node.py](https://pages.github.com/) and leave it running into the nodes 

## Example
- Data is sent from:
  - client 1
    - will encrypt the data using nodes and client public key
      - 1 layer - encrypt with client 2 public key
      - 2 layer - encrypt with node 2 public key
      - 3 layer - encrypt with node 1 public key
  - client 1 to node 1
    - node 1 will decrypt the data using their private key
  - node 1 to node 2
    - node 2 will decrypt the data using their private key
  - node 2 to client 2
    - client 2 will decrypt the data using their private key
      
`having more nodes will make the data more secure but also will consume more memory`

- the message is sent in a random node order every time

#### example of data used: 
> example with the data unencrypted
``` 
{
      "package": {
          "IP": "192.0.0.25",
          "username": "Casimiro",
          "message": "Hello I'm Casimiro"
      }
}
```

> data send when the client gets connected to the server
```
{
    "auth": {
        "ip": "192.168.0.12",
        "username": "casimiro",
        "publicKey": "as12f3aga"
    }
}
```

what will appear in the chat when you're connected:  
`Casimiro joined the chat`

what will appear in the chat:  
`Casimiro - Hello I'm Casimiro`

what will the clients save:
```
{
    "nodes": {
        "node": {
            "IP": "192.0.0.1",
            "Public key":   "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMkf8weHg+fLz96jxKe+osDQg89dF+jm
                            9kqU0Xin4yLevpz3NT47Zng9Fo4f4DBpvrLHl61YZpoj/+/cpDyKlXECAwEAAQ=="
        }
        "node2": {
            "IP": "192.0.0.2",
            "Public key":   "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJO1yW4OqwtTReDXSGLJ2L4nYc5Yk+d9
                            yiS0u2D7Q4K2ee6UZja+wY57yfQHDKzecOaE8oc9q42Xd1JWpIFxP+ECAwEAAQ=="
        }
    }
    "clients": {
        "John": {
            "IP": "192.0.0.168",
            "Public key":   "MFswDQYJKoZIhvcNAQEBBQADSgAwRwJAV2jg0T4xpn3Je7N4O7pa/fEvRZVcdN0m
                            i6GRRev2z79CKboCYpNJcr9uRSHDKzxkIWwk4OoKLfZN7uK06eAI0wIDAQAB"
        }
        "Jason": {
            IP: "192.0.0.126",
            "Public key":   "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKlplx3AsamSKWkbq/f16OpWOcPVph/q
                            KXxzxWJROYHfl8FNwTMOQjV+GFANd7LJUnze3xVnuHmBk+li2ZMYhtMCAwEAAQ=="
        }
        Barbara: {
            IP: 192.0.0.48,
            "Public key":   "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJrKH5Uwx/C8ZTUF2i/axPppkSphe593
                            lpQXs5R9xXAzCd/gJAp/O/ruD0MPRnP6HXnI4WR9Mxx8nWi5eKUQepsCAwEAAQ=="
        }
    }
}
```

## IMPORTANT
Each node has to have a static IP
