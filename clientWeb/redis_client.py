import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def publicar_evento(nome, descricao):
    evento = {"evento": "nova_tarefa", "nome": nome, "descricao": descricao}
    r.publish("tarefas", json.dumps(evento))
