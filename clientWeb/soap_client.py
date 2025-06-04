from zeep import Client

client = Client(wsdl="http://localhost:8002/?wsdl")

def list_items():
    items = client.service.get_items()
    # Converter para lista de dicionários compatível
    return [{"id": i.id, "name": i.name, "description": i.description} for i in items]

def create_item(name, description):
    # Gera um ID simples, ou pode ser do lado do servidor
    from uuid import uuid4
    item_id = str(uuid4())
    client.service.create_item(item_id, name, description)
