# ATTENDANCE MONITORING SYSTEM

This projects is a PoC (Proof of Concept) of a automated attendance control system for educactional institutions. It consists of multiple embedded systems that preprocess data before sending it to the server, to reduce the amount of data being sent (by extracting all detected faces and sending only the resized images of each face) 


<img src='./images/project_architecture.png' width=800px alt='Project Architecture'/>

## Directory Structure
As there are multiple microservices, there may be some difference between them, it was aimed to maintain a common based strcuture as shown below:

```
├── README.md               <- Top level README file  
├── Microservice            <- Microservice folder  
|   ├── manifests           <- Files that defines the configuration of Kubernetes resources  
|   ├── src                 <- Source code for use in the microservice  
|   ├── tests               <- Scripts for testing microservices  
|   ├── Dockerfile          <- File to build docker image  
|   ├── requirements.txt    <- The requirements file for installing all dependencies  
```


## Installation

The microservices were developed using: 
- Python 3.11.5

**Instalation using Docker Compose:** If you want to test the system without using Docker Compose instead of Kubernetes, you can run the following command: 

```bash
$ dockercopomse -up .
```

For testing each microservice, you can either: 
1. Build and run the Docker Image
```bash
build docker images 
run docker image
```

2. Install dependencies and run the main script 
python3 -m venv venv 
pip install -r requirements.txt
python main.py 