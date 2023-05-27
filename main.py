from uuid import uuid4, UUID
import pika

from fastapi import FastAPI, HTTPException

from models import User, Gender, Role

app = FastAPI()

db = [
    User(
        id=uuid4(),
        first_name="Mohammed",
        last_name="Alder",
        gender=Gender.male,
        roles=[Role.user, Role.admin]
    ),
    User(
        id=uuid4(),
        first_name="Huda",
        last_name="Set",
        gender=Gender.female,
        roles=[Role.user]
    )
]


def process_message(channel, method, properties, body):
    # Process the received message here
    print("Received message:", body.decode())

    # Acknowledge the message to remove it from the queue
    channel.basic_ack(delivery_tag=method.delivery_tag)


@app.on_event("startup")
async def startup_event():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Declare the queue from which the receiver will consume messages
    channel.queue_declare(queue="course_user.queue")

    # Set up the consumer callback
    channel.basic_consume(queue="course_user.queue", on_message_callback=process_message)

    # Start consuming messages
    channel.start_consuming()


@app.get("/")
async def root():
    return {"Hello": "DD"}


@app.get("/getUsers")
async def getUsers():
    return db


@app.post("/newUser")
async def addUser(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/deleteUser/{user_id}")
async def deleteUser(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "User is deleted"
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exists"
    )
