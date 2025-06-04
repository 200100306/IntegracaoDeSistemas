import requests

GRAPHQL_URL = "http://127.0.0.1:8004/graphql"

def graphql_query(query, variables=None):
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={'query': query, 'variables': variables},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Erro na requisição GraphQL:", e)
        return None

def list_items():
    query = """
    query {
      getItems {
        id
        name
        description
      }
    }
    """
    result = graphql_query(query)
    print("DEBUG LIST RESULT:", result)

    if result and "data" in result:
        items = result["data"].get("getItems", [])
        if items:
            print("\n📦 Itens disponíveis:")
            for item in items:
                print(f" - ID: {item['id']}, Nome: {item['name']}, Descrição: {item['description']}")
        else:
            print("\n📭 Nenhum item encontrado.")
    else:
        print("\n⚠️ Erro ao recuperar itens.")
        if result and "errors" in result:
            print("Detalhes:", result["errors"])

def create_item(name, description):
    mutation = """
    mutation($name: String!, $description: String!) {
      createItem(name: $name, description: $description) {
        id
        name
        description
      }
    }
    """
    variables = {"name": name, "description": description}
    result = graphql_query(mutation, variables)

    if result and "data" in result:
        item = result["data"]["createItem"]
        print(f"\n✅ Item criado: ID {item['id']}, Nome: {item['name']}")
    else:
        print("\n❌ Erro ao criar item.")
        if result and "errors" in result:
            print("Detalhes:", result["errors"])

def delete_item(item_id):
    mutation = """
    mutation($id: String!) {
      deleteItem(id: $id)
    }
    """
    variables = {"id": item_id}
    result = graphql_query(mutation, variables)

    if result and "data" in result:
        print(f"\n🗑️ {result['data']['deleteItem']}")
    else:
        print("\n❌ Erro ao apagar item.")
        if result and "errors" in result:
            print("Detalhes:", result["errors"])

# Testes de demonstração
if __name__ == "__main__":
    print("🧪 CLIENTE GRAPHQL - Testando operações...")

    create_item("Lápis", "Um lápis preto")
    list_items()
    delete_item("1")
    list_items()
