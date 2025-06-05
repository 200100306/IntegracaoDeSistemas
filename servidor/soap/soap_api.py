from spyne import Application, rpc, ServiceBase, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import json
import os

# Caminho seguro para o arquivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.json")

# Modelo de Item usado nas respostas
class Item(ComplexModel):
    id = Unicode
    name = Unicode
    description = Unicode

class SOAPService(ServiceBase):

    @rpc(_returns=Iterable(Item))
    def get_items(ctx):
        try:
            with open(DATABASE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"items": []}

        for item in data.get("items", []):
            yield Item(
                id=item.get("id", ""),
                name=item.get("name", ""),
                description=item.get("description", "")
            )

    @rpc(Unicode, _returns=Item)
    def get_item(ctx, id):
        try:
            with open(DATABASE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"items": []}

        for item in data.get("items", []):
            if item.get("id") == id:
                return Item(
                    id=item["id"],
                    name=item["name"],
                    description=item["description"]
                )

        return Item(id="N/A", name="Não encontrado", description="Item não existe.")

    @rpc(Unicode, Unicode, _returns=None)
    def create_item(ctx, itemName, itemDescription):
        try:
            with open(DATABASE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"items": []}

        # Geração de ID sequencial como string
        if data["items"]:
            try:
                last_id = max(int(item["id"]) for item in data["items"] if item["id"].isdigit())
            except ValueError:
                last_id = 0
            next_id = str(last_id + 1)
        else:
            next_id = "1"

        item = {
            "id": next_id,
            "name": itemName,
            "description": itemDescription
        }

        data["items"].append(item)

        with open(DATABASE, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

    @rpc(Unicode, _returns=Unicode)
    def delete_item(ctx, id):
        try:
            with open(DATABASE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return "Erro ao ler o banco de dados."

        updated_items = [item for item in data["items"] if item.get("id") != id]

        if len(updated_items) == len(data["items"]):
            return "Item não encontrado."

        data["items"] = updated_items

        with open(DATABASE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return "Item deletado com sucesso."

# Criação da aplicação SOAP
app = Application(
    [SOAPService],
    tns='spyne.soap_api',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(app)

# Inicialização do servidor
if __name__ == '__main__':
    print("SOAP server running at: http://192.168.246.55:8002/?wsdl")
    server = make_server('0.0.0.0', 8002, wsgi_app)
    server.serve_forever()
