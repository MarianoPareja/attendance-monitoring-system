import pika


class RabitMQConnection:
    def __init__(self, host: str, exchange: str, exchange_type: str):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    def post_message(self, data, routing_key="embeddings"):
        """
        data: json serialized data
        """
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=data,
        )
