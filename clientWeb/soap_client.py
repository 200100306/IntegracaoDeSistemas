from zeep import Client

client = Client(wsdl="http://127.0.0.1:8002/?wsdl")

def list_items():
    items = client.service.get_items()
    return [{"id": i.id, "name": i.name, "description": i.description} for i in items]

def create_item(name, description):
    # ID não é necessário — o servidor gera automaticamente
    client.service.create_item(name, description)

def delete_item(item_id):
    return client.service.delete_item(item_id)
