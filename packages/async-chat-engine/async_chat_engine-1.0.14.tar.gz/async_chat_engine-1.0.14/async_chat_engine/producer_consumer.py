"""
Module for ProducerConsumer, which handles the production and consumption of messages using the ChatEngine for processing.
"""
import asyncio
import json
import logging
import uuid

from .chat_engine import ChatEngine


class ProducerConsumer:
    """
    ProducerConsumer handles the queue for producing and consuming messages using the ChatEngine.
    """

    def __init__(self, num_consumers: int, engine: ChatEngine, logger: str) -> None:
        """
        Initialises the ProducerConsumer with the specified number of consumers and a ChatEngine instance.

        Args:
            num_consumers (int): The number of consumer tasks to create.
            engine (ChatEngine): The chat engine instance to use for processing.
        """
        self._queue = asyncio.Queue()
        self._num_consumers = num_consumers
        self._chat_engine = engine
        self._initialised = False
        self._logger = logging.getLogger(logger)
        self._logger.info("Creating ProducerConsumer object")

    async def init_consumers(self):
        """
        Initialises the consumer tasks if they have not been initialised yet.
        """
        if not self._initialised:
            self._logger.info("Initialising consumers")
            self._consumers = [
                asyncio.create_task(self._consume()) for _ in range(self._num_consumers)
            ]
            self._initialised = True

    async def close_consumers(self):
        """
        Cancels and closes the consumer tasks.
        """
        for consumer in self._consumers:
            consumer.cancel()
        await asyncio.gather(*self._consumers, return_exceptions=True)
        self._logger.info("Consumers closed")
        self._initialised = False

    async def produce(self, message):
        """
        Puts a message onto the queue to be consumed by the consumer tasks.

        Args:
            message (Tuple[str, str, websocket]): The message to be processed.
        """
        self._logger.info("Producing message: %s", message)
        await self._queue.put(message)

    async def _consume(self):
        """
        Consumes messages from the queue and processes them using the ChatEngine.
        """
        self._logger.info("Consuming messages")
        _sampling_params = self._chat_engine.create_sampling_params()
        while True:
            # Get message from queue
            _message = await self._queue.get()
            self._logger.info("Got message from queue: %s", _message)
            try:
                # Unpack message
                _query, _user_id, _websocket = _message

                # Set the role
                _role = "user"
                
                # Create prompt for engine
                self._chat_engine.update_chat_history(_user_id, _role, _query)
                _prompt = self._chat_engine.create_prompt(_user_id)

                # Process message
                _stream = await self._chat_engine.engine.add_request(
                    uuid.uuid4().hex, _prompt, _sampling_params
                )

                self._logger.info("Stream created for User: %s %s", _user_id, _stream)

                # Process output
                _cursor = 0
                _output = ""
                async for _request_output in _stream:
                    _output += _request_output.outputs[0].text[_cursor:]

                    await _websocket.send(json.dumps({"message": _output, "status": "generating"}))

                    _cursor = len(_request_output.outputs[0].text)

                await _websocket.send(json.dumps({"message": _output, "status": "complete"}))
                
                # Set the role
                _role = "assistant"
                
                self._chat_engine.update_chat_history(_user_id, _role, _output)
                self._logger.info(
                    "Completed request for User: %s, %s",
                    _user_id,
                    _output,
                )
            except Exception as e:
                self._logger.error("Error processing message: %s", e)
            finally:
                # Mark task as done
                self._queue.task_done()
