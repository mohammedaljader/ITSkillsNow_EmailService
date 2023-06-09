import os
import json
from retry import retry
import asyncio
from aio_pika import connect_robust, IncomingMessage
from email_sender import send_emails


async def process_message(message: IncomingMessage):
    async with message.process():
        body = message.body.decode()
        print(body)
        payload = json.loads(body)
        email = payload['email']
        subject = payload['subject']
        fullname = payload['fullName']
        code = payload['otpCode']
        message = payload['message']
        send_emails(email, subject, message, code , fullname)

@retry(delay=5, backoff=2, max_delay=60)
async def start_listener_retry():
    # Connect to RabbitMQ
    rabbitmq_host = os.getenv('RABBITMQ_HOST')
    rabbitmq_url = f'amqp://{rabbitmq_host}:{5672}'
    connection = await connect_robust(rabbitmq_url)

    # Create a channel
    channel = await connection.channel()

    # get a queue
    queue = await channel.get_queue("auth_message_queue")

    # Start consuming messages
    await queue.consume(process_message)


async def start_listener():
    while True:
        try:
            await start_listener_retry()
            break
        except Exception as e:
            print(f"Failed to connect to RabbitMQ. Retrying in 5 seconds... {str(e)}")
            await asyncio.sleep(5)
