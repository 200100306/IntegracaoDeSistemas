# SOAP
## Install (Python)
1. install the specified packages into python with pip:
```shell 
pip install spyne 
```  
  or if the same venv for multiple servers just install using the requirements.txt
```shell
pip install -r requirements.txt
```

## Install Server (Docker)
1. If needed Build image
```shell
cd servidor
sudo docker build -t  ghcr.io/200100306/trabalhois:soap-server -f Dockerfile-soap . 
```
2. to start the container run the following command
```shell
docker run -d -p 8002:8002 --name soap_server ghcr.io/200100306/trabalhois:soap-server
```

## Run (Server)
1. To only run soap api instead of the whole stack (grpc, graphql, rest) execute:
```shell
cd servidor 
python soap_api.py
```
## Run (Cliente)
```shell
cd cliente
python soap_client.py
```

