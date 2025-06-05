from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import uuid
import os

app = FastAPI()

# Caminho seguro para o arquivo JSON
BASE_DIR = os.path.dirname(__file__)
DATABASE = os.path.join(BASE_DIR, "database.json")


# Função para carregar dados
def load_data():
    try:
        with open(DATABASE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"items": []}

# Função para salvar dados
def save_data(data):
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)

# Modelo de entrada
class Item(BaseModel):
    name: str
    description: str

# Rota GET - listar todos os itens
@app.get("/items")
def get_items():
    data = load_data()
    return data["items"]

# Rota POST - criar novo item
@app.post("/items")
def create_item(item: Item):
    data = load_data()

    # Geração de ID sequencial como string
    if data["items"]:
        try:
            last_id = max(int(i["id"]) for i in data["items"] if i["id"].isdigit())
        except ValueError:
            last_id = 0
        next_id = str(last_id + 1)
    else:
        next_id = "1"

    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description
    }

    data["items"].append(new_item)
    save_data(data)

    return new_item

# Rota DELETE - apagar item pelo ID
@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    data = load_data()
    original_length = len(data["items"])

    # Filtra todos os itens que não têm o ID fornecido
    data["items"] = [item for item in data["items"] if item["id"] != item_id]

    if len(data["items"]) == original_length:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    save_data(data)
    return {"message": "Item deletado com sucesso"}

# Execução direta
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rest_api:app", host="192.168.246.55", port=8001, reload=True)
