import requests

BASE_URL = "http://127.0.0.1:8001"

def list_items():
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        items = response.json()
        print("Itens disponíveis:")
        for item_id, item in items.items():
            print(f"- ID: {item_id}, Nome: {item.get('name')}, Descrição: {item.get('description')}")
    else:
        print("Erro ao obter os itens.")

def create_item(name, description):
    item = {"name": name, "description": description}
    response = requests.post(f"{BASE_URL}/items", json=item)
    if response.status_code == 200:
        data = response.json()
        print(f"Item criado: ID {data['id']}, Nome: {data['item']['name']}")
    else:
        print("Erro ao criar item.")

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(response.json().get("error", "Erro ao deletar item."))

if __name__ == "__main__":
    print("REST Client")
    create_item("Caneta", "Uma caneta azul")
    list_items()
    delete_item("1")
    list_items()
