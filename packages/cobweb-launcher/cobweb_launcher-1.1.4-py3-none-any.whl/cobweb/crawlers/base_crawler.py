import threading

from inspect import isgenerator
from typing import Union, Callable, Mapping

from cobweb.base import Queue, Seed, BaseItem, Request, Response, logger
from cobweb.constant import DealModel, LogTemplate
from cobweb.utils import download_log_info
from cobweb import setting


class Crawler(threading.Thread):

    def __init__(
            self,
            upload_queue: Queue,
            custom_func: Union[Mapping[str, Callable]],
            launcher_queue: Union[Mapping[str, Queue]],
    ):
        super().__init__()

        self.upload_queue = upload_queue
        for func_name, _callable in custom_func.items():
            if isinstance(_callable, Callable):
                self.__setattr__(func_name, _callable)

        self.launcher_queue = launcher_queue

        self.spider_thread_num = setting.SPIDER_THREAD_NUM
        self.max_retries = setting.SPIDER_MAX_RETRIES

    @staticmethod
    def request(seed: Seed) -> Union[Request, BaseItem]:
        stream = True if setting.DOWNLOAD_MODEL else False
        return Request(seed.url, seed, stream=stream, timeout=5)

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        response = item.download()
        yield Response(item.seed, response, **item.to_dict)

    @staticmethod
    def parse(item: Response) -> BaseItem:
        pass

    def get(self) -> Seed:
        return self.launcher_queue['todo'].pop()

    def spider(self):
        while True:
            seed = self.get()

            if not seed:
                continue

            elif seed.params.retry >= self.max_retries:
                seed.params.identifier = DealModel.fail
                self.launcher_queue['done'].push(seed)
                continue

            item = self.request(seed)

            if isinstance(item, Request):

                download_iterators = self.download(item)

                if not isgenerator(download_iterators):
                    raise TypeError("download function isn't a generator")

                seed_detail_log_info = download_log_info(seed.to_dict)

                try:
                    for it in download_iterators:
                        if isinstance(it, Response):
                            response_detail_log_info = download_log_info(it.to_dict)
                            logger.info(LogTemplate.download_info.format(
                                detail=seed_detail_log_info, retry=item.seed.params.retry,
                                priority=item.seed.params.priority,
                                seed_version=item.seed.params.seed_version,
                                identifier=item.seed.params.identifier,
                                status=it.response, response=response_detail_log_info
                            ))
                            parse_iterators = self.parse(it)
                            if not isgenerator(parse_iterators):
                                raise TypeError("parse function isn't a generator")
                            for upload_item in parse_iterators:
                                if not isinstance(upload_item, BaseItem):
                                    raise TypeError("upload_item isn't BaseItem subclass")
                                self.upload_queue.push(upload_item)
                        elif isinstance(it, BaseItem):
                            self.upload_queue.push(it)
                        elif isinstance(it, Seed):
                            self.launcher_queue['new'].push(it)
                        elif isinstance(it, str) and it == DealModel.poll:
                            self.launcher_queue['todo'].push(item)
                            break
                        elif isinstance(it, str) and it == DealModel.done:
                            self.launcher_queue['done'].push(seed)
                            break
                        elif isinstance(it, str) and it == DealModel.fail:
                            seed.params.identifier = DealModel.fail
                            self.launcher_queue['done'].push(seed)
                            break
                        else:
                            raise TypeError("yield value type error!")

                except Exception as e:
                    logger.info(LogTemplate.download_exception.format(
                        detail=seed_detail_log_info, retry=seed.params.retry,
                        priority=seed.params.priority, seed_version=seed.params.seed_version,
                        identifier=seed.params.identifier, exception=e
                    ))
                    seed.params.retry += 1
                    self.launcher_queue['todo'].push(seed)

            elif isinstance(item, BaseItem):
                self.upload_queue.push(item)

    def run(self):
        for index in range(self.spider_thread_num):
            threading.Thread(name=f"spider_{index}", target=self.spider).start()

