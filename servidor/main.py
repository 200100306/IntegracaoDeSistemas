import multiprocessing
import os
import time
import subprocess

def iniciar_rest():
    os.system("python3 rest/rest_api.py")


def iniciar_soap():
    os.system("python3 soap/soap_api.py")


def iniciar_graphql():
    os.system("python3 graphql/graphql_api.py")

def iniciar_grpc():
    os.system("python3 grpc/grpc_api.py")

def iniciar_client():
    os.system("python3 ../clientWeb/main.py")
    
if __name__ == "__main__":
    print("Inicializando os serviços...")

    # Iniciar cada serviço num processo separado
    processos = [
        multiprocessing.Process(target=iniciar_rest),
        multiprocessing.Process(target=iniciar_soap),
        multiprocessing.Process(target=iniciar_graphql),
        multiprocessing.Process(target=iniciar_grpc),
        multiprocessing.Process(target=iniciar_client),
    ]

    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()