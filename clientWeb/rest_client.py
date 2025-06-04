import requests

BASE_URL = "http://127.0.0.1:8001"

def list_items():
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        items = response.json()
        print("Itens disponíveis:")
        for item in items:
            print(f"- ID: {item['id']}, Nome: {item['name']}, Descrição: {item['description']}")
        return items
    else:
        print("Erro ao obter os itens:", response.status_code, response.text)
        return []

def create_item(name, description):
    item = {"name": name, "description": description}
    response = requests.post(f"{BASE_URL}/items", json=item)
    if response.status_code == 200:
        data = response.json()
        print(f"Item criado: ID {data['id']}, Nome: {data['name']}")
    else:
        print("Erro ao criar item:", response.status_code, response.text)

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print(response.json()["message"])
    elif response.status_code == 404:
        print("Item não encontrado para deletar.")
    else:
        print("Erro ao deletar item:", response.status_code, response.text)

if __name__ == "__main__":
    print("REST Client")

    # Cria item
    create_item("Caneta", "Uma caneta azul")

    # Lista todos
    items = list_items()

    # Deleta o primeiro se existir
    if items:
        first_id = items[0]["id"]
        delete_item(first_id)

    # Lista novamente
    list_items()
