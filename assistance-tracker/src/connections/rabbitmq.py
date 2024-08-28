import logging
import time

import pika
import pika.exceptions

logger = logging.getLogger("pika")


class RabbitMQConnection:
    def __init__(self, host: str, exchange: str, exchange_type: str):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.heartbeat_interval = 60

        # Intialize connection object
        while True:
            try:
                print("Connecting to RabbitMQ Server")
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.host, heartbeat=self.heartbeat_interval
                    )
                )
                print("Connected to RabbitMQ successfully")
                break

            except pika.exceptions.AMQPConnectionError as e:
                print("Error when connecting to RabbitMQ host %s", self.host)
                print("Retrying connection in 3 seconds...")
                time.sleep(3)

    def connect(self):
        """
        Connect to RabbitMQ Server
        """
        try:
            logger.info("connecting to RabbitMQ Server")
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host, heartbeat=self.heartbeat_interval
                )
            )

            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=self.exchange, exchange_type=self.exchange_type
            )

            # Declare queue
            self.result = self.channel.queue_declare(
                queue="emb_queue", exclusive=False, durable=False
            )
            self.channel.queue_bind(
                exchange=self.exchange, queue="emb_queue", routing_key="embeddings"
            )
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Error when connecting to rabbitMQ host %s", self.host)

    def post_message(self, data, routing_key="embeddings"):
        """
        Send message to broker

        :param data: JSON serialized data
        """

        while not self.connection.is_open:
            try:
                self.connect()
            except pika.exceptions.AMQPConnectionError as e:
                logger.info("Retrying connection in 3 seconds...")
                time.sleep(3)

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=data,
        )

    def consume_messages(self, callback_fn):

        while not self.connection.is_open:
            try:
                self.connect()
            except pika.exceptions.AMQPConnectionError as e:
                logger.info("Retrying connection in 3 seconds...")
                time.sleep(3)

        self.channel.basic_consume(
            queue="emb_queue", on_message_callback=callback_fn, auto_ack=True
        )
        self.channel.start_consuming()
