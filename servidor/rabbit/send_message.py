import pika

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar a fila
channel.queue_declare(queue='minha_fila')

# Enviar mensagem
channel.basic_publish(exchange='', routing_key='minha_fila', body='Olá, RabbitMQ!')

print("Mensagem enviada para 'minha_fila'!")

connection.close()
