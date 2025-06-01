from rabbitmq import RabbitMQ

def callback(ch, method, properties, body):
    print(f"Received {body}")

rabbitmq = RabbitMQ()
rabbitmq.consume(callback)