import grpc
import items_pb2
import items_pb2_grpc
from google.protobuf.empty_pb2 import Empty

channel = grpc.insecure_channel('127.0.0.1:8003')  # Porta corrigida
stub = items_pb2_grpc.ItemServiceStub(channel)

def list_items():
    response = stub.GetItems(Empty())
    return [{"id": item.id, "name": item.name, "description": item.description} for item in response.items]

def create_item(name, description):
    response = stub.CreateItem(items_pb2.NewItemRequest(name=name, description=description))
    return {"id": response.id, "name": response.name, "description": response.description}

def delete_item(item_id):
    response = stub.DeleteItem(items_pb2.ItemRequest(id=item_id))
    return {"id": response.id, "name": response.name, "description": response.description}

if __name__ == "__main__":
    print("Cliente gRPC")

    item = create_item("Borracha", "Uma borracha branca")
    print("Criado:", item)

    items = list_items()
    print("Itens:")
    for i in items:
        print(i)

    if items:
        deleted = delete_item(items[0]["id"])
        print("Deletado:", deleted)

    print("Itens atualizados:")
    for i in list_items():
        print(i)
