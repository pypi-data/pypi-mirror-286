import aio_pika
from logger import logger

class AsyncThreadedWorker:
    def __init__(self, queue_name, connection, message_handler):
        self.queue_name = queue_name
        self.connection = connection
        self.channel = None
        self.queue = None
        self.message_handler = message_handler
        self.consumer_tag = None

    async def start(self):
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        self.consumer_tag = await self.queue.consume(self.on_message)
        logger.info(f"Consumer started for queue: {self.queue_name}")

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            if self.message_handler:
                await self.message_handler(message)

    async def stop_worker(self):
        if self.channel and self.consumer_tag:
            await self.queue.cancel(self.consumer_tag)
            await self.channel.close()
            logger.info(f"Consumer stopped for queue: {self.queue_name}")
