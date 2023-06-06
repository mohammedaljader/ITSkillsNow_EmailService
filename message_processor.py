import os
import json
from aio_pika import connect_robust, IncomingMessage
from email_sender import send_emails


async def process_message(message: IncomingMessage):
    async with message.process():
        body = message.body.decode()
        payload = json.loads(body)
        email = payload['userPayload']['email']
        username = payload['userPayload']['username']
        fullname = payload['userPayload']['fullName']
        send_emails(email, username, fullname)


async def start_listener():
    # Connect to RabbitMQ
    RabbitMQ_URL = os.getenv('RabbitMQ_URL')
    connection = await connect_robust(RabbitMQ_URL)

    # Create a channel
    channel = await connection.channel()

    # get a queue
    queue = await channel.get_queue("auth.queue")

    # Start consuming messages
    await queue.consume(process_message)
