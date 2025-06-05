import requests

BASE_URL = "http://192.168.246.55:8001"

# Buscar todos os itens
def get_items():
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        print("Itens disponíveis:", response.json())
    else:
        print("Erro ao buscar itens:", response.status_code)

# Criar um novo item
def create_item(name, description):
    data = {"name": name, "description": description}
    response = requests.post(f"{BASE_URL}/items", json=data)
    if response.status_code == 200:
        print("Item criado:", response.json())
    else:
        print("Erro ao criar item:", response.status_code)

# Deletar um item
def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print("Item deletado:", response.json())
    else:
        print("Erro ao deletar item:", response.status_code)

# Testando as funções
if __name__ == "__main__":
    get_items()
    create_item("Novo Item", "Descrição do novo item")
    get_items()  # Verificar se o item foi adicionado
    delete_item("1")  # Substituir pelo ID correto
    get_items()  # Verificar se o item foi removido