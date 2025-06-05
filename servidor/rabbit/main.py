import pika

class RabbitMQ:
    def __init__(self, host='192.168.246.55:5672'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='minha_fila')

    def publish(self, mensagem):
        self.channel.basic_publish(exchange='', routing_key='minha_fila', body=mensagem)
        print("✅ Mensagem enviada:", mensagem)

    def consume(self, callback):
        self.channel.basic_consume(queue='minha_fila', on_message_callback=callback, auto_ack=True)
        print("🕒 A ouvir mensagens...")
        self.channel.start_consuming()
