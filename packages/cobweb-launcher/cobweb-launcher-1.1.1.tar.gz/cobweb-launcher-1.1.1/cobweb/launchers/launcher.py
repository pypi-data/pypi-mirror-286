import time
import inspect
import threading
import importlib

from cobweb import setting
from cobweb.base import Seed, Queue
from cobweb.utils.tools import dynamic_load_class


class Launcher(threading.Thread):

    SEEDS = []

    __DOING__ = {}

    __CUSTOM_FUNC__ = {
        "download": None,
        "download_midware": None,
        "parse": None,
    }

    __LAUNCHER_QUEUE__ = {
        "new": Queue(),
        "todo": Queue(),
        "done": Queue(),
    }

    __LAUNCHER_FUNC__ = [
        "_reset",
        "_scheduler",
        "_insert",
        "_refresh",
        "_delete",
    ]

    def __init__(self, task, project, custom_setting=None):
        super().__init__()
        self.task = task
        self.project = project

        self._stop = threading.Event()  # 结束事件
        self._pause = threading.Event()  # 暂停事件

        if custom_setting:
            setting_ = dict()
            if isinstance(custom_setting, dict):
                setting_ = custom_setting
            else:
                if isinstance(custom_setting, str):
                    custom_setting = importlib.import_module(custom_setting)
                if not inspect.ismodule(custom_setting):
                    raise Exception
                for k, v in custom_setting.__dict__.items():
                    if not k.startswith("__") and not inspect.ismodule(v):
                        setting_[k] = v
            for k, v in setting_.items():
                setattr(setting, k, v)

        self._Crawler = dynamic_load_class(setting.CRAWLER)
        self._Pipeline = dynamic_load_class(setting.PIPELINE)

        self._scheduler_wait_seconds = setting.SCHEDULER_WAIT_SECONDS
        self._todo_queue_full_wait_seconds = setting.TODO_QUEUE_FULL_WAIT_SECONDS
        self._new_queue_wait_seconds = setting.NEW_QUEUE_WAIT_SECONDS
        self._done_queue_wait_seconds = setting.DONE_QUEUE_WAIT_SECONDS
        self._upload_queue_wait_seconds = setting.UPLOAD_QUEUE_WAIT_SECONDS
        self._seed_reset_seconds = setting.SEED_RESET_SECONDS

        self._todo_queue_size = setting.TODO_QUEUE_SIZE
        self._new_queue_max_size = setting.NEW_QUEUE_MAX_SIZE
        self._done_queue_max_size = setting.DONE_QUEUE_MAX_SIZE
        self._upload_queue_max_size = setting.UPLOAD_QUEUE_MAX_SIZE

        self._done_model = setting.DONE_MODEL

        self._upload_queue = Queue()

    @property
    def start_seeds(self):
        return [Seed(seed) for seed in self.SEEDS]

    @property
    def request(self):
        """
        自定义request函数
        use case:
            from cobweb.base import Request, BaseItem
            @launcher.request
            def request(seed: Seed) -> Union[Request, BaseItem]:
                ...
                return Request(seed.url, seed)
        """
        def decorator(func):
            self.__CUSTOM_FUNC__["request"] = func
        return decorator

    @property
    def download(self):
        """
        自定义download函数
        use case:
            from cobweb.base import Request, Response, Seed, BaseItem
            @launcher.download
            def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
                ...
                yield Response(item.seed, response)
        """
        def decorator(func):
            self.__CUSTOM_FUNC__["download"] = func
        return decorator

    @property
    def parse(self):
        """
        自定义parse函数, xxxItem为自定义的存储数据类型
        use case:
            from cobweb.base import Request, Response
            @launcher.download
            def download(item: Response) -> BaseItem:
               ...
               yield xxxItem(seed, **kwargs)
        """
        def decorator(func):
            self.__CUSTOM_FUNC__["parse"] = func
        return decorator

    def _remove_doing_seeds(self, seeds):
        for seed in seeds:
            self.__DOING__.pop(seed, None)

    def _execute_heartbeat(self):
        pass

    def _reset(self):
        pass

    def _scheduler(self):
        pass

    def _insert(self):
        pass

    def _refresh(self):
        pass

    def _delete(self):
        pass

    def _execute(self):
        for func_name in self.__LAUNCHER_FUNC__:
            threading.Thread(name=func_name, target=getattr(self, func_name)).start()
            time.sleep(2)

    def _polling(self):

        check_emtpy_times = 0

        while not self._stop.is_set():

            queue_not_empty_count = 0

            for q in self.__LAUNCHER_QUEUE__.values():
                if q.length != 0:
                    queue_not_empty_count += 1

            if self._pause.is_set() and queue_not_empty_count != 0:
                self._pause.clear()
                self._execute()

            elif queue_not_empty_count == 0:
                check_emtpy_times += 1
            else:
                check_emtpy_times = 0

            if check_emtpy_times > 2:
                check_emtpy_times = 0
                self.__DOING__ = {}
                self._pause.set()

    def run(self):
        threading.Thread(target=self._execute_heartbeat).start()

        self._Crawler(
            upload_queue=self._upload_queue,
            custom_func=self.__CUSTOM_FUNC__,
            launcher_queue=self.__LAUNCHER_QUEUE__,
        ).start()

        self._Pipeline(
            upload_queue=self._upload_queue,
            done_queue=self.__LAUNCHER_QUEUE__["done"],
            upload_queue_size=self._upload_queue_max_size,
            upload_wait_seconds=self._upload_queue_wait_seconds
        ).start()

        self._execute()
        self._polling()
