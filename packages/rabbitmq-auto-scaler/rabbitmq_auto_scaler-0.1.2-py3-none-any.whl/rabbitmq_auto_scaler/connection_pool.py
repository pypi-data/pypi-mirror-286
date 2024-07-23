import asyncio
from aio_pika import connect_robust
from aio_pika.connection import Connection
from logger import logger

class ConnectionPool:
    def __init__(self, url, pool_size=10):
        self.url = url
        self.pool_size = pool_size
        self.pool = asyncio.Queue(maxsize=pool_size)
        self._initialize_pool()

    def _initialize_pool(self):
        # Start pool initialization tasks
        self._tasks = [asyncio.create_task(self._create_and_add_connection()) for _ in range(self.pool_size)]

    async def _create_and_add_connection(self):
        try:
            connection = await connect_robust(self.url)
            await self.pool.put(connection)
            logger.info("Connection added to pool")
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")

    async def get_connection(self):
        # Get a connection from the pool
        connection = await self.pool.get()
        logger.debug("Connection acquired from pool")
        return connection

    async def return_connection(self, connection: Connection):
        # Return the connection to the pool
        await self.pool.put(connection)
        logger.debug("Connection returned to pool")

    async def close(self):
        # Close all connections in the pool
        while not self.pool.empty():
            connection = await self.pool.get()
            await connection.close()
            logger.info("Connection closed")

        # Wait for all connection creation tasks to complete
        if hasattr(self, '_tasks'):
            await asyncio.gather(*self._tasks, return_exceptions=True)
        logger.info("All connections closed")
