import pika

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar a fila
channel.queue_declare(queue='minha_fila')

# Função de callback para processar mensagens recebidas
def callback(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}")

channel.basic_consume(queue='minha_fila', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()
