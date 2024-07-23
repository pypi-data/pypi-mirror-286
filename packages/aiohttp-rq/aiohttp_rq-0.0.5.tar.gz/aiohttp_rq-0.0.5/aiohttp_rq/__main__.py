import asyncio
import json
import logging
import os
import sys
import time

import aiohttp
import click

from .redis_client import REDIS, REQUEST_QUEUE
from .utils import get_client_session_kwargs, get_request_kwargs, process_request_exception, process_response

REDIS_PREFETCH_COUNT = 100
AIOHTTP_RQ_DEBUG = bool(os.environ.get('AIOHTTP_RQ_DEBUG',None))
ASYNCIO_QUEUE = asyncio.Queue()


async def redis_queue_worker(session):
    global ASYNCIO_QUEUE
    while True:
        try:
            pipe = REDIS.pipeline()
            pipe.lrange(REQUEST_QUEUE, 0, REDIS_PREFETCH_COUNT - 1)
            pipe.ltrim(REQUEST_QUEUE, REDIS_PREFETCH_COUNT, -1)
            redis_value_list, trim_success = pipe.execute()
            if not redis_value_list:
                await asyncio.sleep(0.1)
                continue
            for value in redis_value_list:
                await ASYNCIO_QUEUE.put(value)
        except Exception as e: # redis exception
            logging.error(e)
            sys.exit(1)

async def request_worker(session):
    global ASYNCIO_QUEUE
    while True:
        try:
            redis_value = await ASYNCIO_QUEUE.get()
        except Exception as e: # redis exception
            logging.error(e)
            sys.exit(1)
        try:
            redis_data = json.loads(redis_value.decode("utf-8"))
            request_kwargs = get_request_kwargs(redis_data)
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        try:
            if AIOHTTP_RQ_DEBUG:
                print('%s %s' % (request_kwargs['method'],request_kwargs['url']))
            async with session.request(**request_kwargs) as response:
                if AIOHTTP_RQ_DEBUG:
                    print('%s %s' % (request_kwargs['url'],response.status))
                await process_response(redis_data,response)
        except Exception as e: # session.request() exception
            if AIOHTTP_RQ_DEBUG:
                print('%s\n%s: %s' % (request_kwargs['url'],type(e),str(e)))
            process_request_exception(redis_data,e)


async def asyncio_main(loop, workers_count):
    async with aiohttp.ClientSession(**get_client_session_kwargs()) as session:
        task_list = [redis_queue_worker(session)]+list(map(
            lambda i:request_worker(session),[None]*workers_count
        ))
        await asyncio.gather(*task_list, return_exceptions=True)


@click.command()
@click.argument('workers_count', required=True)
def main(workers_count):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(asyncio_main(loop, int(workers_count)))

if __name__ == '__main__':
    main(prog_name='python -m aiohttp_rq')
