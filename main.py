import asyncio

from fastapi import FastAPI
from aio_pika import connect, IncomingMessage

app = FastAPI()


async def process_message(message: IncomingMessage):
    async with message.process():
        # Process the received message here
        print("Received message:", message.body.decode())


async def start_receiver():
    try:
        connection = await connect("amqp://guest:guest@localhost/")
        channel = await connection.channel()
        queue = await channel.get_queue("course_user.queue")
        await queue.consume(process_message)

    except Exception as e:
        print("An error occurred:", str(e))


@app.on_event("startup")
async def startup_event():
    # Start the receiver
    asyncio.create_task(start_receiver())


@app.get("/")
async def root():
    return {"message": "Hello World"}
