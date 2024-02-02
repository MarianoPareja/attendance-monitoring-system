import pika


class RabitMQConnection:
    def __init__(self, host: str, exchange: str, exchange_type: str):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

        # Declare queue
        self.result = self.channel.queue_declare(queue="emb_queue", exclusive=True)
        self.channel.queue_bind(
            exchange=self.exchange, queue="emb_queue", routing_key="embeddings"
        )

    def post_message(self, data, routing_key="embeddings"):
        """
        data: json serialized data
        """
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=data,
        )

    def consume_messages(self, callback_fn):
        self.channel.basic_consume(
            queue="emb_queue", on_message_callback=callback_fn, auto_ack=True
        )
        self.channel.start_consuming()
