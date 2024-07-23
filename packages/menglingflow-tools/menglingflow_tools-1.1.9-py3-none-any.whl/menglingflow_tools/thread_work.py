from threading import Thread, get_ident
from menglingtool.queue import Mqueue
import traceback
import os
import logging
import time
import asyncio

# 便捷获取log对象
def getLogger(name, level=logging.INFO, log_path=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(log_path) if log_path else logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class WorkPool:
    def __init__(self, logger: logging.Logger = None) -> None:
        self.logger = logger if logger else getLogger(f'pid-{get_ident()}')
        self.task_queue = Mqueue()
        self._alive = False
    
    def getTaskNum(self) -> int:
        return self.task_queue.qsize()
    
    def is_alive(self) -> bool:
        return self._alive
    
    def stop(self):
        self._alive = False
    
    def start(self, *, getGood = None, getResult, good_num: int = 3,
                        is_put_args=False,
                        is_put_kwargs=False,
                        is_put_time=True) -> list:
        assert not self._alive, '任务已启动!'
        self.logger.info(f'PID-{os.getpid()} worker num: {good_num}')
        self._alive = True
        
        def _worker():
            gooder = getGood() if getGood else None
            while self._alive:
                que, index, args, kwargs = self.task_queue.get()
                sd = time.time()
                try:
                    result = getResult(gooder, *args, **kwargs) if gooder else getResult(*args, **kwargs)
                    err = None
                except:
                    err = traceback.format_exc()
                    result = None

                self.logger.info(f'args:{args}, kwargs:{kwargs}, is_err:{bool(err)}')
                rdt = {}
                if is_put_args: rdt['args'] = args
                if is_put_kwargs: rdt['kwargs'] = kwargs
                rdt['index'] = index
                rdt['result'] = result
                rdt['err'] = err
                if is_put_time: rdt['time'] = time.time() - sd
                que.put(rdt)

        ts = [Thread(target=_worker, daemon=True) for _ in range(good_num)]
        [t.start() for t in ts]
        return ts


    def arg_in_task_puts(self, vs: list) -> Mqueue: 
        return self.all_in_task_puts([[(v,), {}] for v in vs])


    def args_in_task_puts(self, argss: list) -> Mqueue:
        return self.all_in_task_puts([[args, {}] for args in argss])


    def kwargs_in_task_puts(self, kwargss: list) -> Mqueue:
        return self.all_in_task_puts([[(), kwargs] for kwargs in kwargss])


    def all_in_task_puts(self, args_and_kwargs: list) -> Mqueue:
        result_queue = Mqueue(maxsize=len(args_and_kwargs))
        self.task_queue.puts(*[(result_queue, i, *args_kwargs) for i, args_kwargs in enumerate(args_and_kwargs)])
        return result_queue

    @staticmethod
    def getResults(result_queue: Mqueue, is_sorded=True) -> list:
        while not result_queue.full():
            time.sleep(1)
        ls = result_queue.to_list()
        return sorted(ls, key = lambda x: x['index']) if is_sorded else ls

    @staticmethod
    async def async_getResults(result_queue: Mqueue, is_sorded=True) -> list:
        while not result_queue.full():
            await asyncio.sleep(1)
        ls = result_queue.to_list()
        return sorted(ls, key = lambda x: x['index']) if is_sorded else ls