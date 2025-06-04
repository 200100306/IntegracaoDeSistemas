import grpc
from concurrent import futures
import json
import items_pb2
import items_pb2_grpc
from google.protobuf.empty_pb2 import Empty
import time

DATABASE = "database.json"

def load_data():
    try:
        with open(DATABASE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
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
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    print("Servidor encerrado.")
