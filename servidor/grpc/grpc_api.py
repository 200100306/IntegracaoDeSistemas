import grpc
from concurrent import futures
import json
import os
import items_pb2
import items_pb2_grpc
from google.protobuf.empty_pb2 import Empty

# Caminho seguro para o arquivo JSON
BASE_DIR = os.path.dirname(__file__)
DATABASE = os.path.join(BASE_DIR, "database.json")

def load_data():
    try:
        with open(DATABASE, "r") as file:
            content = file.read().strip()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)

class ItemService(items_pb2_grpc.ItemServiceServicer):
    def GetItems(self, request, context):
        data = load_data()
        items = [
            items_pb2.ItemResponse(id=item_id, name=item["name"], description=item["description"])
            for item_id, item in data.items()
        ]
        return items_pb2.ItemList(items=items)

    def CreateItem(self, request, context):
        data = load_data()
        item_id = str(len(data) + 1)
        new_item = {"name": request.name, "description": request.description}
        data[item_id] = new_item
        save_data(data)
        return items_pb2.ItemResponse(id=item_id, name=request.name, description=request.description)

    def DeleteItem(self, request, context):
        data = load_data()
        if request.id in data:
            deleted_item = data.pop(request.id)
            save_data(data)
            return items_pb2.ItemResponse(id=request.id, name=deleted_item["name"], description=deleted_item["description"])
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Item não encontrado")
        return items_pb2.ItemResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    items_pb2_grpc.add_ItemServiceServicer_to_server(ItemService(), server)
    server.add_insecure_port("[::]:8003")  # Porta corrigida para 8003
    server.start()
    print("Servidor gRPC iniciado em 192.168.246.55:8003")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
