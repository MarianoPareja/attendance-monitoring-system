import pika
import pika.exceptions


class RabitMQConnection:
    def __init__(self, host: str, exchange: str, exchange_type: str):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.heartbeat_interval = 60

    def connect(self):
        """
        Connect to RabbitMQ server
        """
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                heartbeat=self.heartbeat_interval,
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type=self.exchange_type
        )

    def post_message(self, data, routing_key="embeddings"):
        """
        Sends data through class exchange

        Parameters:
        - data (str): Json serialized data

        Returns:
        No returns

        """
        if not self.connection.is_open:
            try:
                self.connect()
            except pika.exceptions.AMQPConnectionError as e:
                print("Error connecting to RabbitMQ server {}".format(e))

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=data,
        )
