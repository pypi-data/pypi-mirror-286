import pytest
import pytest_asyncio
import asyncio
import logging
from rabbitmq_auto_scaler import AutoScaler
from unittest.mock import patch

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mq_url = 'amqps://your_username:your_password@your_rabbitmq_url:5671'
queue = 'your_queue_name'
min_consumers = 1
max_consumers = 5
scale_up_threshold = 10
scale_down_threshold = 1
check_interval = 1

@pytest_asyncio.fixture
async def auto_scaler():
    logger.debug("Initializing AutoScaler")
    auto_scaler = AutoScaler(
        mq_url, queue, min_consumers, max_consumers,
        scale_up_threshold, scale_down_threshold, check_interval,
        test_mode=True 
    )
    with patch.object(auto_scaler, 'start', return_value= await asyncio.sleep(10)):
        start_task = asyncio.create_task(auto_scaler.start())

        try:
            await asyncio.wait_for(start_task, timeout=10)
            logger.debug("AutoScaler initialized and started")
            yield auto_scaler
        except asyncio.TimeoutError:
            logger.error("Timeout while initializing AutoScaler")
            raise
        finally:
            await auto_scaler.stop()
            logger.debug("AutoScaler stopped")

@pytest.mark.asyncio
async def test_auto_scaler_start(auto_scaler):
    logger.debug("Starting test_auto_scaler_start")
    assert not auto_scaler.is_running()
    logger.debug("Completed test_auto_scaler_start")

@pytest.mark.asyncio
async def test_set_message_handler(auto_scaler):
    logger.debug("Starting test_set_message_handler")
    async def mock_handler(message):
        assert message is not None

    await auto_scaler.set_message_handler(mock_handler)
    logger.debug("Completed test_set_message_handler")

@pytest.mark.asyncio
async def test_get_queue_length(auto_scaler):
    logger.debug("Starting test_get_queue_length")
    length = await auto_scaler.get_queue_length()
    assert length >= 0  # Ensure queue length is non-negative
    logger.debug("Completed test_get_queue_length")
    
@pytest.mark.asyncio
async def test_auto_scaler_stop(auto_scaler):
    logger.debug("Starting test_auto_scaler_stop")
    await auto_scaler.stop()
    assert not auto_scaler.is_running()  # Ensure the scaler is stopped
    logger.debug("Completed test_auto_scaler_stop")
