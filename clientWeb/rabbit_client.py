import pika
import json

def publicar_evento(nome, descricao):
    try:
        connection = pika.ConnectionParameters(host='localhost', port=5672)
        channel = connection.channel()
        channel.queue_declare(queue='tarefas')
        mensagem = json.dumps({"evento": "nova_tarefa", "nome": nome, "descricao": descricao})
        channel.basic_publish(exchange='', routing_key='tarefas', body=mensagem)
        connection.close()
        print("✅ Mensagem publicada no RabbitMQ")
    except Exception as e:
        print("❌ Erro ao publicar no RabbitMQ:", e)
