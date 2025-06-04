import pika
import json

def publicar_evento(nome, descricao):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tarefas')
    mensagem = json.dumps({"evento": "nova_tarefa", "nome": nome, "descricao": descricao})
    channel.basic_publish(exchange='', routing_key='tarefas', body=mensagem)
    connection.close()
