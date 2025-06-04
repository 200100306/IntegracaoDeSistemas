import requests

GRAPHQL_URL = "http://localhost:8004/graphql"

def graphql_query(query, variables=None):
    response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro na requisição GraphQL:", response.text)
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
    if result:
        items = result.get("data", {}).get("getItems", [])
        print("Itens disponíveis:")
        for item in items:
            print(f"- ID: {item['id']}, Nome: {item['name']}, Descrição: {item['description']}")

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
    if result:
        item = result.get("data", {}).get("createItem")
        print(f"Item criado: ID {item['id']}, Nome: {item['name']}")

def delete_item(item_id):
    mutation = """
    mutation($id: String!) {
      deleteItem(id: $id)
    }
    """
    variables = {"id": item_id}
    result = graphql_query(mutation, variables)
    if result:
        print(result.get("data", {}).get("deleteItem"))

if __name__ == "__main__":
    print("GraphQL Client")
    create_item("Lápis", "Um lápis preto")
    list_items()
    delete_item("1")
    list_items()
