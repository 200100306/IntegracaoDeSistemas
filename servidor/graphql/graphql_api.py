import json
import os
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI

# Caminho seguro para o arquivo JSON
BASE_DIR = os.path.dirname(__file__)
DATABASE = os.path.join(BASE_DIR, "database.json")

# Carrega os dados do arquivo JSON
def load_data():
    try:
        with open(DATABASE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Salva os dados no arquivo JSON
def save_data(data):
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)

# Define o tipo Item para GraphQL
@strawberry.type
class Item:
    id: str
    name: str
    description: str

# Query do GraphQL para buscar itens
@strawberry.type
class Query:
    @strawberry.field(name="getItems")
    def get_items(self) -> list[Item]:
        data = load_data()
        return [Item(id=k, **v) for k, v in data.items()]

# Mutations do GraphQL: criar e deletar itens
@strawberry.type
class Mutation:
    @strawberry.mutation(name="createItem")
    def create_item(self, name: str, description: str) -> Item:
        data = load_data()
        item_id = str(len(data) + 1)
        new_item = {"name": name, "description": description}
        data[item_id] = new_item
        save_data(data)
        return Item(id=item_id, **new_item)

    @strawberry.mutation(name="deleteItem")
    def delete_item(self, id: str) -> str:
        data = load_data()
        if id in data:
            del data[id]
            save_data(data)
            return "Item deletado com sucesso"
        return "Item não encontrado"

# Criação do schema e inclusão no FastAPI
schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")

# Executa o servidor com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("graphql_api:app", host="0.0.0.0", port=8004, reload=True)
