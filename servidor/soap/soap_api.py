from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import json
DATABASE = "database.json"

class SOAPService(ServiceBase):
    # GET get_items / returns - string with items currently on json
    @rpc( _returns=Unicode)
    def get_items(ctx):
        try:
            with open('database.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"items": []}
            print("COULD NOT FIND DATABASE ---------------------------")
            return
        ret=""
        for item in data['items']:
            ret += "|"
            ret+=str(item['id'])
            ret+="|"
            ret+=str(item['name'])
            ret += "|"
            ret+=str(item['description'])
            ret += "|"
            ret+="\n"
        print(ret, "-------------------------------------------------------")
        return ret
    # GET get_item / returns - string with item currently on json that has corresponding id
    @rpc(Unicode, _returns=Unicode)
    def get_item(ctx,id):
        try:
            with open('database.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"items": []}
            print("COULD NOT FIND DATABASE ---------------------------")
            return
        ret=""
        # data['items'].get(id)
        for item in data['items']:
            if item['id'] == id:
                ret += "|"
                ret+=str(item['id'])
                ret+="|"
                ret+=str(item['name'])
                ret += "|"
                ret+=str(item['description'])
                ret += "|"
                ret+="\n"
        if ret == "":
            return "Item nao existe"
        return ret

    # POST create / recieves items caracteristics (id, name, description) and adds the item into the json db
    @rpc(Unicode, Unicode, Unicode)
    def create_item(ctx,itemID,itemName,itemDescription):
        # Open Original JSON file
        try:
            with open('database.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"items":[]}
            print("COULD NOT FIND DATABASE ---------------------------")
        print("create_item", itemID, itemName, itemDescription)
        item = {
            'id': itemID,
            'name': itemName,
            'description': itemDescription,
        }
        data["items"].append(item)
        print(data)
        # Save data back to JSON file
        with open('database.json', "w") as outfile:
            json.dump(data, outfile, indent=4)


# Starts SOAP API SERVER ON PORT 8002

app = Application([SOAPService], 'spyne.soap_api',
in_protocol=Soap11(), out_protocol=Soap11())
wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    print("SOAP server running at: http://localhost:8002/?wsdl")
    server = make_server('0.0.0.0', 8002, wsgi_app)
    server.serve_forever()
