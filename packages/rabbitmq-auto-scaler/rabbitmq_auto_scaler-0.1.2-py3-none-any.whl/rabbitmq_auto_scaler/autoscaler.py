import asyncio
from logger import logger
from .async_thread_worker import AsyncThreadedWorker
from .connection_pool import ConnectionPool

class AutoScaler:
    def __init__(self, mq_url, queue, min_consumers, max_consumers, scale_up_threshold, scale_down_threshold, check_interval, **kwargs):
        """
        Initializes the AutoScaler with the given parameters.

        :param mq_url: The message queue URL.
        :param queue: The name of the queue.
        :param min_consumers: The minimum number of consumers.
        :param max_consumers: The maximum number of consumers.
        :param scale_up_threshold: The threshold to scale up consumers.
        :param scale_down_threshold: The threshold to scale down consumers.
        :param check_interval: The interval to check the scaling conditions.
        """
        self.mq_url = mq_url
        self.queue_name = queue
        self.min_consumers = min_consumers
        self.max_consumers = max_consumers
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.check_interval = check_interval
        self.consumers = []
        self._running = False
        self.connection_pool = ConnectionPool(mq_url, pool_size=max_consumers)
        self.message_handler = None
        self.test_mode = kwargs.get('test_mode', False)

    async def set_message_handler(self, handler):
        """
        Sets the message handler for the consumers.

        :param handler: The handler function to process messages.
        """
        self.message_handler = handler
        logger.info("Message handler set.")

    async def start(self):
        await self.initialize_workers()
        logger.info("AutoScaler started.")
        self._running = True
        if self.test_mode:
            await asyncio.sleep(self.check_interval)
            return
        while self._running:
            await self.scale()
            await asyncio.sleep(self.check_interval)

    async def initialize_workers(self):
        try:
            for _ in range(self.min_consumers):
                await self.start_worker()
            logger.info(f"{self.min_consumers} initial consumers started.")
        except Exception as e:
            logger.error(f"Failed to initialize workers: {e}")

    async def start_worker(self):
        connection = await self.connection_pool.get_connection()
        worker = AsyncThreadedWorker(self.queue_name, connection, self.message_handler)
        await worker.start()
        self.consumers.append(worker)

    async def scale(self):
        queue_length = await self.get_queue_length()
        if queue_length > self.scale_up_threshold and len(self.consumers) < self.max_consumers:
            await self.start_worker()
            logger.info(f"Scaled up to {len(self.consumers)} consumers.")
        elif queue_length < self.scale_down_threshold and len(self.consumers) > self.min_consumers:
            await self.stop_worker()
            logger.info(f"Scaled down to {len(self.consumers)} consumers.")

    async def stop_worker(self):
        if self.consumers:
            worker = self.consumers.pop()
            await worker.stop_worker()
            await self.connection_pool.return_connection(worker.connection)

    async def get_queue_length(self):
        connection = await self.connection_pool.get_connection()
        try:
            async with connection.channel() as channel:
                queue = await channel.declare_queue(self.queue_name, passive=True)
                queue_length = queue.declaration_result.message_count
                return queue_length
        except Exception as e:
            logger.error(f"Failed to get queue length: {e}")
            return 0
        finally:
            await self.connection_pool.return_connection(connection)
            
    def is_running(self):
        return self._running

    async def stop(self):
        self._running = False
        for worker in self.consumers:
            await worker.stop_worker()
            await self.connection_pool.return_connection(worker.connection)
        await self.connection_pool.close()
