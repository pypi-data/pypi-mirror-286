import asyncio
import logging
import time
import traceback
from pydantic import BaseModel
from typing import TypeAlias, Callable, Dict, Type, Optional
from . import GenericQueue, QueueRole, QueueTopicMessage, QueueMessage, QueueMessageType
from ...common.stoppable import Stoppable
from ..types import BaseChannelRequest, BaseChannelResponse, ReceiverRoutingIdType, RequestIdType

logger = logging.getLogger()


class Result(BaseModel):
    done: asyncio.Event
    response_cls: Type[BaseChannelResponse]
    response: Optional[BaseChannelResponse] = None

    class Config:
        arbitrary_types_allowed = True


class GenericQueueChannel(Stoppable):
    read_q: GenericQueue
    write_q: GenericQueue
    receiver_routing_id: ReceiverRoutingIdType
    results: Dict[RequestIdType, Result]
    get_topic_func: Callable

    def __init__(
        self, receiver_routing_id, connection_url, queue_w_name: str, queue_r_name: str, get_topic_func: Callable
    ):
        super().__init__()
        self.receiver_routing_id = receiver_routing_id
        self.get_topic_func = get_topic_func
        self.results = {}

        self.write_q = GenericQueue(
            role=QueueRole.Publisher,
            url=connection_url,
            name=queue_w_name,
        )
        self.read_q = GenericQueue(
            role=QueueRole.Receiver,
            url=connection_url,
            name=queue_r_name,
            topic=get_topic_func(receiver_routing_id),
        )

    async def run(self):
        self.tasks.append(asyncio.create_task(self.loop()))
        await super().run()

    async def loop(self):
        await self.write_q.run()
        await self.read_q.run()
        try:
            logger.debug("embeddings_loop")
            await self.read_q.is_ready()
            logger.debug("self.input is ready")

            while not await self.is_stopped():
                message = await self.read_q.pop(timeout=5)
                if message:
                    qm = QueueTopicMessage.decode(message.routing_key, message.body)
                    expected_routing_key = self.get_topic_func(self.receiver_routing_id)
                    if message.routing_key == expected_routing_key:
                        base_response = BaseChannelResponse(**qm.data)
                        response_cls = self.results[base_response.request_id].response_cls
                        response = response_cls(**qm.data)
                        logger.info(f"got {response=}")
                        self.results[response.request_id].response = response
                        self.results[response.request_id].done.set()
                        await self.read_q.mark_done(message)
                    else:
                        logger.error(f"!!!!!!!!!!!!!!! BUG: unexpected topic {message=} {qm=} {expected_routing_key=}")
                        await self.read_q.reject(message, requeue=False)

            logger.debug("channel stopped")
            await self.read_q.stop()
            await self.write_q.stop()
        except Exception as e:
            logger.error(f"process_crawler_urls_responses exception {e}")
            logger.error(traceback.format_exc())

    async def process(self, write_cls: Type[BaseChannelRequest], read_cls: Type[BaseChannelResponse], **write_kwargs):
        request_id = str(time.time())
        task = write_cls(request_id=request_id, receiver_routing_id=self.receiver_routing_id, **write_kwargs)

        logger.info(f"channel::process {task=}")

        self.results[request_id] = Result(done=asyncio.Event(), response_cls=read_cls)
        await self.write_q.push(
            QueueMessage(
                message_type=QueueMessageType.Task,
                data=task,
            )
        )
        await asyncio.wait_for(self.results[request_id].done.wait(), timeout=None)
        res = self.results[request_id].response
        del self.results[request_id]
        return res
