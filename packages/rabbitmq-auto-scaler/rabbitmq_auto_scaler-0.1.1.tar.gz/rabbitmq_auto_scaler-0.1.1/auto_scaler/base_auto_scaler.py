from abc import ABC, abstractmethod

class BaseAutoScaler(ABC):
    def __init__(self, mq_url, queue_name, min_consumers=1, max_consumers=10, scale_up_threshold=10, scale_down_threshold=5, check_interval=30):
        self.mq_url = mq_url
        self.queue_name = queue_name
        self.min_consumers = min_consumers
        self.max_consumers = max_consumers
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.check_interval = check_interval

    @abstractmethod
    async def start(self):
        """Start the auto-scaling process."""
        pass

    @abstractmethod
    async def set_message_handler(self, handler):
        """Set the message handler."""
        pass

    @abstractmethod
    async def stop(self):
        """stop the auto-scaling process."""
        pass

    @abstractmethod
    async def get_queue_length(self):
        """Get the length of the queue."""
        pass
    
    @abstractmethod
    def is_running(self):
        """Check if the auto-scaler is running."""
        pass
