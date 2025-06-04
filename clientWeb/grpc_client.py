import grpc
import items_pb2
import items_pb2_grpc

channel = grpc.insecure_channel('localhost:8003')
stub = items_pb2_grpc.ItemServiceStub(channel)

def list_items():
    response = stub.GetItems(items_pb2.Empty())
    return [{"id": item.id, "name": item.name, "description": item.description} for item in response.items]

def create_item(name, description):
    response = stub.CreateItem(items_pb2.ItemRequest(name=name, description=description))
    return {"id": response.id, "name": response.name}

def delete_item(item_id):
    stub.DeleteItem(items_pb2.ItemRequest(id=item_id))
