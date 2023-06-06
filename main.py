import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from message_processor import start_listener

load_dotenv('.env')

app = FastAPI()


@app.get('/')
def index():
    return 'Hello World'


@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ listener
    await start_listener()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
