from flask import Flask, render_template, request, redirect
import rest_client, soap_client, graphql_client, grpc_client
from google.protobuf.empty_pb2 import Empty

app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para listar itens de um dos serviços
@app.route('/<servico>/list_items')
def list_items(servico):
    try:
        if servico == 'rest':
            tarefas = rest_client.list_items()
        elif servico == 'soap':
            tarefas = soap_client.list_items()
        elif servico == 'graphql':
            tarefas = graphql_client.list_items()
        elif servico == 'grpc':
            tarefas = grpc_client.list_items()
        else:
            return f"Serviço '{servico}' inválido.", 400
    except Exception as e:
        return f"Erro ao listar tarefas via {servico}: {str(e)}", 500

    return render_template('index.html', tarefas=tarefas, servico=servico)

# Rota para criar um novo item
@app.route('/<servico>/criar', methods=['POST'])
def create_item(servico):
    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        return "Nome e descrição são obrigatórios!", 400

    try:
        if servico == 'rest':
           rest_client.create_item(name, description)
        elif servico == 'soap':
           soap_client.create_item(name, description)
        elif servico == 'graphql':
           graphql_client.create_item(name, description)
        elif servico == 'grpc':
           grpc_client.create_item(name, description)
        else:
          return f"Serviço '{servico}' inválido.", 400
    except Exception as e:
        return f"Erro ao criar tarefa via {servico}: {str(e)}", 500

    return redirect(f'/{servico}/list_items')

# Rota para apagar um item
@app.route('/<servico>/apagar', methods=['POST'])
def delete_item(servico):
    item_id = request.form.get('id')

    if not item_id:
        return "ID da tarefa é obrigatório!", 400

    try:
        if servico == 'rest':
            rest_client.delete_item(item_id)
        elif servico == 'soap':
            soap_client.delete_item(item_id)
        elif servico == 'graphql':
            graphql_client.delete_item(item_id)
        elif servico == 'grpc':
            grpc_client.delete_item(item_id)
        else:
            return f"Serviço '{servico}' inválido.", 400
    except Exception as e:
        return f"Erro ao apagar tarefa via {servico}: {str(e)}", 500

    return redirect(f'/{servico}/list_items')

# Inicialização da aplicação
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
