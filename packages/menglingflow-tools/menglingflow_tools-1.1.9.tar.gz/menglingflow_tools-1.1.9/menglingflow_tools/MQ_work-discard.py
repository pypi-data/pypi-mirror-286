import pika
import logging
import logging.handlers
from threading import Thread
import json
import os
import time
import asyncio
import traceback

EXCHANGE = 'mengling_factory'

# 便捷获取log对象
def getLogger(name, level=logging.INFO, log_path=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(log_path,
                                                   maxBytes=5 * 1024 * 1024,
                                                   backupCount=5) if log_path else logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def getMQConnection(host, username, password, port=5672, virtual_host='/') -> pika.ConnectionParameters:
    # RabbitMQ服务器的连接参数
    parameters = pika.ConnectionParameters(
        host=host,  # RabbitMQ服务器地址
        port=port,         # RabbitMQ服务器端口，默认是5672
        virtual_host=virtual_host,  # 虚拟主机名称，默认是'/'
        credentials=pika.PlainCredentials(
            username=username,  # RabbitMQ用户名
            password=password  # RabbitMQ密码
        )
    )
    return parameters

def _init_factory(channel, factory, durable):
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')
    channel.queue_declare(queue=factory)
    channel.queue_bind(exchange=EXCHANGE, durable=durable, queue=factory, routing_key=f'{factory}_.*')
    
def _init_result(channel, factory, task_name, durable):
    queue_name = f'result_{factory}_{task_name}'
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=EXCHANGE, durable=durable, queue=queue_name)
    return queue_name
            
def factory_start(mqcon: pika.ConnectionParameters, factory:str, good_getResult, 
                  good_num=1, logger: logging.Logger = None, durable=True)->list:
    logger = logger if logger else getLogger(f'factory-{factory}')
    logger.info(f'factory-{factory} worker num: {good_num}')
    
    def callback(ch, method, properties, body):
        try:
            result = good_getResult(body)
            ch.basic_publish(exchange=EXCHANGE, routing_key=f'result_{method.routing_key}', body=result)
        except:
            pass
    
    with pika.BlockingConnection(mqcon) as connection:
        channel = connection.channel()    
        _init_factory(channel, factory, durable=durable)
        def _worker():
            channel.basic_consume(queue=factory, on_message_callback=callback)
            channel.start_consuming()
        
        ts = [Thread(target=_worker, daemon=True) for _ in range(good_num)]
        [t.start() for t in ts]
        return ts


def task_puts(mqcon: pika.ConnectionParameters, factory:str, task_name:str, values:list, durable=True):
    with pika.BlockingConnection(mqcon) as connection:
        with connection.channel() as channel:
            _init_factory(channel, factory, durable=durable)
            queue_name = _init_result(channel, factory, task_name, durable=durable)
            for v in values:
                channel.basic_publish(exchange=EXCHANGE, routing_key=queue_name, body=v)

            
def result_It_get(mqcon: pika.ConnectionParameters, factory:str, task_name:str, durable=True)-> bytes:
    queue_name = _init_result(channel, factory, task_name, durable=durable)
    with pika.BlockingConnection(mqcon) as connection:
        with connection.channel() as channel:
            method, properties, body = channel.basic_get(queue=queue_name)
            if method:
                channel.basic_ack(delivery_tag = method.delivery_tag)
                yield body
            else:
                time.sleep(1)

async def async_result_It_get(mqcon: pika.ConnectionParameters, factory:str, task_name:str, durable=True)-> bytes:
    queue_name = _init_result(channel, factory, task_name, durable=durable)
    with pika.BlockingConnection(mqcon) as connection:
        with connection.channel() as channel:
            while True:
                method, properties, body = channel.basic_get(queue=queue_name)
                if method:
                    channel.basic_ack(delivery_tag = method.delivery_tag)
                    yield body
                # elif channel.(queue=f'{factory}_{task_name}') > 0:
                #     await asyncio.sleep(1)
                else:
                    break

def result_gets(mqcon: pika.ConnectionParameters):
    with pika.BlockingConnection(mqcon) as connection:
        with connection.channel() as channel:
            pass


if __name__ == '__main__':
    mqcon = getMQConnection('tianyiblue.work', 'ljh', 'mq246822', port=4672)
    with pika.BlockingConnection(mqcon) as connection:
        with connection.channel() as channel:
            queue_name = 'test'
            # channel.exchange_declare(exchange=EXCHANGE)
            # channel.queue_declare(queue=queue_name)
            # channel.queue_bind(exchange=EXCHANGE, queue=queue_name)
            # channel.basic_publish(exchange=EXCHANGE, routing_key=queue_name, body=json.dumps({'a': 3, 'b': 2}))
            method, properties, body = channel.basic_get(queue=queue_name)
            print(method, properties, body)
            channel.basic_nack(method.delivery_tag,requeue=True)
            # channel.basic_get(queue=queue_name)
            # print(result)
