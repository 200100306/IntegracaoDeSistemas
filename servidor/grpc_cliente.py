import grpc
import items_pb2
import items_pb2_grpc
from google.protobuf.empty_pb2 import Empty

def run():
    # Conectar ao servidor gRPC
    channel = grpc.insecure_channel("localhost:50051")  # Substitua pelo IP correto, se necessário
    stub = items_pb2_grpc.ItemServiceStub(channel)

    # Testar o método GetItems
    print("Testando GetItems...")
    try:
        response = stub.GetItems(Empty())
        print("Itens recebidos:")
        for item in response.items:
            print(f"ID: {item.id}, Nome: {item.name}, Descrição: {item.description}")
    except grpc.RpcError as e:
        print(f"Erro ao chamar GetItems: {e.details()}")

    # Testar o método CreateItem
    print("\nTestando CreateItem...")
    new_item = items_pb2.NewItemRequest(name="Item Teste", description="Descrição do Item Teste")
    try:
        created_item = stub.CreateItem(new_item)
        print(f"Item criado: ID={created_item.id}, Nome={created_item.name}, Descrição={created_item.description}")
    except grpc.RpcError as e:
        print(f"Erro ao chamar CreateItem: {e.details()}")

    # Testar o método DeleteItem
    print("\nTestando DeleteItem...")
    item_request = items_pb2.ItemRequest(id="1")  # Substitua pelo ID do item que deseja deletar
    try:
        deleted_item = stub.DeleteItem(item_request)
        print(f"Item deletado: ID={deleted_item.id}, Nome={deleted_item.name}, Descrição={deleted_item.description}")
    except grpc.RpcError as e:
        print(f"Erro ao chamar DeleteItem: {e.details()}")

if __name__ == "__main__":
    run()